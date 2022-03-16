# -*- coding: utf-8 -*-

from odoo import api, fields, models


class photostock_marcas(models.Model):

    _name = 'sumex.photostock_marcas'
    _description = "photostock lista de marcas exclusivamente para productos de photostock"
    _sql_constraints = [('name_uniq', 'UNIQUE (name)', 'photostock_marcas unique name fault')]

    name = fields.Char(string="Marca", required=True)
