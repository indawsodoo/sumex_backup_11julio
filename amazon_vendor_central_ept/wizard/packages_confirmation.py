""" Managing the Packages Functionality of Advance Shipment Notice """
from odoo import models


class PackagesConfirmation(models.TransientModel):
    """
        Managing the Packages Functionality of Advance Shipment Notice
    """
    _name = "packages.confirmation"
    _description = "Packages Confirmation"

    def action_yes(self):
        """
            Usage: Used for validating the picking
            :@task:
            :@author: Dipak Gogiya, 30/12/2020
            :return: True
        """
        context = self._context.copy()
        if context.get('active_id', False):
            stock_immediate_transfer_id = self.env['stock.immediate.transfer']. \
                browse(self._context.get('active_id'))
            context.update({'is_call_from_package_confirmation_wizard': True})
            stock_immediate_transfer_id.with_context(context).process()
        return True
