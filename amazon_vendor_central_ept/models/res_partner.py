""" This file is inherit the existing res partner functionality and added its new functionality """
import logging
from odoo import models, fields

_logger = logging.getLogger("Amazon Vendor center")


class ResPartner(models.Model):
    """
        Inherit the existing functionality of res partner and added its new functionality
    """
    _inherit = 'res.partner'

    avc_warehouse_code = fields.Char('AVC Warehouse Code')
    is_avc_customer = fields.Boolean(string='Customer', default=False)
    invoice_party_id = fields.Char(string='Invoice Party ID')
    delivery_party_id = fields.Char(string='Delivery Party ID')

    def create_or_search_invoice_shipping_partner(self, delivery_address, invoice_address, message_info):
        """
            Used for Search the partners based on domain if partner found then return
            that partners else create the partners and then return those partners.
            :param delivery_address: Delivery Address, Type: Dictionary
            :param invoice_address: Invoice Address, Type: Dictionary
            Added by: Dipak Gogiya, 02/12/2020
            :return: res.partner()
        """
        _logger.info("Message Info : {}".format(message_info))
        delivery_party_id = message_info.get('delivery_party_id', False)
        invoice_party_id = message_info.get('invoice_party_id', False)
        delivery_add_id = inv_add_id = self.env['res.partner']
        _logger.info("Delivery Address Info : {}".format(delivery_address))
        if delivery_party_id:
            delivery_add_id = self.search([('delivery_party_id', '=', delivery_party_id)], limit=1)
        if not delivery_add_id:
            delivery_add_domain = [(address, '=', delivery_address.get(address))
                                   for address in delivery_address]
            delivery_add_id = self.search(delivery_add_domain, limit=1)
            if not delivery_add_id:
                delivery_address.update({'is_avc_customer': True,
                                         'delivery_party_id': delivery_party_id})
                delivery_add_id = self.create(delivery_address)
            else:
                delivery_add_id.write({'is_avc_customer': True,
                                         'delivery_party_id': delivery_party_id})
        _logger.info("Invoice Address Info : {}".format(invoice_address))
        if invoice_party_id:
            inv_add_id = self.search([('invoice_party_id', '=', invoice_party_id)], limit=1)
        if not inv_add_id:
            inv_add_domain = [(inv_address, '=', invoice_address.get(inv_address))
                              for inv_address in invoice_address]
            inv_add_id = self.search(inv_add_domain, limit=1)
            if not inv_add_id:
                invoice_address.update({'is_avc_customer': True,
                                        'invoice_party_id': invoice_party_id})
                inv_add_id = self.create(invoice_address)
            else:
                inv_add_id.write({'is_avc_customer': True,
                                        'invoice_party_id': invoice_party_id})

        return delivery_add_id, inv_add_id
