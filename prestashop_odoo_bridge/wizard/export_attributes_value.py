# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

from odoo.addons.prestashop_odoo_bridge.models.prestapi import PrestaShopWebService,PrestaShopWebServiceDict
_logger = logging.getLogger(__name__)


class ExportPrestashopAttribute(models.TransientModel):
    _inherit = ['export.operation']
    _name = "export.prestashop.attribute"
    _description = "Export Prestashop Attribute"


    @api.model
    def export_now(self, record):
        prestashop = self._context.get('prestashop')
        channel_id = self._context.get('channel_id')
        add_data, add_value = False, False
        attribute_value_list = []
        error_message = ''
        try:
            add_data = prestashop.get(
                'product_options', options={'schema': 'blank'})
        except Exception as e:
            _logger.info("%r",str(e))
            if channel_id.debug == "enable":
                raise UserError(_('Error %s') % str(e))
        try:
            add_value = prestashop.get(
                'product_option_values', options={'schema': 'blank'})
        except Exception as e:
            _logger.info("%r",str(e))
            if channel_id.debug == "enable":
                raise UserError(_('Error %s') % str(e))
        if prestashop and add_data and add_value:
            attribute_id = record.id
            mapping_obj = self.env['channel.attribute.mappings']
            is_mapped = mapping_obj.search([
                ('channel_id', '=', channel_id.id),
                ('odoo_attribute_id', '=', attribute_id)
            ])
            if not is_mapped:
                name = record.name
                create_dim_type = self.create_dimension_type(prestashop,
                                                             channel_id, add_data, record, name)
                if create_dim_type[0] == 0:
                    error_message = error_message + create_dim_type[1]
                else:
                    presta_id = create_dim_type[0]
                    for value_id in record.value_ids:
                        attrib_value_map = self.env['channel.attribute.value.mappings'].search([
                            ('channel_id', '=', self.channel_id.id),
                            ('odoo_attribute_value_id', '=', value_id.id)])
                        name = self.env['product.attribute.value'].browse(
                            value_id.id).name
                        if not attrib_value_map:
                            create_dim_opt = self.create_dimension_option(prestashop, channel_id,
                                                                          add_value, presta_id, value_id, name)
                            if create_dim_opt[0] == 0:
                                error_message = error_message + \
                                    create_dim_opt[1]
                                return False
                            attribute_value_list.append(value_id)
                    error_message += " Dimension(%s) and their value(%r) has been created."\
                        % (record, attribute_value_list)
                    _logger.info('%r', error_message)
                if not len(attribute_value_list):
                    error_message = "No new Dimension(s) found !!!"
                    _logger.info('%r', error_message)
                    return False
            return True

    def create_dimension_type(self, prestashop, channel_id, add_data, erp_dim_type_id, name):
        if add_data:
            add_data['product_option'].update({
                                        'group_type': 'select',
                                        'position':'0'
                                    })
            if type(add_data['product_option']['name']['language']) == list:
                for i in range(len(add_data['product_option']['name']['language'])):
                    add_data['product_option']['name']['language'][i]['value'] = name
                    add_data['product_option']['public_name']['language'][i]['value'] = name
            else:
                add_data['product_option']['name']['language']['value'] = name
                add_data['product_option']['public_name']['language']['value'] = name
            try:
                returnid = prestashop.add('product_options', add_data)
            except Exception as e:
                if channel_id.debug == "enable":
                    raise UserError("Error in creating Dimension Type (ID: %s).%s"%(str(erp_dim_type_id),str(e)))
                return [0, ' Error in creating Dimension Type(ID: %s).%s' % (str(erp_dim_type_id), str(e))]
            if returnid:
                pid = returnid
                mapping_id = channel_id.create_attribute_mapping(
                    erp_dim_type_id, pid)
                return [pid, '']
    
    def update_dimension_type(self, prestashop, presta_id, name):
        update_data = dict()
        try:
            update_data = prestashop.get('product_options', presta_id)
        except Exception as e:
            return [0,'Error Getting Dimension Type(ID: %s'%(str(presta_id))]
        if update_data:
            if type(update_data['product_option']['name']['language']) == list:
                for i in range(len(update_data['product_option']['name']['language'])):
                    update_data['product_option']['name']['language'][i]['value'] = name
                    update_data['product_option']['public_name']['language'][i]['value'] = name
            else:
                update_data['product_option']['name']['language']['value'] = name
                update_data['product_option']['public_name']['language']['value'] = name
            try:
                returnid = prestashop.edit('product_options', presta_id, update_data)
            except Exception as e:
                return [0, ' Error in Updating Dimension Type(ID: %s).%s'%(str(presta_id), str(e))]
            if returnid:
                pid = returnid
                # mapping_id = self.channel_id.create_attribute_mapping(erp_dim_type_id, pid)
                return [pid, 'Updated Dimension Type(ID: %s'%(presta_id)]

    def create_dimension_option(self, prestashop, channel_id, add_value, presta_attr_id,
                                erp_dim_opt_id, name):
        if add_value:
            add_value['product_option_value'].update({
                                        'id_attribute_group': presta_attr_id,
                                        'position':'0'
                                    })
            if type(add_value['product_option_value']['name']['language']) == list:
                for i in range(len(add_value['product_option_value']['name']['language'])):
                    add_value['product_option_value']['name']['language'][i]['value'] = name
            else:
                add_value['product_option_value']['name']['language']['value'] = name
            try:
                returnid = prestashop.add('product_option_values', add_value)
            except Exception as e:
                if self.channel_id.debug == "enable":
                    raise UserError('Error creating Dimension Option(ID: %s.%s' % (str(perp_dim_opt_idresta_id),str(e)))
                return [0, ' Error in creating Dimension Option(ID: %s).%s' % (str(erp_dim_opt_id.id), str(e))]
            if returnid:
                pid = returnid
                mapping_id = channel_id.create_attribute_value_mapping(
                    erp_dim_opt_id, pid)
                return [pid, '']

    def update_dimension_option(self, prestashop, prestshop_atrib_val_id, name):
        attibute_option = False
        try:
            attibute_option = prestashop.get("product_option_values", prestshop_atrib_val_id)
        except Exception as e:
            return [0, 'Error in Getting Dimension Option(ID: %s).%s'%(str(prestshop_atrib_val_id), str(e))]

        if attibute_option:
            # add_value['product_option_value'].update({
            #                             'id_attribute_group': presta_attr_id,
            #                             'position':'0'
            #                         })
            if type(attibute_option['product_option_value']['name']['language']) == list:
                for i in range(len(attibute_option['product_option_value']['name']['language'])):
                    attibute_option['product_option_value']['name']['language'][i]['value'] = name
            else:
                attibute_option['product_option_value']['name']['language']['value'] = name
            try:
                returnid = prestashop.edit('product_option_values', prestshop_atrib_val_id ,attibute_option)
            except Exception as e:
                return [0, ' Error in updating Dimension Option(ID: %s).%s'%(str(prestshop_atrib_val_id), str(e))]
            if returnid:
                pid = returnid
                # mapping_id = self.channel_id.create_attribute_value_mapping(erp_dim_opt_id, pid)
                return [pid, '']
