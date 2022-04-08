# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    check_price_line = fields.Boolean('check', compute='_compute_check_price_line')
    show_warnning = fields.Boolean('show warnning')
    onchange_price = fields.Text('Motivo del Error')
    explanation_onchange_price = fields.Text('Motivo del cambio de precio')
    email_sent = fields.Boolean('Email sent')

    @api.depends('order_line.price_unit')
    def _compute_check_price_line(self):
        for item in self:
            if item.order_line:
                show_warnning_A = False
                show_warnning_B = False
                error_A = 'Los siguientes productos han superado el margen establecido en los ajustes de ventas:\n'
                error_B = 'Los siguientes productos estan por fuera de los limites del margen establecidos en el cliente.:\n'
                for line in item.order_line:
                    product_id = line.product_id
                    if product_id.standard_price > 0:
                        margen = (line.price_unit / (product_id.standard_price / 100)) - 100
                    else:
                        if line.display_type != 'line_note' and line.display_type != 'line_section':
                            raise UserError(_("El producto "+product_id.display_name+" No tiene establecido el costo.\nPor Favor establesca el costo del producto para poder continuar con el proceso."))
                    limit_margin_sale = self.env["ir.config_parameter"].search([('key', '=', 'min_margin_sale')]).value
                    if limit_margin_sale and margen > float(limit_margin_sale) and (line.display_type != 'line_note' and line.display_type != 'line_section'):
                        show_warnning_A = True
                        error_A += '  - '+product_id.name+'\n'
                    elif (margen < item.partner_id.min_margin or margen > item.partner_id.max_margin) and (line.display_type != 'line_note' and line.display_type != 'line_section'):
                        show_warnning_B = True
                        error_B += '  -'+product_id.name+'\n'
                    item.check_price_line = True
                if show_warnning_A and show_warnning_B:
                    item.show_warnning = show_warnning_A
                    item.onchange_price = error_A + '\n' + error_B
                elif show_warnning_A:
                    item.show_warnning = show_warnning_A
                    item.onchange_price = error_A
                elif show_warnning_B:
                    item.show_warnning = show_warnning_B
                    item.onchange_price = error_B
                else:
                    item.show_warnning = False
                    item.onchange_price = None
                    item.explanation_onchange_price = None
            else:
                item.check_price_line = False


    def notificar_correo(self):
        template = self.env.ref('indaws_sumex_customisation.email_margen_indaws')
        if template:
            template.attachment_ids = [(5, 0, [])]
            template.send_mail(self.id, force_send=True)
            template.attachment_ids = [(5, 0, [])]


    def get_emails(self):
        users = self.env['res.users'].search([])
        emails = ''
        for user in users:
            if user.has_group('sales_team.group_sale_manager'):
                if user.email:
                    emails += '<'+user.email+'>,'
        return emails[:-1]


    def write(self, vals):
        if 'show_warnning' in vals and vals['show_warnning'] and not self.email_sent:
            self.notificar_correo()
            vals.update({'email_sent': True})
            return super(SaleOrder, self).write(vals)
        else:
            return super(SaleOrder, self).write(vals)
