# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from xmlrpc.client import Error
import logging
import itertools
from odoo import api, fields, models, _
from odoo.exceptions import UserError,RedirectWarning, ValidationError
from odoo.addons.prestashop_odoo_bridge.models.prestapi import PrestaShopWebService,PrestaShopWebServiceDict,PrestaShopWebServiceError,PrestaShopAuthenticationError
_logger = logging.getLogger(__name__)

OrderStatus = [
    ('0','All'),
    ('6','Canceled'),
    ('5','Shipped'),
    ('2','Complete'),
    ('12','Complete'),
    ('3','Processing'),
    ('13','On Hold'),
    ('9','Pending'),
    ('1','Pending Payment'),
    ('10','Pending Payment'),
    ('14','Pending Payment'),
    ('11','Pending Payment'),
    ('4', 'Shipped')
]

class ImportOrders(models.TransientModel):
    _inherit = ['import.orders']
    _name = 'import.prestashop.orders'
    _description = 'Import Prestashop Orders'

    status = fields.Selection(
        OrderStatus,
        required = 1,
        default = '0'
    )

    def _get_customer_name(self, prestashop, customer_id):
        if prestashop:
            customer = prestashop.get("customers", customer_id)
            customer = customer.get("customer")
            name = customer.get("firstname") + " " + customer.get("lastname")
            customer_email = customer.get("email")
            return {"customer_name": name, "customer_email": customer_email}

    def _get_customer_phone(self, prestashop, customer_id):
        if prestashop:
            address = prestashop.get("addresses",
                                     options={"filter[id_customer]": customer_id})
            address = address.get("addresses")
            if address:
                if type(address.get("address")) == dict:
                    address_id = address.get("address").get("attrs").get("id")
                elif type(address.get("address")):
                    address_id = address.get("address")[
                        0].get("attrs").get("id")
                address = prestashop.get("addresses", address_id)
                address = address.get("address")
                vals = {
                    "customer_phone": address.get("phone"),
                    "customer_mobile": address.get("phone_mobile"),
                }
                return vals

    def get_discount_line_info(self, price):
        return {
            "line_name": "Discount",
            "line_price_unit": float(price),
            "line_product_uom_qty": 1,
            "line_source": "discount",
        }

    def _get_order_line(self, prestashop, channel_id, order_id):
        if prestashop:
            vals = {}
            order = prestashop.get("orders", order_id)
            order = order.get("order")
            if order:
                order_row = order.get("associations").get("order_rows")
                if order_row:
                    vals_list = []
                    discount_price = order.get("total_discounts_tax_incl")
                    order_row = order_row.get("order_row")
                    if type(order_row) == dict:
                        product_id = order_row.get("product_id")
                        tax_excl_price = order_row.get("unit_price_tax_excl")
                        tax_incl_price = order_row.get("unit_price_tax_incl")
                        is_mapped = self.env['channel.template.mappings'].search([
                            ("channel_id", '=', channel_id.id),
                            ('store_product_id', '=', product_id)])
                        product_attribute_id = order_row.get("product_attribute_id")
                        if not is_mapped:
                            product_env = self.env['import.prestashop.products']
                            product_feed_id = product_env._prestashop_create_product_feed(
                                prestashop,channel_id,product_id)
                            _logger.info(
                                'Product feed with id (%r) successfully created.', product_feed_id)
                        if discount_price:
                            vals = {
                                "line_name": order_row.get("product_name"),
                                "line_price_unit": tax_excl_price if channel_id.default_tax_type == "exclude" else tax_incl_price ,
                                "line_product_uom_qty": order_row.get("product_quantity"),
                                "line_product_id": product_id,
                                "line_product_default_code": self.get_default_code(prestashop, product_id),
                                "line_taxes": self._get_product_taxes(prestashop, product_id),
                                "line_variant_ids":  product_attribute_id if product_attribute_id !="0" else "No Variants" 
                            }
                            vals_list.append((0,0,vals))
                            discount_line = self.get_discount_line_info(discount_price)
                            vals_list.append((0,0,discount_line))
                            return {"line_type": "multi", "line_ids": vals_list}
                        else:
                            vals = {
                                "line_type": "single",
                                "line_name": order_row.get("product_name"),
                                "line_price_unit": tax_excl_price if channel_id.default_tax_type == "exclude" else tax_incl_price ,
                                "line_product_uom_qty": order_row.get("product_quantity"),
                                "line_product_id": product_id,
                                "line_product_default_code": self.get_default_code(prestashop, product_id),
                                "line_variant_ids":  product_attribute_id if product_attribute_id !="0" else "No Variants" 
                            }
                            return vals
                    else:
                        for order_val in order_row:
                            product_id = order_val.get("product_id")
                            is_mapped = self.env['channel.template.mappings'].search([
                                ("channel_id", '=', channel_id.id),
                                ('store_product_id', '=', product_id)])
                            product_attribute_id = order_val.get("product_attribute_id")
                            tax_excl_price = order_val.get("unit_price_tax_excl")
                            tax_incl_price = order_val.get("unit_price_tax_incl")
                            if not is_mapped:
                                product_env = self.env['import.prestashop.products']
                                product_feed_id = product_env._prestashop_create_product_feed(
                                    prestashop,channel_id,product_id)
                                _logger.info(
                                    'Product feed with id (%r) successfully created.', product_feed_id)
                            vals = {
                                "line_name": order_val.get("product_name"),
                                "line_product_uom_qty": order_val.get("product_quantity"),
                                "line_price_unit": tax_excl_price if channel_id.default_tax_type == "exclude" else tax_incl_price ,
                                "line_product_id": product_id,
                                "line_product_default_code": self.get_default_code(prestashop, product_id),
                                "line_taxes": self._get_product_taxes(prestashop, product_id),
                                "line_variant_ids":  product_attribute_id if product_attribute_id !="0" else "No Variants" 
                            }
                            vals_list.append((0,0,vals))
                        if discount_price:
                            discount_line = self.get_discount_line_info(discount_price)
                            vals_list.append((0,0,discount_line))
                        return {"line_type": "multi", "line_ids": vals_list}

    def get_variants_ids(self, prestashop, product_id):
        product_data = prestashop.get('product_id/%s' % product_id)
        product_data = product_data.get('product')
        combinations = product_id.get('associations').get('combinations')
        if type(combinations) == dict:
            combinations.get('attrs').get(
                "id")
        elif type(combinations) == list:
            variant_ids = [combination.get('attrs').get(
                "id") for combination in combinations]
        return variant_ids

    def get_default_code(self, prestashop, product_id):
        default_code = ""
        try:
            product_data = prestashop.get('products' , product_id)
        except Exception as e :
            _logger.info("Error :- %r",str(e))
            if self.channel_id.debug == "enable":
                raise UserError("Error :- %r",str(e))
            return default_code
        if product_data:
            default_code = product_data.get('product').get('reference')
        return default_code

    def _get_product_taxes(self, prestashop, product_id):
        if prestashop:
            vals_list = []
            try:
                product_details = prestashop.get("products", product_id)
            except Exception as e:
                _logger.info("Error :- %r",str(e))
                if self.channel_id.debug == "enable":
                    raise UserError("Error :- %r",str(e))
                return vals_list
            product_details = product_details.get("product")
            tax_id = product_details.get("id_tax_rules_group")
            tax_rules = prestashop.get("taxes", options={"filter[id]": tax_id})
            tax_rules = tax_rules["taxes"]
            if tax_rules:
                tax_rule_id = tax_rules.get("tax",{}).get("attrs",{}).get("id")
                tax_rules = prestashop.get("taxes", tax_rule_id)
                tax_rules = tax_rules.get("tax")
                vals = {
                    "rate": float(tax_rules.get("rate")),
                    "name": "VAT",
                    "include_in_price": True,
                    "tax_type": "percent",
                }
                vals_list.append(vals)
            return vals_list

    def _get_shipping_address(self, prestashop, id_address_delivery):
        if prestashop:
            address = prestashop.get("addresses", id_address_delivery)
            address = address.get("address")
            state_id = address.get('id_state')
            customer_id = address.get("id_customer")
            vals = {
                "shipping_partner_id": customer_id,
                "shipping_phone": address.get("phone"),
                "shipping_mobile": address.get("phone_mobile"),
                "shipping_street": address.get("address1"),
                "shipping_street2": address.get("address2"),
                "shipping_zip": address.get("zip"),
                "shipping_city": address.get("city"),
                "shipping_country_code": self._get_country_data(prestashop, address.get("id_country")),
            }
            if state_id != '0':
                state_vals = self._get_state_data(
                    prestashop, address.get("id_state"))
                vals["shipping_state_name"] = state_vals.get("state_name")
                vals["shipping_state_code"] = state_vals.get("state_code")
            vals.update(self._get_customer_name(prestashop, customer_id))
            return vals

    def _get_billing_address(self, prestashop, id_address_invoice):
        if prestashop:
            address = prestashop.get("addresses", id_address_invoice)
            address = address.get("address")
            state_id = address.get('id_state')
            customer_id = address.get("id_customer")
            vals = {
                "invoice_partner_id": customer_id,
                "invoice_email": address.get('email',""),
                "invoice_phone": address.get("phone"),
                "invoice_mobile": address.get("phone_mobile"),
                "invoice_street": address.get("address1"),
                "invoice_street2": address.get("address2"),
                "invoice_zip": address.get("zip"),
                "invoice_city": address.get("city"),
                "invoice_country_code": self._get_country_data(prestashop, address.get("id_country")),
            }
            if state_id != '0':
                state_vals = self._get_state_data(
                    prestashop, address.get("id_state"))
                vals["invoice_state_name"] = state_vals.get("state_name")
                vals["invoice_state_code"] = state_vals.get("state_code")
            vals.update(self._get_customer_name(prestashop, customer_id))
            return vals

    def _get_state_data(self, prestashop, state_id):
        if prestashop:
            states = prestashop.get("states", state_id)
            state_name = states.get("state").get("name")
            state_code = states.get("state").get("iso_code")
            return {"state_name": state_name, "state_code": state_code}

    def _get_country_data(self, prestashop, country_id):
        if prestashop:
            countries = prestashop.get("countries", country_id)
            country_code = countries.get("country").get("iso_code")
            return country_code

    def _get_carrier(self, prestashop, carrier_id):
        if prestashop:
            carriers = prestashop.get("carriers", carrier_id)
            carrier_name = carriers.get("carrier").get("name")
            return carrier_name

    def _get_currency(self, prestashop, currency_id):
        if prestashop:
            currency = prestashop.get("currencies", currency_id)
            currency = currency.get("currency").get("iso_code")
            return currency

    def get_order_all(self, prestashop, channel):
        if prestashop:
            vals_list = []
            orders = prestashop.get("orders")
            orders = orders.get("orders").get("order")
            if orders:
                for order in orders:
                    order_id = order.get("attrs").get("id")
                    order_vals = self._get_order_by_id(prestashop,channel,order_id)
                    if not order_vals:continue
                    vals_list.append(order_vals)
                return vals_list

    def _get_order_by_id(self, prestashop, channel_id, order_id):
        if prestashop:
            try :
                order_vals = prestashop.get("orders", order_id)
            except Exception as e:
                _logger.info("Error :- %r",str(e))
                if self.channel_id.debug == "enable":
                    raise UserError("Error :- %r",str(e))
                return None
            order_vals = order_vals.get("order")
            customer_id = order_vals.get("id_customer")
            customer_vals = self._get_customer_name(prestashop,customer_id)
            vals = {
                "name": order_vals.get("reference"),
                'channel': 'prestashop',
                "channel_id": self.channel_id.id,
                "store_id": order_id,
                "partner_id": customer_id,
                "customer_name": customer_vals.get("customer_name"),
                "customer_email": customer_vals.get("customer_email"),
                "payment_method": order_vals.get("payment"),
                "carrier_id": self._get_carrier(prestashop, order_vals.get("id_carrier")),
                "order_state": order_vals.get("current_state"),
                "currency": self._get_currency(prestashop, order_vals.get("id_currency")),
                "date_order": order_vals.get("date_add"),
                "confirmation_date": order_vals.get("delivery_date"),
                "date_invoice": order_vals.get("invoice_date")
            }
            vals.update(self._get_customer_phone(prestashop,customer_id))
            vals.update(self._get_order_line(prestashop,channel_id,order_id))
            shipping_address_id = order_vals.get("id_address_delivery")
            vals.update(self._get_shipping_address(
                prestashop, shipping_address_id))
            invoice_address_id = order_vals.get("id_address_invoice")
            vals.update(self._get_billing_address(
                prestashop, invoice_address_id))
            return vals

    def _filter_order_using_date(self, prestashop, channel, order_import_date):
        if prestashop:
            vals_list = []
            date = fields.Datetime.to_string(order_import_date)
            try:
                orders = prestashop.get(
                    'orders', options={'filter[date_add]': '>['+date+']', 'date': 1})
            except Exception as e:
                _logger.info("=====> Error while fetching Orders : %r.", e)
                if self.channel_id.debug == "enable":
                    raise UserError("Error while fetching Orders :- %r",str(e))
            orders = orders['orders']['order']
            if isinstance(orders, list) and len(orders):
                for order in orders:
                    order_id = order['attrs']['id']
                    vals = self._get_order_by_id(prestashop,channel,order_id)
                    vals_list.append(vals)
            elif isinstance(orders, dict):
                order_id = orders['attrs']['id']
                vals = self._get_order_by_id(prestashop,channel,order_id)
                vals_list.append(vals)
            return vals_list
    

    def import_now(self):
        data_list = []
        channel = self.channel_id
        prestashop = self._context.get('prestashop')
        prestashop_object_id = self._context.get('prestashop_object_id')
        order_import_date = self._context.get('prestashop_import_date_from')
        if prestashop_object_id:
            vals = self._get_order_by_id(prestashop, channel,prestashop_object_id)
            data_list.append(vals)
        elif order_import_date:
            data_list = self._filter_order_using_date(
                prestashop, channel, order_import_date)
        else:
            data_list = self.get_order_all(prestashop,channel)
        return data_list