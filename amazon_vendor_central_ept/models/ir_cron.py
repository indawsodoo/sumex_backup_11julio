""" This file is inherit the existing cron functionality and added its new functionality """
from odoo import models, fields


class IrCron(models.Model):
    """
        Inherit the existing functionality of cron and added its new functionality
    """
    _inherit = 'ir.cron'

    avc_cron_id = fields.Many2one('amazon.vendor.instance', string="Cron Scheduler")
