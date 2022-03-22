# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    uom_per_price = fields.Float(string="Last Sale Price", digits='Product Price')
    date_product_sale_line = fields.Date(compute='_compute_date')

    def _compute_date(self):
        for rec in self:
            rec.date_product_sale_line = rec.order_id.effective_date

class product_template_sales_info(models.TransientModel):
    _name = 'product.template.sales.info'
    _description = 'Sales info products'

    line_ids = fields.Many2many('sale.order.line', string="Lines",
                                default=lambda self: self._default_lines())

    def _default_lines(self):
        """This function search product in sale order line and
        set value in line_ids."""
        active_model = self._context.get('active_model')
        product_id = self.env[active_model].browse(self._context.get(
            'active_ids'))[0]
        l = []
        for elem in product_id.product_variant_ids:
            l.append(elem.id)

        line_ids = self.env['sale.order.line'].search(
            [['product_id', 'in', l], ['order_id.state', 'not in', (
                'draft', 'sent', 'cancel')]]).sorted(
            key=lambda r: r.order_id.date_order, reverse=True)
        for line in line_ids:
            line.uom_per_price = line.price_unit
            if 'C' in line.product_uom.name:
                line.uom_per_price = line.price_unit / line.product_uom.factor_inv
        return line_ids
