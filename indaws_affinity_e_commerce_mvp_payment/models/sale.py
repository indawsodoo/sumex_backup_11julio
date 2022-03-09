# -*- coding: utf-8 -*-
from odoo import api, fields, models
import json
from lxml import etree


class SaleOrder(models.Model):
    _inherit = "sale.order"

    deposit_calc = fields.Monetary(compute='_get_deposit_calc', store=True, string='Por favor realizar el siguiente pago para proceder con el pedido')
    is_value_percent = fields.Integer(string='Value' , default=0)


    @api.depends('payment_term_id','amount_total')
    def _get_deposit_calc(self):
        for record in self:
            record.is_value_percent = 0
            record.deposit_calc = 0.0
            if record.payment_term_id and record.payment_term_id.line_ids.filtered(lambda line: line.value == 'percent'):
                record.is_value_percent = 1
                record.deposit_calc = (record.amount_total * record.payment_term_id.line_ids.filtered(lambda line: line.value == 'percent').mapped('value_amount')[0])/100


