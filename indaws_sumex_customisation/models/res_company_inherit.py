from odoo import api, fields, models


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    move_line_count = fields.Integer(default=0, string='Move Line Count')
