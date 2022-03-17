""" This file is used for create the new functionality for configure
the schedulers by instance wise and also manage that functionality"""
import logging
from odoo import models, fields, api, _
from odoo.exceptions import Warning

_logger = logging.getLogger("Amazon Vendor Center")


class VendorCronConfiguration(models.TransientModel):
    """
        Create the new functionality for configure the schedulers by instance wise
    """
    _name = "vendor.cron.configuration"
    _description = "Amazon Vendor Central Cron Configuration"

    def _get_avc_instance(self):
        return self.env.context.get('amz_vendor_id', False)

    amazon_vendor_instance_id = fields.Many2one('amazon.vendor.instance', string='Vendor',
                                default=_get_avc_instance, help='Amazon Vendor Instance',
                                copy=False)
    amz_auto_import_po = fields.Boolean(string="Auto Import Purchase Orders?", default=False)
    amz_auto_import_po_next_execution = fields.Datetime('Auto Import PO Next Execution',
                                                        help='Next execution time')
    amz_auto_import_po_interval_number = fields.Integer('Auto Import PO Interval Number',
                                                        help="Repeat every x.")
    amz_auto_import_po_process_interval_type = fields.Selection([('hours', 'Hours'), ('days', 'Days')],
                                                                'Auto Import PO Process Interval Unit')
    amz_auto_import_po_user_id = fields.Many2one("res.users", string="Auto Import PO User",
                                                 default=lambda self: self.env.user)

    amz_auto_inv_and_cost_export = fields.Boolean(string="Auto Export Inventory and Cost Report?", default=False)
    amz_auto_inv_and_cost_export_next_execution = fields.Datetime('Auto Export Inv and Cost Report Next Execution',
                                                                  help='Next execution time')
    amz_auto_inv_and_cost_export_interval_number = fields.Integer('Auto Export Inv and Cost Report Interval Number',
                                                                  help="Repeat every x.")
    amz_auto_inv_and_cost_export_interval_type = fields.Selection([('hours', 'Hours'), ('days', 'Days')],
                                                                  'Auto Export Inv and Cost Report Interval Unit')
    amz_auto_inv_and_cost_export_user_id = fields.Many2one("res.users", string="Auto Export Inv and Cost Report User",
                                                           default=lambda self: self.env.user)
    amz_auto_asn_export = fields.Boolean(string="Auto Export Advance Shipment Notices?", default=False)
    amz_auto_asn_export_next_execution = fields.Datetime('Auto Export Advance Shipment Notices Next Execution',
                                                                  help='Next execution time')
    amz_auto_asn_export_interval_number = fields.Integer('Auto Export Advance Shipment Notices Interval Number',
                                                                  help="Repeat every x.")
    amz_auto_asn_export_interval_type = fields.Selection([('hours', 'Hours'), ('days', 'Days')],
                                                                  'Auto Export Advance Shipment Notices Interval Unit')
    amz_auto_asn_export_user_id = fields.Many2one("res.users", string="Auto Export Advance Shipment Notices User",
                                                           default=lambda self: self.env.user)
    amz_auto_invoices_export = fields.Boolean(string="Auto Export Invoices?", default=False)
    amz_auto_invoices_export_next_execution = fields.Datetime('Auto Export Invoices Next Execution',
                                                                  help='Next execution time')
    amz_auto_invoices_export_interval_number = fields.Integer('Auto Export Invoices Interval Number',
                                                                  help="Repeat every x.")
    amz_auto_invoices_export_interval_type = fields.Selection([('hours', 'Hours'), ('days', 'Days')],
                                                                  'Auto Export Invoices Interval Unit')
    amz_auto_invoices_export_user_id = fields.Many2one("res.users", string="Auto Export Invoices User",
                                                           default=lambda self: self.env.user)

    def save_vendor_cron_configurations(self):
        """
            used for, create the new crons by instance wise or update the existing crons
        """
        _logger.info("Scheduler Cron Configuration Process Started of an Instance: %s" % (self.amazon_vendor_instance_id.name))
        vals = {}
        self.setup_amz_vendor_auto_import_po_cron(self.amazon_vendor_instance_id)
        self.setup_amz_vendor_auto_inv_and_cost_export_cron(self.amazon_vendor_instance_id)
        self.setup_amz_vendor_auto_send_asn_using_cron(self.amazon_vendor_instance_id)
        self.setup_amz_vendor_auto_invoices_export_cron(self.amazon_vendor_instance_id)

        vals['amz_auto_import_po'] = self.amz_auto_import_po
        vals['amz_auto_inv_and_cost_export'] = self.amz_auto_inv_and_cost_export
        vals['amz_auto_asn_export'] = self.amz_auto_asn_export
        vals['amz_auto_invoices_export'] = self.amz_auto_invoices_export
        self.amazon_vendor_instance_id.write(vals)
        _logger.info("Scheduler Cron Configuration Process Ended of an Instance: %s" % (self.amazon_vendor_instance_id.name))

    def setup_amz_vendor_auto_import_po_cron(self, instance):
        """
            used for, create or update the import purchase order cron by instance wise.
            :param instance: amazon.vendor.instance()
        """
        if self.amz_auto_import_po:
            cron_exist = self.env.ref(
                'amazon_vendor_central_ept.ir_cron_amazon_import_purchase_order_vendor_%d' % (instance.id),
                raise_if_not_found=False)
            vals = {'active': True,
                    'interval_number': self.amz_auto_import_po_interval_number,
                    'interval_type': self.amz_auto_import_po_process_interval_type,
                    'nextcall': self.amz_auto_import_po_next_execution,
                    'user_id': self.amz_auto_import_po_user_id.id,
                    'code': "model.sync_amazon_po_from_cron({'amazon_vendor_instance_id':%d})" % (instance.id),
                    'avc_cron_id': instance.id}

            if cron_exist:
                cron_exist.write(vals)
            else:
                cron_exist = self.env.ref('amazon_vendor_central_ept.ir_cron_avc_edi_auto_import_po',
                                          raise_if_not_found=False)
                if not cron_exist:
                    raise Warning(_('Core settings of Amazon Vendor Central are deleted, '
                                    'Please upgrade Amazon Vendor Central module to get back this settings.'))

                name = 'Vendor Central - ' + instance.name + ' : Import purchase Orders'
                vals.update({'name': name})
                new_cron = cron_exist.copy(default=vals)
                self.env['ir.model.data'].create(
                    {'module': 'amazon_vendor_central_ept',
                     'name': 'ir_cron_amazon_import_purchase_order_vendor_%d' % (instance.id),
                     'model': 'ir.cron',
                     'res_id': new_cron.id,
                     'noupdate': True
                     })
        else:
            cron_exist = self.env.ref(
                'amazon_vendor_central_ept.ir_cron_amazon_import_purchase_order_vendor_%d' % (instance.id),
                raise_if_not_found=False)
            if cron_exist:
                cron_exist.write({'active': False})
        return True

    def setup_amz_vendor_auto_inv_and_cost_export_cron(self, instance):
        """
            used for, create or update the export inventory and cost report cron by instance wise.
            :param instance: amazon.vendor.instance()
        """
        if self.amz_auto_inv_and_cost_export:
            cron_exist = self.env.ref(
                'amazon_vendor_central_ept.ir_cron_amazon_export_inv_and_cost_report_vendor_%d' % (instance.id),
                raise_if_not_found=False)
            vals = {'active': True,
                    'interval_number': self.amz_auto_inv_and_cost_export_interval_number,
                    'interval_type': self.amz_auto_inv_and_cost_export_interval_type,
                    'nextcall': self.amz_auto_inv_and_cost_export_next_execution,
                    'user_id': self.amz_auto_inv_and_cost_export_user_id.id,
                    'code': "model.export_inventory_and_cost_from_cron({'amazon_vendor_instance_id':%d})" % (instance.id),
                    'avc_cron_id': instance.id}

            if cron_exist:
                cron_exist.write(vals)
            else:
                cron_exist = self.env.ref('amazon_vendor_central_ept.ir_cron_inventory_and_cost_export',
                                          raise_if_not_found=False)
                if not cron_exist:
                    raise Warning(_('Core settings of Amazon Vendor Central are deleted, '
                                    'Please upgrade Amazon Vendor Central module to get back this settings.'))

                name = 'Vendor Central - ' + instance.name + ' : Export Inventory and Cost Report'
                vals.update({'name': name})
                new_cron = cron_exist.copy(default=vals)
                self.env['ir.model.data'].create(
                    {'module': 'amazon_vendor_central_ept',
                     'name': 'ir_cron_amazon_export_inv_and_cost_report_vendor_%d' % (instance.id),
                     'model': 'ir.cron',
                     'res_id': new_cron.id,
                     'noupdate': True
                     })
        else:
            cron_exist = self.env.ref(
                'amazon_vendor_central_ept.ir_cron_amazon_export_inv_and_cost_report_vendor_%d' % (instance.id),
                raise_if_not_found=False)
            if cron_exist:
                cron_exist.write({'active': False})
        return True

    def setup_amz_vendor_auto_send_asn_using_cron(self, instance):
        """
            used for, create or update the export advance shipment notices cron by instance wise.
            :param instance: amazon.vendor.instance()
        """
        if self.amz_auto_asn_export:
            cron_exist = self.env.ref(
                'amazon_vendor_central_ept.ir_cron_advance_shipment_notice_export_%d' % (instance.id),
                raise_if_not_found=False)
            vals = {'active': True,
                    'interval_number': self.amz_auto_asn_export_interval_number,
                    'interval_type': self.amz_auto_asn_export_interval_type,
                    'nextcall': self.amz_auto_asn_export_next_execution,
                    'user_id': self.amz_auto_asn_export_user_id.id,
                    'code': "model.export_advance_shipment_notices_from_cron({'amazon_vendor_instance_id':%d})" % (instance.id),
                    'avc_cron_id': instance.id}

            if cron_exist:
                cron_exist.write(vals)
            else:
                cron_exist = self.env.ref('amazon_vendor_central_ept.ir_cron_advance_shipment_notice_export',
                                          raise_if_not_found=False)
                if not cron_exist:
                    raise Warning(_('Core settings of Amazon Vendor Central are deleted, '
                                    'Please upgrade Amazon Vendor Central module to get back this settings.'))

                name = 'Amazon Vendor Central - ' + instance.name + ' : Export Advance Shipment Notices'
                vals.update({'name': name})
                new_cron = cron_exist.copy(default=vals)
                self.env['ir.model.data'].create(
                    {'module': 'amazon_vendor_central_ept',
                     'name': 'ir_cron_advance_shipment_notice_export_%d' % (instance.id),
                     'model': 'ir.cron',
                     'res_id': new_cron.id,
                     'noupdate': True
                     })
        else:
            cron_exist = self.env.ref(
                'amazon_vendor_central_ept.ir_cron_advance_shipment_notice_export_%d' % (instance.id),
                raise_if_not_found=False)
            if cron_exist:
                cron_exist.write({'active': False})
        return True

    def setup_amz_vendor_auto_invoices_export_cron(self, instance):
        """
            used for, create or update the export invoices cron by instance wise.
            :param instance: amazon.vendor.instance()
        """
        if self.amz_auto_invoices_export:
            cron_exist = self.env.ref(
                'amazon_vendor_central_ept.ir_cron_invoices_export_%d' % (instance.id),
                raise_if_not_found=False)
            vals = {'active': True,
                    'interval_number': self.amz_auto_invoices_export_interval_number,
                    'interval_type': self.amz_auto_invoices_export_interval_type,
                    'nextcall': self.amz_auto_invoices_export_next_execution,
                    'user_id': self.amz_auto_invoices_export_user_id.id,
                    'code': "model.export_invoices_from_cron({'amazon_vendor_instance_id':%d})" % (instance.id),
                    'avc_cron_id': instance.id}

            if cron_exist:
                cron_exist.write(vals)
            else:
                cron_exist = self.env.ref('amazon_vendor_central_ept.ir_cron_invoices_export',
                                          raise_if_not_found=False)
                if not cron_exist:
                    raise Warning(_('Core settings of Amazon Vendor Central are deleted, '
                                    'Please upgrade Amazon Vendor Central module to get back this settings.'))

                name = 'Amazon Vendor Central - ' + instance.name + ' : Export Invoices'
                vals.update({'name': name})
                new_cron = cron_exist.copy(default=vals)
                self.env['ir.model.data'].create(
                    {'module': 'amazon_vendor_central_ept',
                     'name': 'ir_cron_invoices_export_%d' % (instance.id),
                     'model': 'ir.cron',
                     'res_id': new_cron.id,
                     'noupdate': True
                     })
        else:
            cron_exist = self.env.ref(
                'amazon_vendor_central_ept.ir_cron_invoices_export_%d' % (instance.id),
                raise_if_not_found=False)
            if cron_exist:
                cron_exist.write({'active': False})
        return True

    @api.onchange("amazon_vendor_instance_id")
    def onchange_amazon_vendor_instance_id(self):
        """
            Usage: Used for searching the existing crons for update the existing crons
        """
        self.update_amz_import_po_via_cron_field(self.amazon_vendor_instance_id)
        self.update_amz_export_inv_cost_report_via_cron_field(self.amazon_vendor_instance_id)
        self.update_amz_export_asn_via_cron_field(self.amazon_vendor_instance_id)
        self.update_amz_export_invoices_via_cron_field(self.amazon_vendor_instance_id)

    def update_amz_import_po_via_cron_field(self, instance):
        """
            Usage: Search the import po cron based on instance(amz_vendor) and update that cron.
            :param instance: amazon.vendor.instance()
        """
        try:
            amz_import_po_cron_exist = instance and self.env.ref(
                'amazon_vendor_central_ept.ir_cron_amazon_import_purchase_order_vendor_%d' % (instance.id))
        except Exception as err:
            _logger.info(err)
            amz_import_po_cron_exist = False
        if amz_import_po_cron_exist:
            self.amz_auto_import_po = amz_import_po_cron_exist.active or False
            self.amz_auto_import_po_interval_number = amz_import_po_cron_exist.interval_number or False
            self.amz_auto_import_po_process_interval_type = amz_import_po_cron_exist.interval_type or False
            self.amz_auto_import_po_next_execution = amz_import_po_cron_exist.nextcall or False
            self.amz_auto_import_po_user_id = amz_import_po_cron_exist.user_id.id or False

    def update_amz_export_inv_cost_report_via_cron_field(self, instance):
        """
            Usage: Search the export inventory and cost report cron based on instance(amz_vendor)
             and update that cron.
            :param instance: amazon.vendor.instance()
        """
        try:
            amz_inv_and_cost_export_exist = instance and self.env.ref(
                'amazon_vendor_central_ept.ir_cron_amazon_export_inv_and_cost_report_vendor_%d' % (instance.id))
        except Exception as err:
            _logger.info(err)
            amz_inv_and_cost_export_exist = False
        if amz_inv_and_cost_export_exist:
            self.amz_auto_inv_and_cost_export = amz_inv_and_cost_export_exist.active or False
            self.amz_auto_inv_and_cost_export_interval_number = amz_inv_and_cost_export_exist.interval_number or False
            self.amz_auto_inv_and_cost_export_interval_type = amz_inv_and_cost_export_exist.interval_type or False
            self.amz_auto_inv_and_cost_export_next_execution = amz_inv_and_cost_export_exist.nextcall or False
            self.amz_auto_inv_and_cost_export_user_id = amz_inv_and_cost_export_exist.user_id.id or False

    def update_amz_export_asn_via_cron_field(self, instance):
        """
            Usage: Search the export inventory and cost report cron based on instance(amz_vendor)
             and update that cron.
            :param instance: amazon.vendor.instance()
        """
        try:
            amz_asn_export_cron = instance and self.env.ref(
                'amazon_vendor_central_ept.ir_cron_advance_shipment_notice_export_%d' % (instance.id))
        except Exception as err:
            _logger.info(err)
            amz_asn_export_cron = False
        if amz_asn_export_cron:
            self.amz_auto_asn_export = amz_asn_export_cron.active or False
            self.amz_auto_asn_export_interval_number = amz_asn_export_cron.interval_number or False
            self.amz_auto_asn_export_interval_type = amz_asn_export_cron.interval_type or False
            self.amz_auto_asn_export_next_execution = amz_asn_export_cron.nextcall or False
            self.amz_auto_asn_export_user_id = amz_asn_export_cron.user_id.id or False

    def update_amz_export_invoices_via_cron_field(self, instance):
        """
            Usage: Search the export inventory and cost report cron based on instance(amz_vendor)
             and update that cron.
            :param instance: amazon.vendor.instance()
        """
        try:
            amz_invoices_export_cron = instance and self.env.ref(
                'amazon_vendor_central_ept.ir_cron_invoices_export_%d' % (instance.id))
        except Exception as err:
            _logger.info(err)
            amz_invoices_export_cron = False
        if amz_invoices_export_cron:
            self.amz_auto_invoices_export = amz_invoices_export_cron.active or False
            self.amz_auto_invoices_export_interval_number = amz_invoices_export_cron.interval_number or False
            self.amz_auto_invoices_export_interval_type = amz_invoices_export_cron.interval_type or False
            self.amz_auto_invoices_export_next_execution = amz_invoices_export_cron.nextcall or False
            self.amz_auto_invoices_export_user_id = amz_invoices_export_cron.user_id.id or False
