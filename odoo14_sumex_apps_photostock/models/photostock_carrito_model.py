# -*- coding: utf-8 -*-

from odoo import api, fields, models


class photostock_carrito(models.Model):

    _name = 'sumex.photostock_carrito'
    _description = "photostock registros de carrito"
    _order = "product_id"

    user_id = fields.Many2one('res.users', string = 'User')
    product_id = fields.Many2one('product.product', string = 'Product')
