# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, exceptions
from ..ApiTransaction import PrestashopTransaction

class PrestashopImportOperation(models.TransientModel):
    _inherit = "import.operation"

    prestashop_object_id = fields.Char()
    prestashop_import_date_from = fields.Datetime()
    prestashop_filter_type = fields.Selection([('all', 'All'), ("by_id", "By Id"), ("by_date", "By Date")], default='all')

    def prestashop_get_filter(self):
        return dict(
            prestashop_object_id=self.prestashop_object_id,
            prestashop_import_date_from=self.prestashop_import_date_from
        )

    # def import_button(self):
    #     kw = {'object':self.object}
    #     if hasattr(self,f'{self.channel}_get_filter'):
    #         kw.update(getattr(self,f'{self.channel}_get_filter')())
    #         if hasattr(self,"{}_import_with_filter".format(self.channel)):
    #             return getattr(self,"{}_import_with_filter".format(self.channel))(**kw)
    #     else:
    #         raise exceptions.UserError('Filters for this channel not implemented properly')

    # def prestashop_import_with_filter(self,**kw):
    #     if self.channel_id.channel == "prestashop":
    #         return PrestashopTransaction(channel=self.channel_id).prestashop_import_data(**kw)
    #     else:
    #         return super(prestashopImportOperation,self).import_with_filter(**kw)


	# def import_button(self):
	# 	kw = {'object':self.object}
	# 	if hasattr(self,f'{self.channel}_get_filter'):
	# 		kw.update(getattr(self,f'{self.channel}_get_filter')())
	# 		return self.import_with_filter(**kw)
	# 	else:
	# 		raise exceptions.UserError('Filters for this channel not implemented properly')

	# def import_with_filter(self,**kw):
	# 	return Transaction(channel=self.channel_id).import_data(**kw)
