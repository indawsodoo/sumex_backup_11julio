# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_catalog = fields.Boolean(string='Is Catalog?')
    catalog_product_id = fields.Many2one('product.template', string="Catalog Product",
                                         domain="[('is_catalog', '=', False)]")
    all_attribute_value_ids = fields.Many2many('product.attribute.value',
                                               compute="_compute_all_attribute_value_ids")

    @api.depends('attribute_line_ids', 'attribute_line_ids.value_ids')
    def _compute_all_attribute_value_ids(self):
        for rec in self:
            all_attribute_value_ids = rec.attribute_line_ids.mapped('value_ids')
            rec.all_attribute_value_ids = [(6, 0, all_attribute_value_ids.ids)]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self._context.get('get_catalog_product'):
            active_product_id = self.browse(self._context.get('active_id'))
            products = self.search(args, limit=limit)
            actual = self.env['product.template']
            all_attribute_value_ids = active_product_id.all_attribute_value_ids.ids
            for p in products:
                if p.id != active_product_id.id:
                    match = True
                    for attri in all_attribute_value_ids:
                        if attri not in p.all_attribute_value_ids.ids:
                            match = False
                    if match:
                        actual += p
        else:
            actual = self.search(args, limit=limit)

        return actual.name_get()
