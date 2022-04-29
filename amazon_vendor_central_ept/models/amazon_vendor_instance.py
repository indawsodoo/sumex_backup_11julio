""" This file used for manage the functionality of amazon vendor instance."""
import logging
import time
from io import StringIO
from tempfile import NamedTemporaryFile
from odoo import models, fields, _
from odoo.exceptions import UserError, Warning
from odoo.addons.ftp_connector_ept.models.sftp_interface import sftp_interface

_logger = logging.getLogger("Amazon Vendor Center")


class AmazonVendorInstance(models.Model):
    """
        Usage: Manage the functionality of Amazon Vendor Instance.
    """
    _name = 'amazon.vendor.instance'
    _description = 'Amazon Vendor Instance'

    name = fields.Char(string="Vendor Name", help="Specify the Unique Name of the Vendor")
    country_id = fields.Many2one(comodel_name='res.country', string="Country",
                                 help="The Order Requisitions are creates based on below selected country")
    company_id = fields.Many2one(comodel_name='res.company', string='Vendor Company',
                                 default=lambda self: self.env.company,
                                 help="The Order Requisitions are creates based on below selected company")
    journal_id = fields.Many2one(comodel_name='account.journal', string='Account Journal',
                                 help='Invoice is created in selected Journal')
    is_production_environment = fields.Boolean("Production Environment", default=False,
                                               help="This will identifying the instance is used for "
                                                    "test or production environment")
    pricelist_id = fields.Many2one(comodel_name='product.pricelist', string='Pricelist',
                                   help="List of prices of different products for customers and avc_suppliers")
    supplier_id = fields.Char(string="Supplier Id",
                              help="Amazon Supplier Id available in Global Settings -> Message Format -> "
                                   "Message Format Identifiers -> Your identifiers of Vendor Central Portal")
    order_dispatch_lead_time = fields.Integer(string="Order Lead Time", default=1,
                                              help="The average delay in days between the Routing Request "
                                                   "send and ready for order shipment.")
    avc_vendor_code = fields.Char(string='Vendor code')
    avc_amazon_qualifier = fields.Char(string="Amazon Qualifier", default="14",
                                       help="Amazon Qualifier available in Global Settings -> Message Format -> "
                                            "Message Format Identifiers -> "
                                            "Your identifiers of Vendor Central Portal")
    sender_ftp_connection_id = fields.Many2one(comodel_name='ftp.server.ept', string="Test Sender FTP server",
                                               domain=[('ftp_type', '=', 'sender')],
                                               help="Used for, identifying in which place the file should be uploaded")
    receiver_ftp_connection_id = fields.Many2one(comodel_name='ftp.server.ept', string="Test Receiver FTP server",
                                                 domain=[('ftp_type', '=', 'receiver')],
                                                 help="Used for, identifying from which place the file "
                                                      "should be downloaded")
    production_sender_ftp_connection_id = fields.Many2one(comodel_name='ftp.server.ept',
                                                          string=" Production Sender FTP server",
                                                          domain=[('ftp_type', '=', 'sender')],
                                                          help="Used for, identifying in which place the file "
                                                               "should be uploaded")
    production_receiver_ftp_connection_id = fields.Many2one(comodel_name='ftp.server.ept',
                                                            string="Production Receiver FTP server",
                                                            domain=[('ftp_type', '=', 'receiver')],
                                                            help="Used for, identifying from which place the file "
                                                                 "should be downloaded")
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string="Warehouse")
    warehouse_ids = fields.Many2many(comodel_name='stock.warehouse', string="Warehouses",
                                     help="This warehouse will use for stock export if stock is available "
                                          "in multiple warehouse.\n Otherwise it take stock form Warehouse "
                                          "which is selected for Sale order")
    picking_policy = fields.Selection([('direct', 'Deliver each product when available'),
                                       ('one', 'Deliver all products at once')],
                                      string='Shipping Policy', default='direct', )
    so_customer_id = fields.Many2one(comodel_name='res.partner', string="Sale Order Partner")
    product_stock_field_id = fields.Selection([('free_quantity', 'Free Quantity'),
                                               ('forecast_quantity', 'Forecast Quantity')],
                                              default="free_quantity",
                                              string="Stock Type",
                                              help="Choose the field of the product which will be used for "
                                                   "stock inventory updates.\nIf empty, "
                                                   "Quantity Available is used.")
    warehouse_code = fields.Char("Warehouse Code")

    avc_file_format = fields.Selection(
        [('edi_fact', 'EDI FACT')], default='edi_fact',
        string='File format for AVC operations')

    amazon_edi_carrier_method = fields.Many2one(comodel_name='delivery.carrier', string='Amazon Carrier')
    amazon_unb_id = fields.Char(string='Amazon Unb')
    amazon_gln_number = fields.Char("Amazon GLN Number")
    warehouse_gln_number = fields.Char("Warehouse GLN Number")  # Added by Tushal Nimavat at 21-04-2022

    # Cron Configurations
    amz_auto_import_po = fields.Boolean("Auto Import Purchase Orders?", default=False)
    amz_auto_inv_and_cost_export = fields.Boolean(string="Auto Export Inventory and Cost Report?", default=False)
    amz_auto_asn_export = fields.Boolean(string="Auto Export Advance Shipment Notices?", default=False)
    amz_auto_invoices_export = fields.Boolean(string="Auto Export Inventory and Cost Report?", default=False)

    cron_count = fields.Integer("Scheduler Count",
                                compute="_compute_get_scheduler_list",
                                help="This Field relocates Scheduler Count.")
    team_id = fields.Many2one('crm.team', string="Sales Team")

    # Packages Configurations
    is_use_packages = fields.Boolean(string='Packages', default=False,
                                     help="By enabling this, the Advance Shipment Notice is sent with package details")

    # account_type = fields.Selection(string='Account Type',
    #                                 selection=[('first_order', 'First Order'), ('back_order', 'Back Order'), ],
    #                                 default='first_order')

    def _compute_get_scheduler_list(self):
        """
            Usage: Used for, count the number of cron of an instance and set in the cron_count field
        """
        ir_cron_obj = self.env['ir.cron']
        for record in self:
            record.cron_count = ir_cron_obj.search_count([('avc_cron_id', '=', record.id)])

    def list_of_vendor_cron(self):
        """
            Usage: Find all the cron of the instance.
            :return: action
        """
        vendor_cron = self.env['ir.cron'].search([('avc_cron_id', '=', self.id)])
        action = {
            'domain': "[('id', 'in', " + str(vendor_cron.ids) + " )]",
            'name': 'Cron Scheduler',
            'view_mode': 'tree,form',
            'res_model': 'ir.cron',
            'type': 'ir.actions.act_window',
        }
        return action

    def toggle_prod_environment_value(self):
        """
        This will switch environment between production and pre-production.
        @return : True
        @author: Keyur Kanani
        """
        self.ensure_one()
        self.is_production_environment = not self.is_production_environment

    @staticmethod
    def get_edi_receive_interface(ftp_server_id, directory_id):
        """
        this function is user for download directory
        :param ftp_server_id: sftp server id
        :param directory_id: download directory
        """
        return sftp_interface(
            ftp_server_id.ftp_host,
            ftp_server_id.ftp_username,
            ftp_server_id.ftp_password,
            ftp_server_id.key_filename,
            ftp_server_id.ftp_port,
            download_dir=directory_id.path
        )

    @staticmethod
    def get_edi_sending_interface(ftp_server_id, directory_id):
        """
        this function is used for upload directory
        :param ftp_server_id: sftp server id
        :param directory_id: download directory
        """
        return sftp_interface(
            ftp_server_id.ftp_host,
            ftp_server_id.ftp_username,
            ftp_server_id.ftp_password,
            ftp_server_id.key_filename,
            ftp_server_id.ftp_port,
            upload_dir=directory_id.path
        )

    def vendor_cron_configuration_action(self):
        """
            Usage: Search the cron configuration view and return that view with instance
            :return:
        """
        action = self.env.ref('amazon_vendor_central_ept.action_wizard_vendor_cron_configuration_ept').read()[0]
        context = {
            'amz_vendor_id': self.id
        }
        action['context'] = context
        return action

    def _get_amazon_sale_requisitions(self, states):
        """
            Usage: Searching all the sale requisitions and return it
            :return: amazon.sale.requisition.ept()
        """
        return self.env['amazon.sale.requisition.ept'].search(
            [('amazon_vendor_instance_id', '=', self.id), ('state', 'in', states)]).ids

    def sync_amazon_po_from_cron(self, args=None):
        """
            Sync the amazon purchase order based on vendor
            :param args: dictionary
        """

        amazon_sale_requisition_ept_obj = self.env['amazon.sale.requisition.ept']
        instance_id = args and args.get('amazon_vendor_instance_id', False)
        if instance_id:
            instance = self.search([('id', '=', instance_id)], limit=1)
            amazon_sale_requisition_ept_obj.with_context({'is_cron': True}).import_order_from_amazon(instance)
        return True

    def export_inventory_and_cost_from_cron(self, args=None):
        """
            prepare and send edi inventory from the cron
            :param args: dictionary
        """
        instance_id = args and args.get('amazon_vendor_instance_id', False)
        if instance_id:
            instance = self.browse(instance_id)
            instance.with_context({'is_cron': True}).export_inventory_and_stock_report()
        return True

    def export_advance_shipment_notices_from_cron(self, args=None):
        """
            prepare and send edi Advance Shipment Notices through the cron
            :param args: dictionary
        """
        instance_id = args and args.get('amazon_vendor_instance_id', False)
        amazon_sale_requisition_ept = self.env['amazon.sale.requisition.ept']
        if instance_id:
            instance = self.browse(instance_id)
            for sale_requisition_id in instance._get_amazon_sale_requisitions(states=['ack_send']):
                sale_requisition_id = amazon_sale_requisition_ept.browse(sale_requisition_id)
                sale_requisition_id.with_context({'is_cron': True}).send_advance_shipment_notice()
        return True

    def export_invoices_from_cron(self, args=None):
        """
            prepare and send edi Invoices through the cron
            :param args: dictionary
        """
        instance_id = args and args.get('amazon_vendor_instance_id', False)
        amazon_sale_requisition_ept = self.env['amazon.sale.requisition.ept']
        if instance_id:
            instance = self.browse(instance_id)
            for sale_requisition_id in instance._get_amazon_sale_requisitions(states=['asn_send']):
                sale_requisition_id = amazon_sale_requisition_ept.browse(sale_requisition_id)
                sale_requisition_id.with_context({'is_cron': True}).export_invoice_to_amazon()
        return True

    def check_import_po_mismatch_details(self, common_log_book, is_cron, ftp_server_id):
        """
            Usage: Used for, Check the required parameter filled or not and check any mismatch data is found
            :param common_log_book: common.log.book.ept()
            :param is_cron: Boolean
            :param ftp_server_id: stp.server.ept() or String
            Added by: Dipak Gogiya, 02/12/2020
            :return: True or False
        """
        common_log_lines_obj = self.env['common.log.lines.ept']
        is_mismatch_details = self.verify_common_import_export_mismatch_details(common_log_book, is_cron)
        if isinstance(ftp_server_id, str):
            _logger.info(ftp_server_id)
            if not is_cron:
                raise UserError(_(ftp_server_id))
            common_log_lines_obj.create_avc_log_lines(ftp_server_id, common_log_book)
            is_mismatch_details = True
        else:
            if not ftp_server_id.po_file_import_prefix:
                field_string = ftp_server_id._fields['po_file_import_prefix'] and ftp_server_id._fields[
                    'po_file_import_prefix'].string
                message = "Please set the {}! \n - Goto : Configuration -> SFTP -> {} -> {}".format(field_string,
                                                                                                    ftp_server_id.display_name,
                                                                                                    field_string)
                if not is_cron:
                    raise UserError(_(message))
                common_log_lines_obj.create_avc_log_lines(message, common_log_book)
                is_mismatch_details = True

        return is_mismatch_details

    def verify_common_import_export_mismatch_details(self, common_log_book, is_cron):
        """
            Usage: Used for verify the common required field values for import or export operation
            :param common_log_book: common.log.book.ept()
            :param is_cron: Boolean
            :return: Boolean
        """
        common_log_lines_obj = self.env['common.log.lines.ept']
        is_mismatch_details = False
        if not self.avc_file_format:
            message = "The selected Instance file format is not set, please set the file format for process the file " \
                      " \n - Goto Configuration -> settings -> Select Vendor -> General Configuration -> AVC File Format."
            _logger.info(message)
            if not is_cron:
                raise UserError(_(message))
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
            is_mismatch_details = True
        if not self.avc_file_format == 'edi_fact':
            message = "AVC File Format not set proper of instance :  [{}]".format(self.name)
            _logger.info(message)
            if not is_cron:
                raise UserError(_(message))
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
            is_mismatch_details = True
        if not self.so_customer_id:
            message = "Sale Order Partner is not set of instance [{}]".format(self.name)
            if not is_cron:
                raise UserError(_(message))
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
            is_mismatch_details = True
        return is_mismatch_details

    def delete_files_from_ftp(self, server_filenames, ftp_server_id, directory_id):
        """
            Usage: This method is used for removing the file from the FTP
            :param server_filenames: file names which is need to removes from the FTP, Type: List
            :param ftp_server_id: ftp.server.ept()
            :param directory_id: ftp.directory.ept()
            :return:
        """
        # Used for, getting the connection object of FTP for removing the files from FTP.
        with self.get_edi_receive_interface(ftp_server_id, directory_id) as edi_interface:
            try:
                edi_interface.sftp_client.chdir(directory_id.path)
                # Remove the files from the FTP
                edi_interface.delete_from_ftp(server_filenames)
                _logger.info(
                    "Total [{}] files are removed from FTP, Removed Files : [{}]".format(len(server_filenames),
                                                                                         server_filenames))
            except Exception as error:
                _logger.info("While removing the files from the FTP, Below Error Occurs: {}".format(error))
                pass
        return True

    def upload_file_to_ftp(self, data, ftp_server, directory_id, filename, common_log_book, raise_warning=False):
        """
            Used for upload the file into FTP
            :param data: Data, Type: String
            :param ftp_server: ftp.server.ept()
            :param directory_id: ftp.directory.ept()
            :param filename: name of the file, Type: String
            :@author: Dipak Gogiya, 04/12/2020
            :return: True or Warning
        """
        output = StringIO()
        output.write(data)
        output.seek(0)

        file_order_ship = NamedTemporaryFile(delete=False)
        file_order_ship.write(output.read().encode())
        file_order_ship.close()
        try:
            with self.get_edi_sending_interface(ftp_server, directory_id) as edi_interface:
                _logger.info("Connection Established Successfully!")
                edi_interface.push_to_ftp(filename, file_order_ship.name)
                _logger.info("File Exported to FTP, File : %s, "
                             "Directory Path : %s" % (filename, directory_id.path))
        except Exception as error:
            message = "File Uploading Fail! Here what we got error : {}".format(error)
            if raise_warning:
                raise Warning(_(message))
            if common_log_book:
                self.env['common.log.lines.ept'].create_avc_log_lines(message, common_log_book)
            return False
        return True

    def export_inventory_and_stock_report(self):
        _logger.info("Export Inventory And Cost Report Process Started.")
        is_cron = self._context.get('is_cron', False)

        # Get Ftp Server.
        ftp_server = self.env['ftp.server.ept'].get_ftp_server(self, is_sender_ftp_server=True,
                                                               is_cron=is_cron)

        # Create the Job
        message = "Export Cost and inventory feed (COSTINV) Report - Job"
        common_log_book = self.env['common.log.book.ept'].create_avc_common_log(
            'amazon.vendor.central.product.ept', 'export', message)
        # Check the required field values or Verify the any mismatch details found
        if self.check_export_inv_and_stock_mismatch_details(ftp_server, common_log_book, is_cron):
            return True

        product_lines = self.prepare_export_inv_and_stock_report_product_lines()
        # Prepare EDI file for Export Stock to amazon vendor central
        file_inventory_data = self.prepare_inventory_and_stock_edi_segment_data(product_lines)

        directory_id = ftp_server.default_upload_dir_id or False
        _logger.info("FTP Directory : %s, Directory Path : %s"
                     % (directory_id.display_name, directory_id.path))

        # Used for, create the new attachment and uploading the file to the FTP
        attachment, file_uploaded_successfully = self.env['ir.attachment'].create_attachment_and_upload_file_to_ftp(
            file_inventory_data,
            ftp_server, self,
            ftp_server.inventory_file_export_prefix,
            directory_id,
            common_log_book=common_log_book,
            raise_warning=is_cron)
        if attachment and common_log_book:
            common_log_book.message_post(body=_("<b>Export Inventory and Cost Report File : </b>"),
                                         attachment_ids=attachment.ids)
        if common_log_book.log_lines:
            if not is_cron:
                return common_log_book.get_action_for_avc_operations(
                    external_id='amazon_vendor_central_ept.action_vendor_common_log_book_ept',
                    form_view_ref='common_connector_library.action_common_log_book_ept_form',
                    record_ids=common_log_book)
        else:
            common_log_book.unlink()
        _logger.info("Export Inventory And Cost Report Process Ended.")
        return True

    def check_export_inv_and_stock_mismatch_details(self, ftp_server, common_log_book, is_cron):
        """
            Usage: Check the required field values or Verify the any mismatch details found
            :param ftp_server: ftp.server.ept()
            :param common_log_book: common.log.book.ept()
            :param is_cron: Boolean
            :return: Boolean
        """
        res_config_settings_obj = self.env['res.config.settings']
        common_log_lines_obj = self.env['common.log.lines.ept']
        is_mismatch_details = self.verify_common_import_export_mismatch_details(common_log_book, is_cron)
        if not self.warehouse_code:
            field_string = res_config_settings_obj._fields['avc_warehouse_code'] and \
                           res_config_settings_obj._fields[
                               'avc_warehouse_code'].string
            message = "The {} is not define of Instance : {}, \n - Goto Configuration => Settings" \
                      " => Select Vendor: {} => Inventory & Cost Configuration => {}". \
                format(field_string, self.name, self.name, field_string)
            _logger.info(message)
            if not is_cron:
                raise UserError(_(message))
            common_log_lines_obj.create_avc_log_lines(ftp_server, common_log_book)
            is_mismatch_details = True
        if not self.product_stock_field_id:
            field_string = res_config_settings_obj._fields['avc_product_stock_field_id'] and \
                           res_config_settings_obj._fields[
                               'avc_product_stock_field_id'].string
            message = "The {} is not define of Instance : {}, \n - Goto Configuration => Settings" \
                      " => Select Vendor: {} => Inventory & Cost Configuration => {}". \
                format(field_string, self.name, self.name, field_string)
            _logger.info(message)
            if not is_cron:
                raise UserError(_(message))
            common_log_lines_obj.create_avc_log_lines(ftp_server, common_log_book)
            is_mismatch_details = True
        if isinstance(ftp_server, str):
            _logger.info(ftp_server)
            if not is_cron:
                raise UserError(_(ftp_server))
            common_log_lines_obj.create_avc_log_lines(ftp_server, common_log_book)
            is_mismatch_details = True

        if not isinstance(ftp_server, str) and not ftp_server.inventory_file_export_prefix:
            field_string = ftp_server._fields['inventory_file_export_prefix'] and ftp_server._fields[
                'inventory_file_export_prefix'].string
            message = "Please set the {}! \n - Goto : Configuration -> SFTP -> {} -> {}".format(field_string,
                                                                                                ftp_server.display_name,
                                                                                                field_string)
            _logger.info(message)
            if not is_cron:
                raise UserError(_(message))
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
            is_mismatch_details = True
        return is_mismatch_details

    def prepare_export_inv_and_stock_report_product_lines(self):
        """
            Usage: Used for prepare the product with stock (Stock calculated based on Stock Type)
            data of all warehouse define in the instance warehouse fields
            :return: product_lines (Contain product with stock info)
        """
        product_obj = self.env['product.product']
        context = self._context
        domain = [('amazon_vendor_instance_id', '=', self.id)]
        if context.get('is_calling_from_amazon_product_action_wizard'):
            domain.append(('id', 'in', context.get('active_ids')))
        if context.get('default_product_ids', False):# Added by Tushal Nimavat at 22-04-2022
            domain.append(('id', 'in', context.get('default_product_ids', False)))

        avc_product_ids = self.env['amazon.vendor.central.product.ept'].search(domain)
        product_ids = avc_product_ids.mapped('product_id')

        warehouses = set(self.warehouse_id + self.warehouse_ids)

        products_and_qty = []
        for warehouse in warehouses:
            if self.product_stock_field_id == 'forecast_quantity':
                products_and_qty.append(product_obj.get_forecasted_qty_ept(warehouse, product_ids.ids))
            else:
                products_and_qty.append(product_obj.get_free_qty_ept(warehouse, product_ids.ids))
        product_lines = product_ids.prepare_products_info(products_and_qty, self.pricelist_id)

        return product_lines

    def prepare_inventory_and_stock_edi_segment_data(self, product_lines):
        """
            Usage: Prepare EDI file for Export Stock to amazon vendor central
            :param product_lines: Product Lines Info
            :return: file inventory EDI Segment Data
        """
        currency_name = self.pricelist_id.currency_id.name

        total_segment = 0
        seq = self.env['ir.sequence'].next_by_code('amazon.edi.inventory.number')
        seq_interchange = self.env['ir.sequence'].next_by_code('amazon.edi.ship.message.trailer')

        file_inventory = """UNB+UNOC:2+%s:%s+%s:%s+%s:%s+%s+++++EANCOM'""" % (
            self.warehouse_gln_number or '',  # changed by Tushal Nimavat at 21-04-2022
            self.avc_amazon_qualifier or '',
            self.amazon_unb_id or '',  # changed by Tushal Nimavat at 21-04-2022
            self.avc_amazon_qualifier, time.strftime("%y%m%d"), time.strftime("%H%M"),
            seq_interchange or '')
        total_segment += 1

        file_inventory += """UNH+1+INVRPT:D:96A:UN:EAN008'"""
        total_segment += 1

        file_inventory += """BGM+35+%s+9'""" % (seq or '')
        total_segment += 1

        file_inventory += """DTM+137:%s:102'""" % (time.strftime("%Y%m%d"))
        total_segment += 1

        file_inventory += """DTM+366:%s:102'""" % (time.strftime("%Y%m%d"))
        total_segment += 1

        file_inventory += """NAD+SU+%s::9'""" % (
                    self.warehouse_gln_number or '')  # changed by Tushal Nimavat at 21-04-2022
        total_segment += 1

        """ warehouse_code = Warehouse Code of Cost and Inventory Report"""
        file_inventory += """NAD+WH+%s::92'""" % (self.warehouse_code or '')  # self.amazon_gln_number
        total_segment += 1

        file_inventory += """CUX+2:%s:10'""" % (currency_name)
        total_segment += 1

        file_inventory, total_segment = self.env['amazon.sale.requisition.line.ept'] \
            .prepare_inventory_and_stock_edi_lines_segment_data(file_inventory, total_segment, product_lines, self)

        file_inventory += """UNT+%s+%s'""" % (str(total_segment), str(seq))
        file_inventory += """UNZ+1+%s'""" % (str(seq_interchange))

        _logger.info("Total Segments of Export Inventory and Cost Report are : {}".format(total_segment))

        return file_inventory
