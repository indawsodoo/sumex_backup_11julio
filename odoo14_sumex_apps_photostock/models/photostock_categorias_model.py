# -*- coding: utf-8 -*-

from odoo import api, fields, models


class photostock_categorias(models.Model):

    _name = 'sumex.photostock_categorias'
    _description = "photostock lista de categorias exclusivamente para productos de photostock"
    _sql_constraints = [('name_uniq', 'UNIQUE (name)', 'photostock_categorias unique name fault')]

    name = fields.Char(string="Categoria", required=True)
