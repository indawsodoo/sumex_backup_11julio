# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    min_margin = fields.Float('Margen Mínimo')
    max_margin = fields.Float('Margen Máximo')

    @api.onchange('min_margin')
    def _onchange_min_margin(self):
        if self.min_margin < 0:
            raise ValidationError('El Margen Mínimo debe ser mayor a cero')
        elif self.min_margin > 100:
            raise ValidationError('El Margen Mínimo debe ser Menor a 100')

    @api.onchange('max_margin')
    def _onchange_max_margin(self):
        if self.max_margin < 0:
            raise ValidationError('El Margen Máximo debe ser mayor a cero')
        elif self.max_margin > 100:
            raise ValidationError('El Margen Máximo debe ser Menor a 100')


