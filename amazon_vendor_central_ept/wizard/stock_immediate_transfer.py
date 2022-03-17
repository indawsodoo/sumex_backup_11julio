""" Inherit the existing functionality and added the new functionality """
from odoo import models


class StockImmediateTransfer(models.TransientModel):
    """
        Inherit the existing functionality and Added the new functionality
    """
    _inherit = 'stock.immediate.transfer'

    def process(self):
        """
            Usage: Used for Pop-up the confirmation wizard of confirm the picking
            without packages if the packages not found and packages feature enable
            of amazon advantage requisition, The confirmation wizard is pop-up only
            when the picking is created from the amazon advantage requisition order,
            if the picking is created from another sources then it should be validated
            as per Odoo default flow
            :@task:
            :@author: Dipak Gogiya, 30/12/2020
            :return: Super() or Wizard
        """
        pickings = self.pick_ids.filtered(lambda picking: picking.is_amazon_vendor_central_picking)
        instance = pickings and pickings[0].amazon_vendor_instance_id
        if instance and instance.is_use_packages and pickings and not self._context.get(
                'is_call_from_package_confirmation_wizard', False):
            if not pickings[0].mapped('package_ids'):
                return self._open_asn_confirmation_wizard()
        return super(StockImmediateTransfer, self).process()

    def _open_asn_confirmation_wizard(self):
        """
            Usage: Open the wizard for confirming the advance shipment notice is sent without
            packages details.
            :@task:
            :@author: Dipak Gogiya, 30/12/2020
            :return: action
        """
        view_id = self.env.ref('amazon_vendor_central_ept.packages_confirmation_form_view')
        action = self.env["ir.actions.act_window"]._for_xml_id(
            'amazon_vendor_central_ept.packages_confirmation_act_window')
        action_data = {'view_id': view_id.id, 'views': [(view_id.id, 'form')], 'target': 'new',
                       'name': 'Confirmation?'}

        action.update(action_data)
        return action
