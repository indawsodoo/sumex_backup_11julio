# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import AccessDenied


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    email_notification = fields.Char(
        "Email Notification", default="odoo@example.com")
    is_email_validation = fields.Boolean("Email Validation")


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res['is_email_validation'] = ICPSudo.get_param('new_user_approval_bizople.is_email_validation',self.is_email_validation)
        res['email_notification'] = ICPSudo.get_param('new_user_approval_bizople.email_notification',self.email_notification)
        return res

    @api.model
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('new_user_approval_bizople.is_email_validation',self.is_email_validation)
        ICPSudo.set_param('new_user_approval_bizople.email_notification',self.email_notification)
        return res