# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Website(models.Model):
    _inherit = 'website'


    def _prepare_sale_order_values(self, partner, pricelist):
        values = super(Website, self)._prepare_sale_order_values(partner, pricelist)
        partner_shipping = self.env['res.partner'].sudo().search([('name', '=', 'Tiba Logistics Spain, S.L.U')], limit=1).id
        if partner_shipping:
            values['partner_shipping_id'] = partner_shipping
        return values