# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from xmlrpc.client import Error
import logging
from odoo.exceptions import  UserError,RedirectWarning, ValidationError
from odoo import api, fields, models, _
from odoo.addons.prestashop_odoo_bridge.models.prestapi import PrestaShopWebService,PrestaShopWebServiceDict,PrestaShopWebServiceError,PrestaShopAuthenticationError
try:
    from odoo.loglevels import ustr as pob_decode
except:
    from odoo.tools.misc import ustr as pob_decode
_logger = logging.getLogger(__name__)


class ImportPrestashopCategories(models.TransientModel):
    _inherit = ['import.categories']
    _name = "import.prestashop.categories"
    _description = "Import Prestashop Categories"

    def get_category_all(self, prestashop):
        if prestashop:
            vals_list = []
            categories = prestashop.get("categories", options={
                                        'display': '[is_root_category,id_parent,id,name]'})
            categories = categories.get("categories").get("category")
            for category in categories:
                is_root_category = category.get("is_root_category")
                id_parent = category.get("id_parent")
                store_id = category.get("id")
                vals = {
                    "channel_id": self.channel_id.id,
                    "channel": 'prestashop',
                    "leaf_category": is_root_category,
                    "store_id": store_id,
                }
                if type(category['name']['language'])==list:
                    channel_lang = self.channel_id.ps_language_id
                    for cat_name in category['name']['language']:
                        if cat_name['attrs']['id'] == channel_lang:
                            vals["name"] = cat_name['value']
                else:
                    vals['name'] = category.get('name')['language']['value']
                if id_parent != '0':
                    vals['parent_id'] = id_parent
                vals_list.append(vals)
            return vals_list
        
    def filter_category_using_date(self, prestashop, import_category_date):
        if prestashop:
            vals_list = []
            date = fields.Datetime.to_string(import_category_date)
            try:
                categories = prestashop.get('categories', options={
                    'filter[date_add]': '>['+date+']', 'date': 1})
            except Exception as e:
                _logger.info("=====> Error while fetching categories : %r.", e)
                if self.channel_id.debug == "enable":
                    raise UserError("Error while fetching categories : %r.", e)
            categories = categories['categories']['category']
            if isinstance(categories, list) and categories:
                for category in categories:
                    category_id = category['attrs']['id']
                    vals = self.get_category_by_id(prestashop, category_id)
                    if vals:
                        vals_list.append(vals)
            elif isinstance(categories, dict):
                category_id = categories['attrs']['id']
                vals = self.get_category_by_id(prestashop, category_id)
                if vals:
                    vals_list.append(vals)
            return vals_list

    def get_category_by_id(self, prestashop, category_id):
        if prestashop:
            vals = {}
            try:
                categories = prestashop.get("categories", resource_id=category_id)
            except Exception as e:
                _logger.info("Error :- %r",str(e))
                if self.channel_id.debug == "enable":
                    raise UserError("Error :- %r",str(e))
                return vals
            categories = categories.get("category")
            is_root_category = categories.get("is_root_category")
            id_parent = categories.get("id_parent")
            id_shop_default = categories.get("id")
            category_name = categories.get("name").get("language")[
                0].get("value")
            vals = {
                    "channel_id": self.channel_id.id,
                    "channel": 'prestashop',
                    "leaf_category": is_root_category,
                    "store_id": id_shop_default,
                    "name": category_name
                }
            if id_parent != "0":
                vals['parent_id'] = id_parent
        return vals

    def import_now(self):
        data_list = []
        prestashop = self._context.get('prestashop')
        prestashop_object_id = self._context.get('prestashop_object_id')
        import_category_date = self._context.get("prestashop_import_date_from")
        if prestashop_object_id:
            vals = self.get_category_by_id(prestashop, prestashop_object_id)
            if vals:
                data_list.append(vals)
        elif import_category_date:
            data_list = self.filter_category_using_date(
                prestashop, import_category_date)
        else:
            data_list = self.get_category_all(prestashop)
        return data_list
  
