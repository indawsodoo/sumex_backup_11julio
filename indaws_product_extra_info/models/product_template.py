# -*- coding: utf-8 -*-

from odoo import models, fields

class product_template(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template Inherited'

    last_purchase_price = fields.Float(digits=(6, 2),
                                       string="Last Purchase Price",
                                       compute='_get_datos_purchases')

    last_sale_price = fields.Float(digits=(6, 2),
                                   string="Last Sale Price",
                                   compute='_get_datos_sales')
    ean2 = fields.Char(string="EAN2")

    def _get_datos_purchases(self):
        """This function give last purchase price."""
        for record in self:
            price = 0.0
            l = []
            for elem in record.product_variant_ids:
                l.append(elem.id)
            lines = self.env['purchase.order.line'].search(
                [['product_id', 'in', l],
                 ['order_id.state', 'not in', (
                     'draft', 'sent', 'confirmed', 'cancel')]]).sorted(
                key=lambda r: r.order_id.date_order, reverse=True)
            if len(lines) > 0:
                price = lines[0].price_unit
            record.last_purchase_price = price

    def _get_datos_sales(self):
        """This function give last sale price."""
        for record in self:
            price = 0.0
            l = []
            for elem in record.product_variant_ids:
                l.append(elem.id)
            lines = self.env['sale.order.line'].search(
                [['product_id', 'in', l],
                 ['order_id.state', 'not in',
                  ('draft', 'sent', 'cancel')]]).sorted(
                key=lambda r: r.order_id.date_order, reverse=True)
            if len(lines) > 0:
                price = lines[0].price_unit
            record.last_sale_price = price
