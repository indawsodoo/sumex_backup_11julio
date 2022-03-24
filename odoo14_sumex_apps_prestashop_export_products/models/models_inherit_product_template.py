# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sumex_apps_prestashop_export_products_product_inherit(models.Model):

	_inherit = 'product.template'

	_created_from_import_prestashop_name = fields.Char("Prestashop - Name", required = False, default = '')
	_created_from_import_prestashop_product_id = fields.Integer("Prestashop - Product ID", required = False, default = 0)