class ExportPrestashopCategories(models.TransientModel):
    _inherit = ['export.categories']

    def action_prestashop_export_category(self):
        return self.export_button()

    def prestashop_create_category(self, prestashop, channel, record, initial_record_id, p_cat_id,
                meta_description='', meta_keywords='', with_product=False):
        cat_id = record.id
        cat_name = record.name
        cat_data = None
        try:
            cat_data = prestashop.get(
                'categories', options={'schema': 'blank'})
        except Exception as e:
            return [0, '\r\nCategory Id:%s ;Error in Creating blank schema for categories.Detail : %s' % (str(cat_id), str(e)), False]
        if cat_data:
            if type(cat_data['category']['name']['language']) == list:
                for i in range(len(cat_data['category']['name']['language'])):
                    cat_data['category']['name']['language'][i]['value'] = cat_name
                    cat_data['category']['link_rewrite']['language'][i]['value'] = channel._get_link_rewrite(
                        zip, cat_name)
                    cat_data['category']['meta_description']['language'][i]['value'] = meta_description
                    cat_data['category']['meta_keywords']['language'][i]['value'] = meta_keywords
                    cat_data['category']['meta_title']['language'][i]['value'] = record.name
            else:
                cat_data['category']['name']['language']['value'] = cat_name
                cat_data['category']['link_rewrite']['language']['value'] = channel._get_link_rewrite(
                    zip, cat_name)
                cat_data['category']['meta_description']['language']['value'] = meta_description
                cat_data['category']['meta_keywords']['language']['value'] = meta_keywords
                cat_data['category']['meta_title']['language']['value'] = record.name
            cat_data['category']['is_root_category'] = '0'
            cat_data['category']['id_parent'] = p_cat_id 
            cat_data['category']['active'] = '1'
            try:
                returnid = prestashop.add('categories', cat_data)
            except Exception as e:
                _logger.info('Category Data Not Exported::::::::::::: %r ::::::::::::::::', [
                             str(e), record.id, cat_data])
                if channel.debug == "enable":
                    raise UserError('Category Data Not Exported ==> %r ', [
                             str(e), record.id, cat_data])
                return False
            if record.id !=initial_record_id:
                self.env['channel.category.mappings'].create(
                        {
                            'channel_id': channel.id,
                            'ecom_store': channel.channel,
                            'leaf_category': True,
                            'category_name': record.id,
                            'odoo_category_id': record.id,
                            'store_category_id': returnid,
                            'operation': 'export',
                        })
            return returnid

    def prestashop_export_now(self, record, initial_record_id):
        result_list = [False, ""]
        with_product = self._context.get('with_product')
        channel = self._context.get('channel_id')
        prestashop = self._context.get('prestashop')
        cat_id = self.prestashop_sync_category(
            channel, prestashop, record, initial_record_id, with_product=with_product)
        if cat_id:
            remote_object = CreateRemoteObject(cat_id)
            result_list = [True, remote_object]
        return result_list

    def prestashop_sync_category(self, channel, prestashop, record, initial_record_id, with_product=False):
        p_cat_id = 1
        res = ""
        parent_id = record.parent_id
        if parent_id.id:
            is_parent_mapped = self.env["channel.category.mappings"].search([
                ("channel_id","=",channel.id),
                ("odoo_category_id","=",parent_id.id),
            ])
            if not is_parent_mapped:
                p_cat_id = self.with_context({
                    'with_product': with_product,
                    "channel_id": channel,
                    "prestashop": prestashop,
                }).prestashop_export_now(record.parent_id, initial_record_id)
                if p_cat_id[0]:
                    p_cat_id = p_cat_id[1].id
            else:
                p_cat_id = is_parent_mapped.store_category_id
        res = self.prestashop_create_category(
            prestashop, channel, record, initial_record_id, p_cat_id, with_product=with_product)
        return res


class CreateRemoteObject:

    def __init__(self, id):
        self.id = id
