# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _search_for_original_product(self, old_product):
        new_product_id = self.env['product.product']
        all_attribute_value_ids = old_product.product_template_attribute_value_ids.mapped('product_attribute_value_id').ids
        for p in old_product.product_tmpl_id.catalog_product_id.product_variant_ids:
            match = True
            for attribute in all_attribute_value_ids:
                if attribute not in p.product_template_attribute_value_ids.mapped('product_attribute_value_id').ids:
                    match = False
            if match:
                new_product_id += p
        return new_product_id

    @api.model
    def create(self, values):
        product_id = values.get('product_id')
        if product_id:
            product = self.env['product.product'].browse(product_id)
            if product and product.product_tmpl_id.is_catalog:
                new_product_id = self._search_for_original_product(product)
                if not new_product_id:
                    raise ValidationError(_("No Product Found"))
                values['product_id'] = new_product_id.id
        res = super(SaleOrderLine, self).create(values)
        return res

    def write(self, values):
        product_id = values.get('product_id')
        if product_id:
            product = self.env['product.product'].browse(product_id)
            if product and product.product_tmpl_id.is_catalog:
                new_product_id = self._search_for_original_product(product)
                if not new_product_id:
                    raise ValidationError(_("No Product Found"))
                values['product_id'] = new_product_id.id
        res = super(SaleOrderLine, self).write(values)
        return res
