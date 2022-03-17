""" This file creating and managing the Amazon Requisition Order functionality """
import csv
import time
import logging
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger("Amazon Vendor Central Ept")


class AmazonSaleRequisition(models.Model):
    """
        Create and Manage the Amazon Requisition Order Functionality
    """
    _name = 'amazon.sale.requisition.ept'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'
    _description = 'Amazon Sales Requisition'

    def _compute_vendor_order_ids(self):
        """
        This function it the compute function and calculate the value of total order crated from 1 Vendor order.
        Set that order count in vendor order.
        """
        for order in self:
            order.order_count = len(order.sale_order_id)

    def _compute_check_invoice_exists(self):
        for record in self:
            if record.sale_order_id.invoice_ids:
                record.is_invoice_exists = True
            else:
                record.is_invoice_exists = False

    @api.depends('amazon_sale_requisition_line_ids.product_availability')
    def _compute_is_product_availability_ia_or_ib(self):
        requisition_lines = self.amazon_sale_requisition_line_ids.filtered(
            lambda req_line: req_line.product_availability in ['IA', 'IB'])
        if requisition_lines:
            self.is_product_availability_ia_or_ib = True
        else:
            self.is_product_availability_ia_or_ib = False

    name = fields.Char(string='Reference', help='Reference', readonly=True, copy=False)
    partner_id = fields.Many2one('res.partner', help='Customer')
    shipping_partner_id = fields.Many2one('res.partner', string='Shipping Partner', help='Shipping Address')
    invoice_partner_id = fields.Many2one('res.partner', string='Invoice Partner', help='Invoice Address')
    amazon_vendor_instance_id = fields.Many2one('amazon.vendor.instance', string='Vendor',
                                                help='Amazon Vendor Instance', copy=False)
    order_date = fields.Date(string='Order Date', help='Process Lines')
    delivery_date = fields.Date(string='Delivery Date', help='Delivery Date', readonly=True)
    max_delivery_date = fields.Date(string='Max Delivery Date', help='Max Delivery Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('processed', 'Processed'),
                              ('ack_send', 'Ack Sent'),
                              ('asn_send', 'Asn Sent'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')], string='Order State', store=True, default='draft')
    amazon_sale_requisition_line_ids = fields.One2many('amazon.sale.requisition.line.ept',
                                                       'amazon_sale_requisition_id',
                                                       string="Amazon Sale Requisition Lines", )
    sale_order_id = fields.Many2one('sale.order', string='Vendor Order')

    sender_id = fields.Char('Sender ID', readonly=True)
    recipient_id = fields.Char('Recipient ID', readonly=True)
    buyer_id = fields.Char('Buyer ID', readonly=True)
    buyer_address = fields.Char('Buyer Address', readonly=True)
    delivery_party_id = fields.Char('Delivery Party ID', readonly=True)
    country_code = fields.Char('Delivery Country', readonly=True)
    invoice_party_id = fields.Char('Invoice Party ID', readonly=True)
    currency_code = fields.Char('Currency Code', readonly=True)
    vat_number = fields.Char('VAT Registration Number', readonly=True)
    amazon_edi_order_id = fields.Char(string='Amazon Reference', readonly=True)
    is_acknowledgement_sent = fields.Boolean(string='Acknowledgement', help='Is Acknowledgement Sent', readonly=True)
    syntax_identifier = fields.Selection([('UNOA', 'UNOA'),
                                          ('UNOC', 'UNOC')], string="Identifier")
    association_code = fields.Char(string="Association assigned code")
    message_function_code = fields.Char(string="Function of the message")
    warehouse_code = fields.Char(string="Warehouse Code")
    avc_vendor_code = fields.Char('Vendor code')
    avc_file_format = fields.Selection(
        related="amazon_vendor_instance_id.avc_file_format",
        string='File Format', readonly=True)
    order_count = fields.Integer(string='Order Count', compute='_compute_vendor_order_ids')
    is_invoice_exists = fields.Boolean(string="Is Invoice Exists?", default=False,
                                       compute=_compute_check_invoice_exists)
    country_id = fields.Many2one('res.country', string="Country")
    currency_id = fields.Many2one('res.currency', string='Currency')
    is_product_availability_ia_or_ib = fields.Boolean(
        string='Product Availability', default=False, compute=_compute_is_product_availability_ia_or_ib, store=True)

    def create(self, vals):
        """
        Create the sequence for requisition and do the super call of method.
        :return: super call of create method.
        """
        vals['name'] = self.env['ir.sequence'].next_by_code('amazon.sale.requisition.ept')
        return super(AmazonSaleRequisition, self).create(vals)

    def action_view_vendor_order(self):
        """
        This function returns an action that displays existing orders
        of given vendor central sales order ids. It can either be an in a list or a form
        view if there is only one order to show.
        :return:action
        """
        action = self.env.ref('sale.action_quotations').read()[0]

        sale_order_ids = self.mapped('sale_order_id')
        if len(sale_order_ids) > 1:
            action['domain'] = [('id', 'in', sale_order_ids.ids)]
        elif sale_order_ids:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = sale_order_ids.id
        return action

    def create_common_log_ept(self, message='', operation='import'):
        """
        Method for create process log.
        :param message:
        :return:
        """
        model = self.env['ir.model'].search([('model', '=', 'amazon.sale.requisition.ept')])
        vals = {
            'type': operation,
            'module': 'amz_vendor_central',
            'message': message,
            'model_id': model.id,
            'res_id': self.id
        }
        return self.env['common.log.book.ept'].create(vals)

    def import_order_from_amazon(self, instance):
        """
            This method is used for import the order from amazon.
            :param instance: amazon.vendor.instance()
            :return:True
        """
        _logger.info("Import Purchase Order (PO) Process Started...")
        common_log_lines_obj = self.env['common.log.lines.ept']
        server_filenames = []
        message = "Import Purchase Order (PO) - Job"
        common_log_book = self.env['common.log.book.ept'].create_avc_common_log('amazon.sale.requisition.ept', 'import',
                                                                                message)
        is_cron = self._context.get('is_cron', False)

        # Get Ftp Server.
        ftp_server_id = self.env['ftp.server.ept'].get_ftp_server(instance, is_sender_ftp_server=False,
                                                                  is_cron=is_cron)

        # Check Required parameter Values for import purchase order.
        if not instance.check_import_po_mismatch_details(common_log_book, is_cron, ftp_server_id):

            directory_id = ftp_server_id.default_receive_dir_id

            # Used for, getting the connection object of FTP for downloading the files from FTP.
            with instance.get_edi_receive_interface(ftp_server_id, directory_id) \
                    as edi_interface:
                try:
                    # Used for, Downloading the files from the FTP
                    filenames_dict = edi_interface.pull_from_ftp(ftp_server_id.po_file_import_prefix)
                except Exception as error:
                    message = "Please check SFTP Configuration, Here what we get " \
                              "instead of Download the file from FTP : {}".format(error)
                    if not is_cron:
                        raise Warning(_(message))
                    _logger.info(message)
                    common_log_lines_obj.create_avc_log_lines(message, common_log_book)
                    return True

            if not common_log_book.log_lines and not filenames_dict:
                message = "No file is available in the FTP"
                if not is_cron:
                    raise Warning(_(message))
                _logger.info(message)
                common_log_lines_obj.create_avc_log_lines(message, common_log_book)

            if not common_log_book.log_lines:
                common_log_book.unlink()

            _logger.info("Total [{}] Files Found from FTP".format(len(filenames_dict)))
            for server_filename, filename in filenames_dict.items():
                with open(filename) as file:
                    _logger.info("Starting process of file: ""'{}'".format(server_filename))

                    log_book_msg = 'Amazon Import Purchase Order - (PO) Job for Import PO File : [{}]'.format(
                        server_filename)
                    common_log_book = self.env['common.log.book.ept'].create_avc_common_log(
                        'amazon.sale.requisition.ept', 'import', log_book_msg)

                    # Starting to process the EDI file and create the amazon sale requisition order with lines
                    requisition = self.read_amazon_edi_fact(instance, file, "'", common_log_book, is_cron,
                                                            server_filename)
                    server_filenames.append(server_filename)

                    if not common_log_book.log_lines:
                        common_log_book.unlink()
                    else:
                        if requisition:
                            common_log_book.write({'amazon_sale_requisition_id': requisition.id})
                    _logger.info("Process Ended of file: ""'{}'".format(server_filename))

            if server_filenames:
                # Used for delete files from the FTP
                instance.delete_files_from_ftp(server_filenames, ftp_server_id, directory_id)

        _logger.info("Import Purchase Order (PO) Process Ended...")
        return True

    def process_edi_segments(self, instance, file, delimiter, common_log_book, is_cron):
        """
            Used for prepare the segment data dictionary
            :param instance: amazon.vendor.instance()
            :param file: contain the order data, Type: Binary
            :param delimiter: delimiter
            :param common_log_book: common.log.book.ept()
            :param is_cron: Boolean
            :return: order_info, message_info, order_line_info, order_type, segment_data, is_mismatch_details
        """
        common_log_lines_obj = self.env['common.log.lines.ept']
        order_line_info, order_info, other_vals, message_info, is_mismatch_details = {}, {}, {}, {}, False
        line_no, order_line, total_segment, order_type, segment_data = 1, 0, 0, '', ''

        for segment in csv.reader(file, delimiter=delimiter, quotechar='|'):
            for seg in segment:
                if not seg.strip():
                    continue
                if seg.startswith('UNB+UNOA') or seg.startswith('UNB+UNOC'):
                    values = self.prepare_unb_unoa_unoc_segment(seg)
                    message_info.update(values)
                    total_segment += 1
                elif seg.startswith('UNH'):
                    values = self.prepare_unh_segment(seg)
                    order_info.update(values)
                    total_segment += 1
                elif seg.startswith('BGM+'):
                    values = self.prepare_bgm_segment(seg)
                    order_info.update(values)
                    total_segment += 1
                elif seg.startswith('DTM+137'):
                    values = self.prepare_dtm_137_segment(seg)
                    order_info.update(values)
                    total_segment += 1
                elif seg.startswith('DTM+63'):
                    order_vals, message_vals = self.prepare_dtm_63_segment(seg)
                    order_info.update(order_vals)
                    message_info.update(message_vals)
                    total_segment += 1
                elif seg.startswith('DTM+64'):
                    values = self.prepare_dtm_64_segment(seg)
                    other_vals.update(values)
                    total_segment += 1
                elif seg.startswith('RFF+CR'):
                    values = self.prepare_rff_cr_segment(seg)
                    order_info.update(values)
                    total_segment += 1
                elif seg.startswith('RFF+ADE'):
                    order = seg.split(":")
                    order_type = order[1]
                    total_segment += 1
                elif seg.startswith('RFF+PD'):
                    total_segment += 1
                elif seg.startswith('REF+ON'):
                    total_segment += 1
                elif seg.startswith('NAD+BY'):
                    values = self.prepare_nad_by_segment(seg)
                    message_info.update(values)
                    total_segment += 1
                elif seg.startswith('NAD+SU'):
                    values = self.prepare_nad_su_segment(seg)
                    other_vals.update(values)
                    total_segment += 1
                elif seg.startswith('NAD+DP'):
                    message_vals, order_vals = self.prepare_nad_dp_segment(seg, instance)
                    message_info.update(message_vals)
                    order_info.update(order_vals)
                    total_segment += 1
                elif seg.startswith('NAD+WH'):
                    order_vals = self.prepare_nad_wh_segment(seg)
                    order_info.update(order_vals)
                    total_segment += 1
                elif seg.startswith('NAD+IV'):
                    # vendors information get from this part
                    message_vals, order_vals = self.prepare_nad_iv_segment(seg, instance)
                    message_info.update(message_vals)
                    order_info.update(order_vals)
                    total_segment += 1
                elif seg.startswith('RFF+VA'):
                    values = self.prepare_rff_va_segment(seg)
                    message_info.update(values)
                    total_segment += 1
                elif seg.startswith('CUX+2'):
                    order_vals, message_vals = self.prepare_cux_2_segment(seg, instance)
                    other_vals.update(order_vals)
                    message_info.update(message_vals)
                    total_segment += 1
                elif seg.startswith('LIN+'):
                    order_line_info = self.prepare_lin_segment(seg, order_line_info, line_no)
                    line_no += 1
                    order_line += 1
                    total_segment += 1
                elif seg.startswith('PIA+'):
                    code = seg.split("+")
                    item_type = code[2].split(':')[1]
                    code = code[2][:-3] if len(code) > 2 else ''
                    if not order_line_info['Line_' + str(line_no - 1)].get('ean', False):
                        order_line_info['Line_' + str(line_no - 1)].update({'default_code': code})
                    order_line_info['Line_' + str(line_no - 1)].update({'item_type': item_type})
                    total_segment += 1
                elif seg.startswith('QTY+'):
                    order_line_info = self.prepare_qty_segment(seg, order_line_info, line_no)
                    total_segment += 1
                elif seg.startswith('PRI+'):
                    order_line_info = self.prepare_pri_segment(seg, order_line_info, line_no)
                    total_segment += 1
                elif seg.startswith('UNS+S'):
                    total_segment += 1
                elif seg.startswith('CNT+2'):
                    total_segment += 1
                    is_mismatch = self.prepare_cnt_2_segment(seg, order_line, common_log_book, is_cron=is_cron)
                    if is_mismatch: is_mismatch_details = True
                elif seg.startswith('UNT+'):
                    is_mismatch = self.prepare_unt_segment(seg, total_segment, common_log_book, is_cron=is_cron)
                    if is_mismatch: is_mismatch_details = True
                elif seg.startswith('UNZ+'):
                    continue
                else:
                    message = 'Segment [%s] Mismatch.' % seg
                    common_log_lines_obj.create_avc_log_lines(message, common_log_book)
                    is_mismatch_details = True
            segment_data = "'".join(segment)
        return order_info, message_info, order_line_info, order_type, segment_data, is_mismatch_details

    def read_amazon_edi_fact(self, instance, file, delimiter, common_log_book, is_cron, server_filename):
        """
            Used for process the purchase order file download from FTP and Create sale requisition with its lines.
            :param instance: amazon.vendor.instance()
            :param file: contain the order data, type: Binary
            :param delimiter: delimiter
            :param common_log_book: common.log.book.ept()
            :param is_cron: Boolean
            :param server_filename: Contain the file name getting from the FTP.
            @author: Keyur Kanani
        """
        attachment = self.env['ir.attachment']

        # Read the EDI file and prepare the segment data for create the attachment
        order_info, message_info, order_line_info, order_type, segment_data, is_mismatch_details = \
            self.process_edi_segments(instance, file, delimiter, common_log_book, is_cron)

        if is_mismatch_details: return True

        if order_type == 'firstorder':
            existing_order_id = self.search([('amazon_edi_order_id', '=', order_info.get('order_name', ''))], limit=1)
            if existing_order_id:
                _logger.info("Amazon Requisition Order : [{}] Already Exists".format(existing_order_id.name))
                return True

        # Create the Amazon Sale Requisition Order.
        requisition_id = self.create_amazon_sale_requisition_order(order_info, message_info, instance)

        if requisition_id:
            # Create the Amazon Sale Requisition Order Lines and attach with Amazon Sale Requisition Order.
            self.env['amazon.sale.requisition.line.ept'].create_amazon_sale_requisition_lines(order_line_info,
                                                                                              requisition_id,
                                                                                              common_log_book,
                                                                                              instance)

        if segment_data:
            res_model = 'amazon.sale.requisition.ept'
            # Create the attachment
            attachment = attachment.create_file_attachment(segment_data, server_filename, res_model)

        if attachment:
            common_log_book.write({'attachment_id': attachment.id, 'res_id': requisition_id.id,
                                   'amazon_sale_requisition_id': requisition_id.id})
            # Attach the attachment with common log book
            common_log_book.message_post(body=_("<b>Import PO File</b>"),
                                         attachment_ids=attachment.ids)
            # Attach the attachment with amazon order requisition
            requisition_id and requisition_id.message_post(body=_("<b>Import PO File</b>"),
                                                           attachment_ids=attachment.ids)

        return requisition_id

    def create_sale_order(self):
        """
        This is the Parent function and call different sub-functions from this function.
        This function call on clicking on "Create Sale Order" button
        :return:
        """
        # Check any mismatch data found for create the sale order
        self.check_mismatch_details_for_create_sale_order()

        # Filter the Acknowledgment Lines based on product availability
        acknowledgement_lines = self.amazon_sale_requisition_line_ids.filtered(
            lambda l: l.acknowledge_qty > 0 and l.product_availability in ['IA', 'IB'])
        if acknowledgement_lines:
            amazon_product_ids = acknowledgement_lines.mapped('product_id').mapped('default_code')
            if not amazon_product_ids:
                raise Warning(_(
                    "Amazon product not found for defined odoo product,please import amazon product first"))

            # Used for create the sale order based on requisition
            order_id = self.env['sale.order'].create_avc_sale_order(self)

            if order_id:
                # Used for create the sale order lines based on amazon requisition order lines and sale order
                self.env['sale.order.line'].create_avc_sale_order_lines(order_id, acknowledgement_lines)
                self.sale_order_id = order_id.id
                self.state = 'processed'
        return True

    def check_mismatch_details_for_create_sale_order(self):
        """
            Usage: Used for, checking any mismatch data found for create sale order,
            if found then raise the Warning
            Added by: Dipak Gogiya, 04/12/2020
        """
        requisition_order_lines = self.amazon_sale_requisition_line_ids
        if requisition_order_lines.filtered(
                lambda line: not line.product_id and line.product_availability in ['IA', 'IB', 'IR']):
            raise UserError(_("The Product is required if the Product Availability is 'Accepted' or "
                              "'Backorder' or 'Cancel : Out of Stock'"))

        if requisition_order_lines.filtered(lambda line: line.backorder_qty > 0 and line.product_availability != 'IB'):
            raise UserError(_("The Product Availability is required 'Backorder' not 'Accepted' "
                              "if the backorder quantity greater then zero"))

        # if requisition_order_lines.filtered(lambda line: line.acknowledge_qty <= 0):
        #     raise UserError(_("Some Acknowledge Quantity is missing in the Requisition Order Lines "
        #                       "Please define Acknowledge Quantity for create sale order, "
        #                       "Make sure Acknowledge Quantity is greater then Zero"))
        return True

    def create_amazon_sale_requisition_order(self, order_info, message_info, instance):
        """
        Use: To generate sale requisition's value based on given information.
        :param order_info: basic order information, Type: Dictionary
        :param message_info: order information of sandor and receiver,
            Type: Dictionary
        :param instance: amazon.vendor.instance()
        :return: amazon.sale.requisition.ept()
        """
        partner_obj = self.env['res.partner']
        delivery_address = order_info.get('delivery_address', {})
        invoice_address = order_info.get('inv_address_data', {})
        partner_id = invoice_address.get('parent_id', False)
        warehouse_code = order_info.get('warehouse_code', '')
        delivery_add_id = False
        inv_add_id = False
        partner_address = {}

        requisition_address_id = partner_obj.search([('avc_warehouse_code', '=', warehouse_code)],
                                                    limit=1)
        if not requisition_address_id:
            delivery_add_id, inv_add_id = partner_obj. \
                create_or_search_invoice_shipping_partner(delivery_address, invoice_address,
                                                          message_info)
            delivery_add_id.is_avc_customer and delivery_add_id.write({'is_avc_customer': True})
            inv_add_id.is_avc_customer and inv_add_id.write({'is_avc_customer': True})
            partner_address = partner_obj.browse(partner_id).address_get(
                ['contact', 'invoice', 'delivery'])
        order_date = order_info['date_order'].strftime('%Y-%m-%d') if order_info.get('date_order', False) \
            else time.strftime('%Y-%m-%d')
        order_vals = {
            'amazon_edi_order_id': order_info.get('order_name', ''),
            'order_date': order_date,
            'state': 'draft',
            'partner_id': requisition_address_id.id if requisition_address_id else partner_address.get(
                'contact', False),
            'shipping_partner_id': requisition_address_id.id if requisition_address_id else delivery_add_id.id,
            'invoice_partner_id': requisition_address_id.id if requisition_address_id else inv_add_id.id,
            'delivery_date': order_info.get('delivery_date', False),
            'association_code': order_info.get('association_code', ''),
            'message_function_code': order_info.get('message_function_code', ''),
            'warehouse_code': warehouse_code,
            'country_id': order_info.get('country_id', False),
            'currency_id': message_info.get('currency_id', False),
            'avc_vendor_code': order_info.get('avc_vendor_code', ''),
        }
        order_vals.update(message_info)
        order_vals.update({'amazon_vendor_instance_id': instance.id})
        _logger.info("Amazon Requisition Order Values : [{}]".format(order_vals))
        requisition_id = self.create(order_vals)
        return requisition_id

    def export_po_acknowledgment(self):
        """
            Usage: Used for, send the PO Acknowledgment to the amazon vendor center
            based on amazon requisition order and Amazon PO's information it will
            create POA EDI file and send it to Amazon Vendor Central.
            :return: Boolean
        """
        _logger.info("Send Acknowledgment Process Started!")
        attachment = self.env['ir.attachment']
        file_upload_successfully = False
        instance = self.amazon_vendor_instance_id

        # Get FTP Server
        ftp_server = self.env['ftp.server.ept'].get_ftp_server(instance, is_sender_ftp_server=True, is_cron=False)

        # Used for checking the mismatch data
        self.check_mismatch_details_for_po_acknowledgment(ftp_server)

        message = 'Export Purchase Order - (PO) Acknowledgement Log Book'
        common_log_book = self.env['common.log.book.ept'].create_avc_common_log('amazon.sale.requisition.ept',
                                                                                'export',
                                                                                message, self)
        # Get the amazon products if not create the log and exit the process
        is_mismatch_details, amazon_products = self.get_amazon_products(common_log_book)

        if is_mismatch_details:
            return True

        acknowledgement_data = self.prepare_acknowledgment_data(instance, common_log_book,
                                                                amazon_products)

        if common_log_book and not common_log_book.log_lines:
            directory_id = ftp_server.default_upload_dir_id or False
            _logger.info("FTP Directory : %s, Directory Path : %s"
                         % (directory_id.display_name, directory_id.path))

            # Used for, create the new attachment and uploading the file to the FTP
            attachment, file_upload_successfully = attachment.create_attachment_and_upload_file_to_ftp(
                acknowledgement_data,
                ftp_server, instance,
                ftp_server.po_ack_file_export_prefix,
                directory_id, raise_warning=True)

            attachment and self.message_post(body=_("<b>Export PO File</b>"), attachment_ids=attachment.ids)
            common_log_book.unlink()
        else:
            if common_log_book:
                common_log_book.message_post(body=_("<b>Export PO File</b>"),
                                             attachment_ids=attachment.ids)
        if self._context.get('is_call_from_requisition', False):
            if file_upload_successfully:
                self.write({"is_acknowledgement_sent": True, "state": "done"})
        else:
            if file_upload_successfully:
                self.write({"is_acknowledgement_sent": True, "state": "ack_send"})
        _logger.info("Send Acknowledgment Process Ended!")

        return True

    def check_mismatch_details_for_po_acknowledgment(self, ftp_server):
        """
            Usage: Used for check the any mismatch data is found if found then raise the Warning
            Added By: Dipak Gogiya, 04/12/2020
            :return: True
        """
        if not self._context.get('is_call_from_requisition', False) and self.sale_order_id.state not in ['sale']:
            raise UserError(_("You must have to confirm sale orders"))
        if not self.sender_id or not self.recipient_id:
            raise UserError(_("Sender or Recipient identifier not found."))
        if isinstance(ftp_server, str):
            _logger.info(ftp_server)
            raise UserError(_(ftp_server))
        if not ftp_server.po_ack_file_export_prefix:
            field_string = ftp_server._fields['po_ack_file_export_prefix'] and ftp_server._fields[
                'po_ack_file_export_prefix'].string
            message = "Please set the {}! \n - Goto : Configuration -> SFTP -> {} -> {}".format(field_string,
                                                                                                ftp_server.display_name,
                                                                                                field_string)
            raise UserError(_(message))
        return True

    def get_amazon_products(self, common_log_book):
        """
            Usage: Used for find the amazon products based on requisition lines details
            :param common_log_book: common.log.book.ept()
            :return: is_mismatch_details, amazon_products
        """
        is_mismatch_details, mismatch_products, amazon_products = False, [], {}
        amz_avc_product_obj = self.env['amazon.vendor.central.product.ept']
        common_log_lines_obj = self.env['common.log.lines.ept']
        instance = self.amazon_vendor_instance_id
        for requisition_order_line in self.amazon_sale_requisition_line_ids:
            product_id = requisition_order_line.product_id
            amz_avc_product = amz_avc_product_obj. \
                search_avc_existing_amazon_product(product_id, instance) if product_id else product_id
            if not amz_avc_product:
                amz_avc_product = amz_avc_product_obj. \
                    search_avc_amazon_product_by_edit_line_code(instance,
                                                                requisition_order_line.amazon_edi_line_code,
                                                                requisition_order_line.amazon_edi_line_code_type)
            if not amz_avc_product:
                mismatch_products.append(requisition_order_line.amazon_edi_line_code)
                is_mismatch_details = True
            else:
                amazon_products[requisition_order_line.id] = amz_avc_product
        for mismatch_product in mismatch_products:
            message = "Amazon product not found of Amazon Line Code: [{}]".format(mismatch_product)
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
        return is_mismatch_details, amazon_products

    def prepare_acknowledgment_data(self, instance, common_log_book, amazon_products):
        """
            Usage: Used for prepare the acknowledgement data for sending the amazon vendor central
            :param instance: amazon.vendor.instance()
            :param common_log_book: common.log.book.ept()
            :param amazon_products: amazon products
            :return: segment_data
        """
        amazon_edi_order_id = self.amazon_edi_order_id or ''
        supplier_id = instance.supplier_id or ''
        # invoice_address_id = self.invoice_partner_id
        # shipping_address_id = self.shipping_partner_id

        seq_interchange = self.env['ir.sequence'].next_by_code('amazon.edi.purchase.order.response')

        po_ack_file_string = "UNB+%s:2+%s:%s+%s:%s+%s:%s+%s++++1+EANCOM'" % (
            self.syntax_identifier or '', self.recipient_id or '', instance.avc_amazon_qualifier, self.sender_id or '',
            instance.avc_amazon_qualifier, time.strftime("%y%m%d"), time.strftime("%H%M"), str(seq_interchange))
        total_segment = 1

        po_ack_file_string += "UNH+1+ORDRSP:D:96A:UN:%s'" % (self.association_code or '')
        total_segment += 1

        po_ack_file_string += "BGM+231+%s+%s'" % (amazon_edi_order_id, self.message_function_code or '')
        total_segment += 1

        po_ack_file_string += "DTM+137:%s:102'" % (time.strftime("%Y%m%d"))
        total_segment += 1

        date_done = self.delivery_date or time.strftime("%Y%m%d")
        date_done = date_done.strftime("%Y%m%d")

        po_ack_file_string += "DTM+171:%s:102'" % (date_done)
        total_segment += 1

        po_ack_file_string += "RFF+ON:%s'" % (amazon_edi_order_id)
        total_segment += 1

        # po_ack_file_string += "RFF+CR:%s'" % (self.avc_vendor_code or '')
        # total_segment += 1

        # po_ack_file_string += "NAD+BY+%s::9'" % (supplier_id)
        # total_segment += 1

        po_ack_file_string += "NAD+SU+%s::9'" % (supplier_id)
        total_segment += 1

        # po_ack_file_string += "NAD+DP+%s::9++%s:%s+%s+%s++%s+%s'" % (
        #     self.delivery_party_id or '', shipping_address_id.name or '',
        #     shipping_address_id.country_id.name or '', shipping_address_id.street,
        #     shipping_address_id.city or '', shipping_address_id.zip, shipping_address_id.country_id.code or '')
        po_ack_file_string += "NAD+DP+%s::9+++++++%s'" % (
            self.delivery_party_id or '', self.currency_code or '')
        total_segment += 1

        # po_ack_file_string += "NAD+IV+%s::9++%s:%s+%s+%s++%s+%s'" % (
        #     self.invoice_party_id or '', invoice_address_id.name or '',
        #     invoice_address_id.country_id.name or '', invoice_address_id.street,
        #     invoice_address_id.city or '', invoice_address_id.zip, invoice_address_id.country_id.code or '')
        # total_segment += 1

        # po_ack_file_string += "RFF+VA:%s'" % (self.vat_number or '')
        # total_segment += 1

        # po_ack_file_string += "NAD+WH+%s'" % (self.warehouse_code or '')
        # total_segment += 1

        po_ack_file_string += "CUX+2:%s:9'" % (self.currency_code or '')
        total_segment += 1

        if self.amazon_sale_requisition_line_ids:
            pass
        po_ack_file_string, total_segment, line_no = self.amazon_sale_requisition_line_ids. \
            prepare_avc_acknowledgment_lines_data(po_ack_file_string, total_segment,
                                                  common_log_book, amazon_products)

        po_ack_file_string += "UNS+S'"
        total_segment += 1

        po_ack_file_string += "CNT+2:%s'" % (str(line_no))
        total_segment += 1

        seq = self.env['ir.sequence'].next_by_code('amazon.edi.ship.message.trailer')
        po_ack_file_string += "UNT+%s+%s'" % (str(total_segment), str(seq))
        po_ack_file_string += "UNZ+1+%s'" % (str(seq_interchange))

        return po_ack_file_string

    def send_advance_shipment_notice(self):
        """
            Usage: Used for, preparing the EDI file of Send Advance Shipment Notice
            and sending the file to the Amazon Vendor Central
            :return: Boolean
        """
        attachments = self.env['ir.attachment']
        stock_picking = self.env['stock.picking']
        _logger.info("Send Advance Shipment Notice Process Started!")
        instance = self.amazon_vendor_instance_id
        is_cron = self._context.get('is_cron', False) or False
        pickings = self.sale_order_id.picking_ids.filtered(
            lambda x: not x.shipment_notice_sent and x.location_dest_id.usage == 'customer' and x.state not in ['cancel'])
        if not pickings:
            return False
        # Get FTP Server
        ftp_server = self.env['ftp.server.ept'].get_ftp_server(instance, is_sender_ftp_server=True, is_cron=is_cron)

        message = 'Export Advance Shipment Notice - [856] Log Book'
        common_log_book = self.env['common.log.book.ept'].create_avc_common_log('amazon.sale.requisition.ept',
                                                                                'export',
                                                                                message, self)
        if isinstance(ftp_server, str):
            self.env['common.log.lines.ept'].create_avc_log_lines(ftp_server, common_log_book)
            return False

        updated_pickings = self.get_updated_pickings_for_asn(pickings, ftp_server, common_log_book, is_cron=is_cron)

        _logger.info("FTP Server : {}".format(ftp_server.display_name))
        directory_id = ftp_server.default_upload_dir_id or False
        _logger.info("FTP Directory : %s, Directory Path : %s"
                     % (directory_id.display_name, directory_id.path))

        for picking in updated_pickings:
            picking = stock_picking.browse(picking)
            # Prepare the Advance Shipment Notice EDI Data
            advance_shipment_notice_data = picking.prepare_asn_data()

            attachment, file_upload_successfully = attachments.create_attachment_and_upload_file_to_ftp(
                advance_shipment_notice_data,
                ftp_server, instance,
                ftp_server.asn_file_export_prefix,
                directory_id, common_log_book=common_log_book)
            attachments += attachment
            if file_upload_successfully:
                picking.write({'shipment_notice_sent': True})

        if pickings and all(pickings.filtered(lambda picking: picking.state != 'cancel').mapped('shipment_notice_sent')):
            self.write({'state': 'asn_send'})
        if attachments:
            _logger.info("Total {} Attachments created".format(len(attachments)))
            self.message_post(body=_("<b>Advance Shipment Notice File</b>"),
                              attachment_ids=attachments.ids)

        if not is_cron and common_log_book.log_lines:
            return common_log_book.get_action_for_avc_operations(
                external_id='amazon_vendor_central_ept.action_vendor_common_log_book_ept',
                form_view_ref='common_connector_library.action_common_log_book_ept_form',
                record_ids=common_log_book)
        if not common_log_book.log_lines:
            common_log_book.unlink()
        _logger.info("Send Advance Shipment Notice Process Ended!")
        return True

    def get_updated_pickings_for_asn(self, pickings, ftp_server, common_log_book, is_cron=False):
        """
           Used for check the any mismatch data is found if found then raise the Warning
           :param pickings: stock.picking()
           :param ftp_server: ftp.server.ept()
           :param common_log_book: common.log.book.ept()
           :param is_cron: Boolean
           :@author: Dipak Gogiya, 07/12/2020
           :return: True
        """
        res_config_settings_obj = self.env['res.config.settings']
        common_log_lines_obj = self.env['common.log.lines.ept']
        mismatch_pickings = set()
        instance = self.amazon_vendor_instance_id
        message = "Mismatch Details: \n    "
        mismatch_details = False
        if not self.sender_id and not self.recipient_id:
            message += "- Sender or recipient identifier not found.\n    "
            mismatch_details = True
            if not is_cron:
                raise UserError(_(message))
        if not self.is_acknowledgement_sent:
            message += f"- Please Send Acknowledgment First!\n    "
            mismatch_details = True
            if not is_cron:
                raise UserError(_(message))
        if not self.sale_order_id.warehouse_id.partner_id:
            message += f"- Please Define the Address of Warehouse : [{self.sale_order_id.warehouse_id.name}]\n    "
            mismatch_details = True
            if not is_cron:
                raise UserError(_(message))
        if not ftp_server.asn_file_export_prefix:
            message += f"Please Select the Shipment Notice File Prefix of FTP Server : {ftp_server.display_name}"
            mismatch_details = True
            if not is_cron:
                raise UserError(_(message))
        sscc_code_string = self.env['stock.picking']._fields['sscc_code'] and \
                           self.env['stock.picking']._fields['sscc_code'].string
        if not mismatch_details and not instance.amazon_gln_number:
            field_string = res_config_settings_obj._fields['amazon_gln_number'] and \
                           res_config_settings_obj._fields[
                               'amazon_gln_number'].string
            message += "The {} is not define of Instance : {}, \n - Goto Settings => Amazon Vendor" \
                      " => Select Vendor: {} => Inventory & Cost Configuration => {}". \
                format(field_string, instance.name, instance.name, field_string)
            mismatch_details = True
            if not is_cron:
                raise UserError(_(message))
        if mismatch_details and is_cron:
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
            return set()
        for picking in pickings:
            if not picking.sscc_code:
                message = "The {} is not defined of Delivery Order : [{}]". \
                    format(sscc_code_string, picking.name)
                common_log_lines_obj.create_avc_log_lines(message, common_log_book, order_ref=picking.name)
                mismatch_pickings.add(picking.id)
            elif picking.state != 'done':
                message = f"Picking {picking.name} not validated, For sending the Advance Shipment Notice please " \
                          f"validate the picking"
                common_log_lines_obj.create_avc_log_lines(message, common_log_book, order_ref=picking.name)
                mismatch_pickings.add(picking.id)
        return set(pickings.ids) - mismatch_pickings

    def export_invoice_to_amazon(self):
        """
            Export the invoice to amazon for the ansi x12 and edi fact.
            :return: True
            Added By: Keyur Kanani
        """
        is_cron = self._context.get('is_cron', False) or False
        message = ""
        if self.sale_order_id:
            if not self.sale_order_id.picking_ids:
                message += f"Delivery Order not found of Sale Order: [{self.sale_order_id.name}]"
                if not is_cron:
                    raise Warning(_(message))
            if not any(self.sale_order_id.picking_ids.mapped('shipment_notice_sent')):
                message += f"Please Send Advance Shipment First, Requisition: [{self.name}], " \
                           f"Sale Order: [{self.sale_order_id.name}]"
                if not is_cron:
                    raise Warning(_(message))
            if not self.sale_order_id.invoice_ids:
                message += f"Please create Invoice for Sale Order: [{self.sale_order_id.name}]"
                if not is_cron:
                    raise Warning(_(message))
            invoices = self.sale_order_id.invoice_ids.filtered(
                lambda invoice: invoice.move_type == 'out_invoice' and invoice.is_amazon_edi_invoice
                                and not invoice.exported_to_edi)
            if message:
                # Create the new JOB.
                common_log_book = self.env['common.log.book.ept'].create_avc_common_log('amazon.sale.requisition.ept',
                                                                                        'export',
                                                                                        "Export Invoices To Amazon Vendor Central Job",
                                                                                        self)
                self.env['common.log.lines.ept'].create_avc_log_lines(message, common_log_book)
            # Exported the invoices to the amazon vendor central
            if not message and invoices:
                return invoices.send_avc_invoices_to_amazon(self, is_cron)
        return True

    def vendor_requisition_reset_to_draft_ept(self):
        """
        Reset sale order requisition to draft from cancelled state
        @author: Keyur
        :return:
        """
        self.ensure_one()
        self.write({'state': 'draft'})

    def prepare_unb_unoa_unoc_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        header = segment.split("+")
        return {'sender_id': header[2][:-3], 'recipient_id': header[3][:-3],
                'syntax_identifier': header[1][:-2]}

    def prepare_unh_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        association_code = segment.split(':')[4]
        return {'association_code': association_code}

    def prepare_bgm_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        order_name = segment.split("+")
        message_code = order_name[3]
        order_name = order_name[2] if len(order_name) >= 3 else ''
        return {'order_name': order_name,
                'message_function_code': message_code}

    def prepare_dtm_137_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        date_seg = segment.split(":")
        date_order = datetime.strptime(date_seg[1], '%Y%m%d')
        return {'date_order': date_order}

    def prepare_dtm_63_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        date_seg = segment.split(":")
        delivery_date = datetime.strptime(date_seg[1], '%Y%m%d')
        return {'delivery_date': delivery_date}, {'max_delivery_date': delivery_date}

    def prepare_dtm_64_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        date_seg = segment.split(":")
        earliest_date = datetime.strptime(date_seg[1], '%Y%m%d')
        return {'earliest_date': earliest_date}

    def prepare_rff_cr_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        vendor_code_seg = segment.split(":")
        return {'avc_vendor_code': vendor_code_seg[1]}

    def prepare_nad_by_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        buyer_id = segment.split(":")
        buyer_address = buyer_id and buyer_id[0][7:] + ': ' + buyer_id[2]
        buyer_id = buyer_id and buyer_id[0][7:]
        return {'buyer_id': buyer_id, 'buyer_address': buyer_address}

    def prepare_nad_su_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        supplier_id = segment.split(":")
        supplier_id = supplier_id and supplier_id[0][7:]
        return {'supplier_id': supplier_id}

    def prepare_location_162_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        location_id = segment.split(":")
        return {'sr_location_id': location_id and location_id[0][8:]}  # sr means sales report

    def prepare_sales_report_dtm_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        date_seg = segment.split(":")
        date_order = datetime.strptime(date_seg[1], '%Y%m%d')
        date = {'dtm_90_date_order': date_order} \
            if date_seg[1] == 'DTM+90' else {'dtm_91_date_order': date_order}
        return date

    def prepare_nad_dp_segment(self, segment, instance):
        """
           Used for prepare the segment
           :param segment: segment data
           :param instance: amazon.advantage.instance()
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        country_obj = self.env['res.country']
        delivery = segment.split("+")
        delivery_party_id = delivery[2][:-3]
        country_code = delivery[len(delivery) - 1]
        country_id = country_obj.search([('code', 'ilike', country_code)], limit=1)
        delivery_address = self.prepare_delivery_address(delivery, country_id, instance)
        return {'delivery_party_id': delivery_party_id, 'country_code': country_code}, {
            'delivery_address': delivery_address, 'country_id': country_id.id}

    def prepare_nad_wh_segment(self, segment):
        """
            Used for prepare the warehouse code segment
            :param segment: segment data
            :return: Dict.
        """
        warehouse_code = segment.split("+")
        return {'warehouse_code': warehouse_code[2]}

    def prepare_delivery_address(self, delivery, country_id, instance):
        """
           Used for prepare the segment
           :param delivery: delivery info, Type: String
           :param country_id: res.country()
           :param instance: amazon.advantage.instance()
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        return {'name': delivery[4],
                'street': delivery[5],
                'city': delivery[6],
                'zip': delivery[8],
                'country_id': country_id.id,
                'parent_id': instance.so_customer_id.id,
                'type': 'delivery'}

    def prepare_nad_iv_segment(self, segment, instance):
        """
           Used for prepare the segment
           :param segment: segment data
           :param instance: amazon.advantage.instance()
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        country_obj = self.env['res.country']
        # vendors information get from this part
        customer = False
        invoice_seg = segment.split("+")
        invoice_id = invoice_seg and invoice_seg[2][:-3]
        if invoice_seg[4].find(":") >= 0:
            customer = invoice_seg[4].split(":")
        elif invoice_seg[4].find(",") >= 0:
            customer = invoice_seg[4].split(",")
        country_id = country_obj.search([('code', 'ilike', invoice_seg[9])], limit=1)
        inv_address_data = self.prepare_inv_address(customer, invoice_seg,
                                                    country_id, instance)
        return {'invoice_party_id': invoice_id}, \
               {'inv_address_data': inv_address_data, 'invoice_address': segment}

    def prepare_inv_address(self, customer, invoice_seg, country_id, instance):
        """
           Used for prepare invoice address
           :param customer: address of customer, Type : String
           :param invoice_seg: invoice segment, type: String
           :param country_id: res.country()
           :param instance: amazon.advantage.instance()
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        return {
            'type': 'invoice',
            'name': customer and "{}".format(customer[0]) or '',
            'street': customer and customer[1] or '',
            'street2': invoice_seg[5],
            'city': invoice_seg[6],
            'zip': invoice_seg[8],
            'country_id': country_id.id if country_id else False,
            'parent_id': instance.so_customer_id.id,
        }

    def prepare_rff_va_segment(self, segment):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        vat_number = segment.split(":")
        return {'vat_number': vat_number[1]}

    def prepare_cux_2_segment(self, segment, instance):
        """
            Used for prepare the segment
            :param segment: segment data
            :param instance: amazon.advantage.instance()
            :@author: Dipak Gogiya, 02/08/2020
            :return: Dict.
        """
        currency = segment.split(":")
        currency_code = currency[1]
        currency_id = self.env['res.currency'].search([('name', '=', currency_code)], limit=1)
        pricelist_id = instance.pricelist_id if instance else False
        pricelist_id = pricelist_id.id if pricelist_id else False
        return {'currency_id': currency_id and currency_id.id, 'pricelist_id': pricelist_id}, \
               {'currency_code': currency_code, 'currency_id': currency_id and currency_id.id}

    def prepare_lin_segment(self, segment, order_line_info, line_no):
        """
           Used for prepare the segment lines
           :param segment: segment data
           :param order_line_info: segment data lines
           :param line_no: contain line number, Type: Integer
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        # sale order line data separate here
        order_line_info.update({'Line_' + str(line_no): {}})
        ean = segment.split("+")
        ean = ean[len(ean) - 1]
        if ean.upper().find('EN', 0, len(ean)) != -1 \
                and ean.upper().find(':', 0, len(ean)) != -1:
            ean = ean.split(":")[0] if ean.split(":") else ''
            order_line_info['Line_' + str(line_no)].update({'ean': ean, 'item_type': 'EN'})
        # UP used for Universal Product Code
        elif ean.upper().find('UP', 0, len(ean)) != -1 \
                and ean.upper().find(':', 0, len(ean)) != -1:
            ean = ean.split(":")[0] if ean.split(":") else ''
            order_line_info['Line_' + str(line_no)].update({'ean': ean, 'item_type': 'UP'})
        elif ean.upper().find('SRV', 0, len(ean)) != -1 \
                and ean.upper().find(':', 0, len(ean)) != -1:
            ean = ean.split(":")[0] if ean.split(":") else ''
            order_line_info['Line_' + str(line_no)].update({'ean': ean, 'item_type': 'SRV'})

        return order_line_info

    def prepare_pia_sales_report_segment(self, segment, order_line_info, line_no):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        pia_segment = segment.split(":")
        order_line_info['Line_' + str(line_no - 1)].update({'pia_code': pia_segment and pia_segment[1][6:]})
        return order_line_info

    def prepare_moa_segment(self, segment, order_line_info, line_no):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        moa_segment = segment.split(":")
        order_line_info['Line_' + str(line_no - 1)].update({'cost_of_goods_sold': moa_segment and moa_segment[-1]})
        return order_line_info

    def prepare_sales_report_qty_segment(self, segment, order_line_info, line_no):
        """
           Used for prepare the segment
           :param segment: segment data
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        sr_qty_segment = segment.split(":")
        qty_segment = sr_qty_segment[1] if len(sr_qty_segment) > 1 else 0
        if sr_qty_segment[0] == 'QTY+21':
            order_line_info['Line_' + str(line_no - 1)].update({'sr_ordered_qty': qty_segment})
        elif sr_qty_segment[0] == 'QTY+145':
            order_line_info['Line_' + str(line_no - 1)].update({'sr_on_hand_qty': qty_segment})
        else:
            order_line_info['Line_' + str(line_no - 1)].update({'sr_sold_qty': qty_segment})
        return order_line_info

    def prepare_qty_segment(self, segment, order_line_info, line_no):
        """
           Used for prepare the segment
           :param segment: segment data
           :param order_line_info: segment data lines
           :param line_no: contain line number, Type: Integer
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        qty = segment.split(":")
        qty = qty[1] if len(qty) > 1 else 0
        order_line_info['Line_' + str(line_no - 1)].update({'qty': qty})
        return order_line_info

    def prepare_pri_segment(self, segment, order_line_info, line_no):
        """
           Used for prepare the segment
           :param segment: segment data
           :param order_line_info: segment data lines
           :param line_no: contain line number, Type: Integer
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        price = segment.split(":")
        if len(price) > 3:
            price_qualifier = price[3]
            order_line_info['Line_' + str(line_no - 1)].update(
                {'price_qualifier': price_qualifier}
            )
        price = price[1] if len(price) > 1 else 0
        order_line_info['Line_' + str(line_no - 1)].update({'price': price})
        return order_line_info

    def prepare_cnt_2_segment(self, segment, order_line, common_log_book, is_cron=False):
        """
           Used for prepare the segment
           :param segment: segment data
           :param order_line: order line number, Type: Integer
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        total_line = segment.split(":")
        total_line = total_line[1] if len(total_line) > 1 else 0
        if int(total_line) != order_line:
            message = 'Order Line not integrated properly, Please Check order line data in file.'
            if not is_cron:
                raise UserError(_(message))
            _logger.info(message)
            self.env['common.log.lines.ept'].create_avc_log_lines(message, common_log_book)
            return True
        return False

    def prepare_unt_segment(self, segment, total_segment, common_log_book, is_cron=False):
        """
           Used for prepare the segment
           :param segment: segment data
           :param total_segment: Contain total segments, Type: Integer
           :@author: Dipak Gogiya, 02/08/2020
           :return: Dict.
        """
        segments = segment.split("+")
        segments = segments[1]
        if int(segments) != total_segment:
            message = 'File not integrated properly, Please Check file data.'
            if not is_cron:
                raise UserError(_(message))
            _logger.info(message)
            self.env['common.log.lines.ept'].create_avc_log_lines(message, common_log_book)
            return True
        return False

    def reprocess_requisition_lines(self):
        """
            Usage: Used for set the product in the requisition order lines
            :@author: Dipak Gogiya, 02/08/2020
            :@task: 170072 - Update following things on V14 Vendor Central.
            :return: Boolean
        """
        amazon_product_dict = {}
        amazon_sale_requisition_lines = self.amazon_sale_requisition_line_ids.filtered(
            lambda requisition_order_line: not requisition_order_line.product_id)
        if amazon_sale_requisition_lines:
            query = """
                        SELECT 
                            amazon_sku, 
                            barcode, 
                            product_id 
                        FROM 
                            amazon_vendor_central_product_ept 
                        WHERE 
                            product_type = '%s' AND 
                            amazon_vendor_instance_id = %s
                    """ % (amazon_sale_requisition_lines[0].item_type, self.amazon_vendor_instance_id.id)
            self._cr.execute(query)
            amazon_products = self._cr.dictfetchall()
            for amazon_product in amazon_products:
                if amazon_product.get('amazon_sku', ''):
                    amazon_product_dict.update({amazon_product.get('amazon_sku'): amazon_product.get('product_id')})
                if amazon_product.get('barcode', ''):
                    amazon_product_dict.update({amazon_product.get('barcode'): amazon_product.get('product_id')})
            for amazon_sale_requisition_line in amazon_sale_requisition_lines:
                if amazon_product_dict.get(amazon_sale_requisition_line.amazon_edi_line_code):
                    requisition_product_details = {
                        'product_id': amazon_product_dict.get(amazon_sale_requisition_line.amazon_edi_line_code)}
                    amazon_sale_requisition_line.write(requisition_product_details)
        return True

    def update_product_availability(self):
        """
            Usage: Used for added the cancel out of stock in product availability
            automatically if the order quantity is more then on hand quantity
            :@author: Dipak Gogiya, 02/08/2020
            :@task: 170072 - Update following things on V14 Vendor Central.
            :return: Boolean
        """
        amazon_sale_requisition_lines = self.amazon_sale_requisition_line_ids.filtered(
            lambda requisition_order_line: requisition_order_line.product_id
                                           and requisition_order_line.order_qty > requisition_order_line.qty_available)
        if amazon_sale_requisition_lines:
            requisition_ids = '(' + str(amazon_sale_requisition_lines.ids).strip('[]') + ')'
            self._cr.execute(""" Update amazon_sale_requisition_line_ept set product_availability = '%s' 
            where id in %s""" % ('IR', requisition_ids))

    def unlink(self):
        for requisition in self:
            if requisition.state != 'draft':
                raise UserError(
                    "You can not delete the Sales requisition which is not in Draft state.")
        return super(AmazonSaleRequisition, self).unlink()
