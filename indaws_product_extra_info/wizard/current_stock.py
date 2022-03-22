# -*- coding: utf-8 -*-

from odoo import models, fields


class product_template_stock_info(models.TransientModel):
    _name = 'product.template.stock.info'
    _description = 'Stock info products'

    quant_ids = fields.Many2many('stock.quant', string="Warehouse",
                                 default=lambda self: self._default_quants())

    def _default_quants(self):
        """This function search product quantity in Warehouse
        set value in quant_ids."""
        product_id = self.env['product.template'].browse(self._context.get(
            'active_ids'))[0]
        l = []
        for elem in product_id.product_variant_ids:
            l.append(elem.id)

        quants = self.env['stock.quant'].search(
            [['product_id', 'in', l],
             ['location_id.usage', '=', 'internal']])
        return quants
