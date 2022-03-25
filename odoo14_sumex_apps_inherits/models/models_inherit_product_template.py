# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sumex_apps_inherits_product_inherit(models.Model):

	_inherit = 'product.template'

	_existe_producto_como_referencia_sage = fields.Boolean("PRODUCTO EXISTE EN REFERENCIAS SAGE", required = False, default = False)
	_existe_variante_como_referencia_sage = fields.Char("VARIANTE EXISTE EN REFERENCIAS SAGE", required = False, default = False)
