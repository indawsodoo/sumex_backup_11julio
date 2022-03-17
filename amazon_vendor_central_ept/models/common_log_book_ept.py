""" This file is inherit the Common Log Book Ept Functionality
and add its new functionality """
from odoo import models, fields


class CommonLogBookEpt(models.Model):
    """
        Inherit existing functionality and added its new functionality.
    """
    _inherit = "common.log.book.ept"
    _order = "id desc"

    amazon_sale_requisition_id = fields.Many2one('amazon.sale.requisition.ept',
                                                 string='Amazon Requisition Order',
                                                 help='Amazon sale requisition', copy=False)

    def create_avc_common_log(self, model_name, log_type, message, requisition=False):
        """
            This method is used for create the common log based on method parameters.
            :param model_name: Contain the name of the model, Type: Char
            :param message: Contain the log message for create the log.
            :return:log
            Added By: Dipak Gogiya
        """
        model = self.env['ir.model'].search([('model', '=', model_name)])
        vals = {
            'type': log_type,
            'module': 'amz_vendor_central',
            'message': message,
            'model_id': model.id,
            'amazon_sale_requisition_id': requisition.id if requisition else requisition
        }
        log = self.create(vals)
        return log

    def get_action_for_avc_operations(self, external_id, form_view_ref, record_ids):
        """
        This function returns an action of defined below external_id and form_view_ref
        of given vendor central sales order ids. It can either be an in a list or a form
        view if there is only one order to show.
        :param external_id: External Id of Resource Object, Type: String
        :param form_view_ref: Form View Reference of Resource Object, Type: String
        :param record_ids: Resource Object Ids
        :author Dipak Gogiya, 21/04/2021
        :Task ID :
        :return:action
        """
        action = self.env.ref(external_id).read()[0]

        if len(record_ids) > 1:
            action['domain'] = [('id', 'in', record_ids.ids)]
        elif record_ids:
            action['views'] = [(self.env.ref(form_view_ref).id, 'form')]
            action['res_id'] = record_ids.id
        return action
