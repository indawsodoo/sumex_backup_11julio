# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from xmlrpc.client import Error
from odoo import api, fields, models, _
from odoo.addons.prestashop_odoo_bridge.models.prestapi import PrestaShopWebService,PrestaShopWebServiceDict,PrestaShopWebServiceError,PrestaShopAuthenticationError
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class ImportPrestashoppartners(models.TransientModel):
    _inherit = ['import.partners']
    _name = "import.prestashop.partners"
    _description = "Import Prestashop Partners"

    def _get_state_data(self, prestashop, state_id):
        if prestashop:
            states = prestashop.get("states", resource_id=state_id)
            state_name = states.get("state").get("name")
            state_code = states.get("state").get("iso_code")
            return {"state_name": state_name, "state_code": state_code}

    def _get_country_data(self, prestashop, country_id):
        if prestashop:
            countries = prestashop.get("countries", resource_id=country_id)
            country_code = countries.get("country").get("iso_code")
            return country_code
    
    def _get_address_by_id(self, prestashop, customer_id):
        if prestashop:
            addresses = prestashop.get("addresses", options={
                                       'filter[id_customer]': customer_id})
            if addresses.get('addresses'):
                address_list = addresses.get("addresses").get("address")
                if type(address_list) == dict:
                    address_id = address_list.get("attrs").get("id")
                elif type(address_list) == list:
                    address_id = address_list[0].get("attrs").get("id")
                address = prestashop.get("addresses", address_id)
                address = address.get("address")
                state_id = address.get("id_state")
                state_data = {"state_name": "", "state_code": ""}
                if state_id != "0":
                    state_data = self._get_state_data(
                        prestashop, address.get("id_state"))
                vals = {
                    "street": address.get("address1"),
                    "street2": address.get("address2"),
                    "zip": address.get("postcode"),
                    "city": address.get("city"),
                    "state_name": state_data.get("state_name"),
                    "state_code": state_data.get("state_code"),
                    "country_code": self._get_country_data(prestashop, address.get("id_country"))
                }
                return vals

    def get_customer_by_id(self, prestashop, customer_id):
        if prestashop:
            try:
                customers = prestashop.get("customers", resource_id=customer_id)
            except Exception as e:
                _logger.info("Error:- %r",str(e))
                if self.channel_id.debug == "enable":
                    raise UserError("Error:- %r",str(e))
                return None
            customer_vals = customers["customer"]
            store_id = customer_vals.get("id")
            name = customer_vals.get("firstname")
            last_name = customer_vals.get("lastname")
            email = customer_vals.get("email")
            website = customer_vals.get("website")
            vals = {
                "channel_id": self.channel_id.id,
                "channel": 'prestashop',
                "store_id": store_id,
                "name": name,
                "last_name": last_name,
                "email": email,
                "website": website,
            }
            address_vals = self._get_address_by_id(prestashop, customer_id)
            if address_vals:
                vals.update(address_vals)
            return vals

    def filter_customer_using_date(self, prestashop, import_customer_date):
        if prestashop:
            vals_list = []
            date = fields.Datetime.to_string(import_customer_date)
            try:
                customers = prestashop.get('customers', options={
                    'filter[date_add]': '>['+date+']', 'date': 1})
            except Exception as e:
                _logger.info("=====> Error while fetching customers : %r.", e)
                if self.channel_id.debug == "enable":
                    raise UserError("=====> Error while fetching customers : %r.", str(e))
            customers = customers.get("customers")
            if not customers:
                return vals_list
            customers = customers.get('customer',False)
            if isinstance(customers, list) and len(customers):
                for customer in customers:
                    customer_id = customer['attrs']['id']
                    vals = self.get_customer_by_id(prestashop, customer_id)
                    if vals:
                        vals_list.append(vals)
            elif isinstance(customers, dict):
                customer_id = customers['attrs']['id']
                vals = self.get_customer_by_id(prestashop, customer_id)
                if vals:
                    vals_list.append(vals)
            return vals_list

    def get_customer_all(self, prestashop):
        if prestashop:
            vals_list = []
            customers = prestashop.get("customers")
            customers = customers.get("customers").get("customer")
            for customer in customers:
                customer_id = customer.get("attrs").get("id")
                customer_vals = self.get_customer_by_id(
                    prestashop, customer_id)
                if not customer_vals:continue
                vals_list.append(customer_vals)
            return vals_list

    def import_now(self):
        data_list = []
        prestashop = self._context.get('prestashop')
        prestashop_object_id = self._context.get('prestashop_object_id')
        import_customer_date = self._context.get('prestashop_import_date_from')
        if prestashop_object_id:
            vals = self.get_customer_by_id(prestashop, prestashop_object_id)
            if vals:
                data_list.append(vals)
        elif import_customer_date:
            data_list = self.filter_customer_using_date(
                prestashop, import_customer_date)
        else:
            data_list = self.get_customer_all(prestashop)
        return data_list