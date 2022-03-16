# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PhotostockProductImagesInherit(models.Model):

    _inherit = 'product.image'

    photostock_include = fields.Boolean(string = "Photostock Inclusión", required = False)
    photostock_product_tmpl_id = fields.Many2one('product.template', "Photostock Imagen", index = True, ondelete = "cascade")

    @api.model
    def create(self, vals_list):

        if 'default_photostock_include' not in self._context:
            return super(PhotostockProductImagesInherit, self).create(vals_list)
        vals_list['photostock_include'] = True
        rows = super(PhotostockProductImagesInherit, self).create(vals_list)
        return rows

    @api.model
    def write(self, vals_list):

        if 'default_photostock_include' not in self._context:
            return super(PhotostockProductImagesInherit, self).write(vals_list)
        vals_list['photostock_include'] = True
        rows = super(PhotostockProductImagesInherit, self).write(vals_list)
        return rows
