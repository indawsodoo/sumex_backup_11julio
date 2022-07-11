# -*- coding: utf-8 -*-

from odoo import models, fields


class sumex_apps_sage_inherits_account_move_inherit(models.Model):
    _inherit = 'account.move'

    _sage_field_percent_descuento = fields.Char(required=False, string='_sage_field_percent_descuento')
    _sage_field_percent_prontopago = fields.Char(required=False, string='_sage_field_percent_prontopago')
    _sage_field_percent_retencion = fields.Char(required=False, string='_sage_field_percent_retencion')
    _sage_field_percent_financiacion = fields.Char(required=False, string='_sage_field_percent_financiacion')
    _sage_field_percent_rappel = fields.Char(required=False, string='_sage_field_percent_rappel')
