from ast import literal_eval
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ftp_id = fields.Many2one("ftp.server.ept", string="Ftp Server")

    def get_values(self):
        """

        :return:
        """
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()

        ftp_id = literal_eval(icp_sudo.get_param('ftp_connector_ept.ftp_id', default='False'))

        res.update(ftp_id=ftp_id)
        return res

    def set_values(self):
        """

        :return:
        """
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('ftp_connector_ept.ftp_id', self.ftp_id.id)
