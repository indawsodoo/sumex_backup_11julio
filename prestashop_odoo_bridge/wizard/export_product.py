# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, _
from odoo.addons.prestashop_odoo_bridge.models.prestapi import PrestaShopWebService,PrestaShopWebServiceDict,PrestaShopWebServiceError,PrestaShopAuthenticationError
from odoo.exceptions import  UserError,RedirectWarning, ValidationError ,Warning
from odoo.addons.odoo_multi_channel_sale.tools import extract_list as EL
from odoo.addons.odoo_multi_channel_sale.tools import ensure_string as ES
from odoo.addons.odoo_multi_channel_sale.tools import JoinList as JL
from odoo.addons.odoo_multi_channel_sale.tools import MapId
import logging
_logger = logging.getLogger(__name__)

class ExportProductsPrestashop(models.TransientModel):
    _inherit = ['export.products']

    def action_prestashop_export_product(self):
        active_ids = self._context.get('active_ids')
        prod_env = self.env['product.product']
        temp_ids = [prod_env.browse(
            active_id).product_tmpl_id.id for active_id in active_ids]
        channel_id = self.channel_id.id
        return self.env['export.templates'].create({
            "channel_id": channel_id,
            "operation": "export" if self.operation == "export" else "update",
        }).with_context({
            "active_ids": temp_ids,
            "active_model": "product.template",
        }).action_prestashop_export_template()


