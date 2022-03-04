# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    min_margin_sale = fields.Float(config_parameter='min_margin_sale', string='Margen de venta mínimo (%)', opy=True, default='', store=True)

    @api.onchange('min_margin_sale')
    def _onchange_min_margin_sale(self):
        if self.min_margin_sale < 0:
            raise ValidationError('El Margen Mínimo debe ser mayor a cero')
        elif self.min_margin_sale > 100:
            raise ValidationError('El Margen Mínimo debe ser Menor a 100')
