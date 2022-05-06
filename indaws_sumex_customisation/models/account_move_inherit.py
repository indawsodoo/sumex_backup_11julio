# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    statusfacturado=fields.Char('StatusFacturado')