class ExportPrestashopProducts(models.TransientModel):
    _inherit = ['export.templates']

    def prestashop_export_now(self, record):
        if record.type == "service":
            return [False, ""]
        channel_id = self._context.get('channel_id')
        variant_list = []
        prestashop = self._context.get('prestashop')
        product_bs = prestashop.get('products', options={'schema': 'blank'})
        response = self.prestashop_export_template(
            prestashop, channel_id, product_bs, record)
        if response[0]:
            ps_template_id = response[1]
        else:
            return response
        if record.attribute_line_ids:
            for variant_id in record.product_variant_ids:
                response = self.prestashop_export_product(
                    prestashop, channel_id, variant_id, record, ps_template_id)
                if response[0]:
                    variant_list.append(response[1])
            if len(variant_list):
                remote_object = CreateRemoteTemplateObject(
                    ps_template_id, variant_list)
                return [True, remote_object]
        else:
            remote_object = CreateRemoteTemplateObject(
                ps_template_id, [ps_template_id])
            return [True, remote_object]

    def prestashop_update_now(self, record, remote_id):
        channel_id = self._context.get('channel_id')
        prestashop = self._context.get('prestashop')
        product_schema = prestashop.get(
            'products', remote_id, options={'schema': 'blank'})
        response = self.prestashop_update_template(
            prestashop, channel_id, product_schema, record, remote_id)
        return response

    def _get_store_categ_id(self, prestashop, erp_id):
        mapping_obj = self.env['channel.category.mappings']
        domain = [('odoo_category_id', '=', erp_id)]
        check = self.channel_id._match_mapping(
            mapping_obj,
            domain,
            limit=1
        )
        if not check:
            vals = dict(
                channel_id=self.channel_id.id,
                operation='export',
                category_ids=[(6,0,[erp_id])]
            )
            obj = self.env['export.prestashop.categories'].create(vals)
            cat_id = obj.with_context({
                'with_product': True,
                "channel_id": self.channel_id,
                "prestashop": prestashop,
            }).prestashop_export_now(erp_id, erp_id.id)
            if cat_id[0]:
                return cat_id[1].id
            else:
                _logger.info(
                    "Category cannot be exported to prestashop with id %r", erp_id.id)
                return False
        return check.store_category_id

    def prestashop_update_template(self, prestashop, channel_id, product_bs, template_record, remote_id):
        # attribute_line_ids = template_record.attribute_line_ids
        # if attribute_line_ids:
        #     for attribute_line_id in attribute_line_ids:
        #         attribute_id = attribute_line_id.attribute_id
        #         res = self.env['export.prestashop.attribute'].create({
        #             "channel_id":channel_id,
        #             "operation":'update',
        #             }).with_context({
        #                 "channel_id":channel_id,
        #                 "prestashop":prestashop,
        #             }).prestashop_update_now(attribute_id)
        #         _logger.info('response from product option =========> %r', res)
        #         if not res:
        #             raise ValidationError('Product Attributes cannot be exported to Prestashop.')
        cost = template_record.standard_price
        default_code = template_record.default_code or ''
        erp_category_id = template_record.categ_id
        presta_default_categ_id = self._get_store_categ_id(
            prestashop, erp_category_id)
        ps_extra_categ = []
        extra_categories = self.env['extra.categories'].search([
            ('instance_id', '=', channel_id.id),
            ('product_id', '=', template_record.id)])
        extra_categories_set = set()
        if extra_categories:
            for extra_category in extra_categories:
                for categ in extra_category.extra_category_ids:
                    cat_id = self._get_store_categ_id(prestashop, categ)
                    if cat_id not in extra_categories_set:
                        extra_categories_set.add(cat_id)
                        ps_extra_categ.append({'id': str(cat_id)})
        product_bs['product'].update({
            'price': str(round(template_record.with_context(pricelist=channel_id.pricelist_name.id).price, 2)),
            'active': '1',
            'weight': str(template_record.weight) or '',
            'redirect_type': '404',
            'minimal_quantity': '1',
            'available_for_order': '1',
            'show_price': '1',
            'depth': str(template_record.length) or '',
            'width': str(template_record.width) or '',
            'height': str(template_record.height) or '',
            'state': '1',
            'ean13': template_record.barcode or '',
            'reference': default_code or '',
            'out_of_stock': '2',
            'condition': 'new',
            'id_category_default': str(presta_default_categ_id)
        })
        if cost:
            product_bs['product']['wholesale_price'] = str(round(cost, 3))
        if type(product_bs['product']['name']['language']) == list:
            for i in range(len(product_bs['product']['name']['language'])):
                product_bs['product']['name']['language'][i]['value'] = template_record.name
                product_bs['product']['link_rewrite']['language'][i]['value'] = channel_id._get_link_rewrite(
                    '', template_record.name)
                product_bs['product']['description']['language'][i]['value'] = template_record.description
                product_bs['product']['description_short']['language'][i]['value'] = template_record.description_sale
        else:
            product_bs['product']['name']['language']['value'] = template_record.name
            product_bs['product']['link_rewrite']['language']['value'] = channel_id._get_link_rewrite(
                '', template_record.name)
            product_bs['product']['description']['language']['value'] = template_record.description
            product_bs['product']['description_short']['language']['value'] = template_record.description_sale
        if 'category' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['category']['id'] = str(
                presta_default_categ_id)
        if 'categories' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['categories']['id'] = str(
                presta_default_categ_id)
        pop_attr = product_bs['product']['associations'].pop(
            'combinations', None)
        a1 = product_bs['product']['associations'].pop('images', None)
        a2 = product_bs['product'].pop('position_in_category', None)
        a3 = product_bs['product'].pop('manufacturer_name', None)
        a4 = product_bs['product'].pop('quantity', None)
        if ps_extra_categ:
            if 'category' in product_bs['product']['associations']['categories']:
                a3 = product_bs['product']['associations']['categories']['category'] = ps_extra_categ
            if 'categories' in product_bs['product']['associations']['categories']:
                a3 = product_bs['product']['associations']['categories']['categories'] = ps_extra_categ
        try:
            returnid = prestashop.edit(
                'products', remote_id, product_bs)
            _logger.info("Product Template successfully updated to Prestashop with id: %r",
                         remote_id)
        except Exception as e:
            if channel_id.debug == "enable":
                raise UserError( ' Error in updating Product Template(ID: %s).%s' % (str(presta_default_categ_id), str(e)))
            return [False, ' Error in updating Product Template(ID: %s).%s' % (str(presta_default_categ_id), str(e))]
        return [True, remote_id]

    def prestashop_export_template(self, prestashop, channel_id, product_bs, template_record):
        attribute_line_ids = template_record.attribute_line_ids
        if attribute_line_ids:
            res = self.env['export.prestashop.attribute'].create({
                "channel_id": channel_id.id,
                "operation": "export",
            })
            for attribute_line_id in attribute_line_ids:
                attribute_id = attribute_line_id.attribute_id
                result = res.with_context({
                    "channel_id": channel_id,
                    "prestashop": prestashop,
                }).export_now(attribute_id)
                if not result:
                    raise ValidationError(
                        'Product Attributes cannot be exported to Prestashop.')
        cost = template_record.standard_price
        default_code = template_record.default_code or ''
        erp_category_id = template_record.categ_id
        presta_default_categ_id = self._get_store_categ_id(
            prestashop, erp_category_id)
        ps_extra_categ = []
        extra_categories = self.env['extra.categories'].search([
            ('instance_id', '=', channel_id.id),
            ('product_id', '=', template_record.id)])
        extra_categories_set = set()
        if extra_categories:
            for extra_category in extra_categories:
                for categ in extra_category.extra_category_ids:
                    cat_id = self._get_store_categ_id(prestashop, categ)
                    if cat_id not in extra_categories_set:
                        extra_categories_set.add(cat_id)
                        ps_extra_categ.append({'id': str(cat_id)})

        product_bs['product'].update({
            'price': str(round(template_record.with_context(pricelist=channel_id.pricelist_name.id).price, 2)),
            'active': '1',
            'weight': str(template_record.weight) or '',
            'redirect_type': '404',
            'minimal_quantity': '1',
            'available_for_order': '1',
            'show_price': '1',
            'depth': str(template_record.length) or '',
            'width': str(template_record.width) or '',
            'height': str(template_record.height) or '',
            'state': '1',
            'ean13': template_record.barcode or '',
            'reference': default_code or '',
            'out_of_stock': '2',
            'condition': 'new',
            'id_category_default': str(presta_default_categ_id)
        })
        if cost:
            product_bs['product']['wholesale_price'] = str(round(cost, 3))
        if type(product_bs['product']['name']['language']) == list:
            for i in range(len(product_bs['product']['name']['language'])):
                product_bs['product']['name']['language'][i]['value'] = template_record.name
                product_bs['product']['link_rewrite']['language'][i]['value'] = channel_id._get_link_rewrite(
                    '', template_record.name)
                product_bs['product']['description']['language'][i]['value'] = template_record.description
                product_bs['product']['description_short']['language'][i]['value'] = template_record.description_sale
        else:
            product_bs['product']['name']['language']['value'] = template_record.name
            product_bs['product']['link_rewrite']['language']['value'] = channel_id._get_link_rewrite(
                '', template_record.name)
            product_bs['product']['description']['language']['value'] = template_record.description
            product_bs['product']['description_short']['language']['value'] = template_record.description_sale
        if 'category' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['category']['id'] = str(
                presta_default_categ_id)
        if 'categories' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['categories']['id'] = str(
                presta_default_categ_id)
        pop_attr = product_bs['product']['associations'].pop(
            'combinations', None)
        a1 = product_bs['product']['associations'].pop('images', None)
        a2 = product_bs['product'].pop('position_in_category', None)
        a3 = product_bs['product'].pop('manufacturer_name', None)

        if ps_extra_categ:
            if 'category' in product_bs['product']['associations']['categories']:
                a3 = product_bs['product']['associations']['categories']['category'] = ps_extra_categ
            if 'categories' in product_bs['product']['associations']['categories']:
                a3 = product_bs['product']['associations']['categories']['categories'] = ps_extra_categ
        try:
            returnid = prestashop.add('products', product_bs)
            product_record = self.env["product.product"].search([("product_tmpl_id","=",template_record.id)])
            if len(product_record) == 1:
                product_data = prestashop.get("products",returnid)
                stock_id = product_data.get("product").get(
                    "associations",{}).get("stock_availables",{}).get("stock_available",{}).get("id")
                response = self.prestashop_export_product(
                    prestashop, channel_id,product_record,template_record , returnid,stock_id = stock_id)
            _logger.info("Product Template successfully exported to Prestashop with id: %r",
                         returnid)
        except Exception as e:
            _logger.info("Error in creating Product Template(ID: %s).%s" %
                         (str(presta_default_categ_id), str(e)))
            if channel_id.debug == "enable":
                raise UserError("Error in creating Product Template(ID: %s).%s" %
                         (str(presta_default_categ_id), str(e)))
            return [False, ""]
        if returnid:
            return [True, returnid]

    def prestashop_export_product(self, prestashop, channel_id, product_record, template_record, ps_template_id,stock_id = None):
        if template_record.attribute_line_ids:
            default_attr = "0"
            response_combination = self.create_combination(
                prestashop, channel_id, ps_template_id, product_record, default_attr)
            return response_combination
        else:
            response_update = self.create_normal_product(
                prestashop, channel_id, template_record, product_record, ps_template_id,stock_id)
            return response_update

    def create_combination(self, prestashop, channel_id, presta_main_product_id,
                           product_record, default_attr):
        presta_dim_list = []
        combination_bs = prestashop.get(
            'combinations', options={'schema': 'blank'})
        qty = product_record._product_available()
        image_id = False
        quantity = qty[product_record.id]['qty_available'] - \
            qty[product_record.id]['outgoing_qty']
        if type(quantity) == str:
            quantity = quantity.split('.')[0]
        if type(quantity) == float:
            quantity = quantity.as_integer_ratio()[0]
        image = product_record.image_1920
        if image:
            image_id = self.create_images(
                prestashop, image, presta_main_product_id)
        price_extra = round(float(product_record.with_context(pricelist=channel_id.pricelist_name.id).lst_price) -
                            float(product_record.with_context(pricelist=channel_id.pricelist_name.id).list_price), 2)
        ean13 = product_record.barcode or ''
        default_code = product_record.default_code or ''
        weight = product_record.weight
        attribute_value_ids = product_record.product_template_attribute_value_ids
        attrib_value_mapped_env = self.env['channel.attribute.value.mappings']
        for attribute_value_id in attribute_value_ids:
            value_id = attribute_value_id.product_attribute_value_id.id
            is_attrib_value_mapped = attrib_value_mapped_env.search([
                ("channel_id", '=', channel_id.id),
                ("odoo_attribute_value_id", '=', value_id)
            ])
            presta_dim_list.append(
                {"id": is_attrib_value_mapped.store_attribute_value_id})
        if presta_dim_list:
            try :
                data = prestashop.get('combinations',options={'schema': 'blank'})
            except Exception as e:
                _logger.info("Error:- %r",str(e))
                if channel_id.debug == "enable":
                    raise UserError("Error:- %r",str(e))
            combination_bs['combination']['associations']['product_option_values']['product_option_values'] = presta_dim_list
            combination_bs['combination'].update({
                'ean13': ean13,
                'weight': str(weight),
                'reference': default_code,
                'price': str(price_extra),
                'quantity': quantity,
                'default_on': default_attr,
                'id_product': str(presta_main_product_id),
                'minimal_quantity': '1',
            })
        try:
            returnid = prestashop.add('combinations', combination_bs)
        except Exception as e:
            _logger.info('Error in creating Variant(ID: %s).%s' %
                         (str(product_record.id), str(e)))
            if channel_id.debug == "enable":
                raise UserError('Error in creating Variant(ID: %s).%s' % (
                    str(product_record.id), str(e)))
           
        if returnid:
            temp_data = False
            data = {'combination': {
                'associations': {'images': {'image': {'id': str(image_id)}}},
                'minimal_quantity': '1',
                'id_product': str(presta_main_product_id),
                'id': str(returnid),
                'quantity': quantity}}
            try:
                prestashop.edit('combinations', returnid, data)
            except Exception as e:
                _logger.info('...... Error combination image:%r ... ', e)
                if channel_id.debug == "enable":
                    raise UserError('...... Error combination image:%r ... ', e)
            if default_attr:
                try:
                    temp_data = prestashop.get('products', presta_main_product_id)
                except Exception as e:
                    msg = ' Error in Updating default variant(ID: %s).%s' % (str(presta_main_product_id), str(e))
                    _logger.info('..Error: %r ////...', msg)
                if temp_data:
                    temp_data['product']['id_default_combination'] = returnid
                    a1 = temp_data['product'].pop('position_in_category', None)
                    a2 = temp_data['product'].pop('manufacturer_name', None)
                    a3 = temp_data['product'].pop('quantity', None)
                    a4 = temp_data['product'].pop('type', None)
                    try:
                        prestashop.edit('products', presta_main_product_id, temp_data)
                    except Exception as e:
                        _logger.info(
                            '----------------%r----------------', str(e))
                        if channel_id.debug == "enable":
                            raise UserError('...... Error combination update:%r ... ', e)
                        
            pid = int(returnid)
            if float(quantity) > 0.0:
                get = self.prestashop_update_quantity(
                    prestashop, presta_main_product_id, quantity, None, pid)
            return [True, pid]

    def create_normal_product(self, prestashop, channel_id, erp_template_id, 
                product_record, prest_main_product_id, stock_id):
        erp_category_id = product_record.categ_id.id
        default_code = product_record.default_code or ''
        presta_default_categ_id = self._get_store_categ_id(erp_category_id)
        if prestashop:
            add_data = prestashop.get('products', prest_main_product_id)
        if add_data:
            add_data['product'].update({
                'price': str(round(product_record.with_context(pricelist=channel_id.pricelist_name.id).price, 2)),
                'active': '1',
                'redirect_type': '404',
                'minimal_quantity': '1',
                'available_for_order': '1',
                'show_price': '1',
                'state':'1',
                'out_of_stock': '2',
                'default_on': '1',
                'condition': 'new',
                'reference': default_code,
                'id_category_default': presta_default_categ_id
            })
            a1 = add_data['product'].pop('position_in_category', None)
            a2 = add_data['product'].pop('manufacturer_name', None)
            a3 = add_data['product'].pop('quantity', None)
            a4 = add_data['product'].pop('type', None)
            try:
                returnid = prestashop.edit(
                    'products', prest_main_product_id, add_data)
            except Exception as e:
                return [0, ' Error in creating Product(ID: %s).%s' % (str(erp_product_id), str(e))]
            if product_record.image_1920:
                get = self.create_images(
                    prestashop, product_record.image_1920, prest_main_product_id)
            qty = product_record._product_available()
            quantity = qty[product_record.id]['qty_available'] - qty[product_record.id]['outgoing_qty']
            if type(quantity) == str:
                quantity = quantity.split('.')[0]
            if type(quantity) == float:
                quantity = quantity.as_integer_ratio()[0]
            if float(quantity) > 0.0:
                get = self.prestashop_update_quantity(
                    prestashop, prest_main_product_id, quantity, stock_id)
            return [True, prest_main_product_id]

    @api.model
    def create_images(self, prestashop, image_data, resource_id, image_name=None, resource='images/products'):
        if image_name == None:
            image_name = 'op' + str(resource_id) + '.png'
        try:
            returnid = prestashop.add(
                str(resource) + '/' + str(resource_id), image_data, image_name)
            return returnid
        except Exception as e:
            return False

    def prestashop_update_quantity(self, prestashop, pid, quantity, stock_id=None, attribute_id=None):
        if stock_id:
            stock_data = {}
            try:
                stock_data = prestashop.get('stock_availables', stock_id)
            except Exception as e:
                _logger.info(
                    "Error in Updating Quantity,can`t get stock_available data.")
            if type(quantity) == str:
                quantity = quantity.split('.')[0]
            if type(quantity) == float:
                quantity = quantity.as_integer_ratio()[0]
            if stock_data.get("stock_available"):
                stock_data['stock_available']['quantity'] = quantity
            try:
                up = prestashop.edit('stock_availables', stock_id, stock_data)
                return True
            except Exception as e:
                _logger.info(
                    "Error in Updating Quantity,Unknown Error.%s" % str(e))
        elif attribute_id:
            stock_search = {}
            try:
                stock_search = prestashop.get('stock_availables',
                                              options={'filter[id_product]': pid, 'filter[id_product_attribute]': attribute_id})
            except Exception as e:
                _logger.info(
                    "Error :- ----------------> Unable to search given stock id")
            if type(stock_search.get("stock_availables",False)) == dict:
                stock_id = stock_search['stock_availables']['stock_available']['attrs']['id']
                try:
                    stock_data = prestashop.get('stock_availables', stock_id)
                except Exception as e:
                    _logger.info(
                        "Error :- ----------------> Error in Updating Quantity,can`t get stock_available data.")
                if type(quantity) == str:
                    quantity = quantity.split('.')[0]
                if type(quantity) == float:
                    quantity = int(quantity)
                stock_data['stock_available']['quantity'] = int(quantity)
                try:
                    up = prestashop.edit(
                        'stock_availables', stock_id, stock_data)
                except Exception as e:
                    pass
                _logger.info('Stock Successfully exported to Prestashop.')
                return True
            else:
                _logger.info(' No stock`s entry found in prestashop for given combination (Product id:%s ; Attribute id:%s)' % (
                    str(pid), str(attribute_id)))
        else:
            product_data = {}
            try:
                product_data = prestashop.get('products', pid)
            except Exception as e:
                _logger.info(
                    "Error in Updating Quantity,can`t get product data.")
            product_data = product_data.get("product")
            if product_data:
                stock_available = product_data.get("associations",{}).get("stock_availables")
                if stock_available:
                    stock_id = stock_available.get("stock_available").get("id")
                    stock_data = {}
                    try:
                        stock_data = prestashop.get('stock_availables', stock_id)
                    except Exception as e:
                        _logger.info(
                            "Error in Updating Quantity,can`t get stock_available data.")
                    if type(quantity) == str:
                        quantity = quantity.split('.')[0]
                    if type(quantity) == float:
                        quantity = quantity.as_integer_ratio()[0]
                    if stock_data.get("stock_available"):
                        stock_data['stock_available']['quantity'] = quantity
                    try:
                        up = prestashop.edit('stock_availables', stock_id, stock_data)
                        return True
                    except Exception as e:
                        _logger.info(
                            "Error in Updating Quantity,Unknown Error.%s" % str(e))

class CreateRemoteTemplateObject:

    def __init__(self, product_template_id, product_variant_list):
        self.id = product_template_id
        self.variants = (CreateRemoteVariantObject(product_variant_id)
                         for product_variant_id in product_variant_list)


class CreateRemoteVariantObject:

    def __init__(self, product_variant_id):
        self.id = product_variant_id
