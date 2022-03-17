""" Inherit the existing functionality and added the new functionality """
import time
import logging
from odoo import models, fields, _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger("Amazon Vendor Central Ept")


class AccountMove(models.Model):
    """
        Inherit the existing functionality and added the new functionality
    """
    _inherit = 'account.move'

    is_amazon_edi_invoice = fields.Boolean(string='Is Amazon Invoice', default=False)
    exported_to_edi = fields.Boolean(string='Invoice Exported to Amazon', copy=False)

    def send_avc_invoices_to_amazon(self, requisition, is_cron=False):
        """
            Send Invoice to Vendor central for edi fact format.
            :return:True
        """
        _logger.info("Invoice Export To The Amazon Vendor Central Process Started...!")
        attachments = self.env['ir.attachment']
        instance = requisition.amazon_vendor_instance_id

        # Create the new JOB.
        common_log_book = self.env['common.log.book.ept'].create_avc_common_log('amazon.sale.requisition.ept',
                                                                                'export',
                                                                                "Export Invoices To Amazon Vendor Central Job",
                                                                                requisition)

        # Get Ftp Server.
        ftp_server = self.env['ftp.server.ept'].get_ftp_server(instance, is_sender_ftp_server=True, is_cron=is_cron)

        if isinstance(ftp_server, str):
            self.env['common.log.lines.ept'].create_avc_log_lines(ftp_server, common_log_book)
            return False

        directory_id = ftp_server.default_upload_dir_id
        _logger.info("FTP Directory : %s, Directory Path : %s" % (directory_id.name, directory_id.path))

        # Used for checking the mismatch data
        if self.check_avc_mismatch_details_for_export_invoice(requisition, ftp_server, common_log_book, is_cron=is_cron):
            return False

        price_qualifier_values = {requisition_line.product_id.id: requisition_line.price_qualifier for requisition_line
                                  in requisition.amazon_sale_requisition_line_ids.filtered(
                lambda requisition_line: requisition_line.product_availability in ['IA', 'IB'])}

        for account_move in self:
            invoice_lines = account_move.invoice_line_ids.filtered(
                lambda invoice_line: invoice_line.product_id and invoice_line.product_id.type != 'service')

            is_mismatch_details = account_move.check_avc_invoice_with_lines_mismatch_details(common_log_book,
                                                                                             invoice_lines)

            # Skip to export the invoice to the Amazon vendor central if any mismatch data found.
            if is_mismatch_details:
                continue

            # Prepare the Invoice Acknowledgment Data with its Invoice Line Item and Invoice lines taxes
            invoice_acknowledgment_data = account_move.prepare_avc_invoice_edi_file_data(requisition, instance,
                                                                                         invoice_lines,
                                                                                         price_qualifier_values)
            # Used for, create the new attachment and uploading the file to the FTP
            attachment, file_upload_successfully = attachments.create_attachment_and_upload_file_to_ftp(
                invoice_acknowledgment_data,
                ftp_server, instance,
                ftp_server.invoice_file_export_prefix,
                directory_id, common_log_book=common_log_book)
            attachments += attachment

            if file_upload_successfully:
                # Set True once the invoice exported successfully to the amazon advantage vendor central.
                account_move.write({'exported_to_edi': True})

        if attachments and requisition:
            common_log_book.message_post(body=_("<b>The Invoice files</b>"),
                                         attachment_ids=attachments.ids)
            requisition.message_post(body=_("<b>The Invoice files</b>"),
                                     attachment_ids=attachments.ids)
        if self and all(self.mapped('exported_to_edi')) and requisition.sale_order_id.invoice_status == 'invoiced':
            requisition.state = 'done'
        # Unlink the job if no any log lines created.
        if not is_cron and common_log_book.log_lines:
            return common_log_book.get_action_for_avc_operations(
                external_id='amazon_vendor_central_ept.action_vendor_common_log_book_ept',
                form_view_ref='common_connector_library.action_common_log_book_ept_form',
                record_ids=common_log_book)
        if not common_log_book.log_lines:
            common_log_book.unlink()

        _logger.info("Invoice Export To The Amazon Advantage Process Started...!")
        return True

    def check_avc_mismatch_details_for_export_invoice(self, requisition, ftp_server, common_log_book, is_cron):
        """
            Usage: Used for, checking the required field values filled or not for exporting the
            invoice to the amazon vendor central
            :param requisition: amazon.sale.requisition.ept()
            :param ftp_server: ftp.server.ept()
            :param common_log_book: common.log.book.ept()
            :param is_cron: Boolean
            :return: Boolean
        """
        message = "Mismatch Details: \n    "
        mismatch_details = False
        if not requisition.sender_id or not requisition.recipient_id:
            message += f"Sender or recipient identifier not found of Requisition : [{requisition.name}]!"
            mismatch_details = True
            if not is_cron:
                raise Warning(_(message))

        if not requisition.association_code:
            message += f"Association Code not found of Requisition : [{requisition.name}]!"
            mismatch_details = True
            if not is_cron:
                raise Warning(_(message))

        if not requisition.invoice_party_id:
            message += f"Invoice Party ID not found of Requisition : [{requisition.name}]!"
            mismatch_details = True
            if not is_cron:
                raise Warning(_(message))

        if not requisition.vat_number:
            message += f"VAt Number not found of Requisition : [{requisition.name}]!"
            mismatch_details = True
            if not is_cron:
                raise Warning(_(message))

        if not ftp_server.invoice_file_export_prefix:
            field_string = ftp_server._fields['invoice_file_export_prefix'] and ftp_server._fields[
                'invoice_file_export_prefix'].string
            message += "Please set the {}! \n - Goto : Configurations -> SFTP -> {} -> {}".format(field_string,
                                                                                                  ftp_server.display_name,
                                                                                                  field_string)
            mismatch_details = True
            if not is_cron:
                raise UserError(_(message))

        if mismatch_details and is_cron:
            self.env['common.log.lines.ept'].create_avc_log_lines(message, common_log_book)
        return mismatch_details

    def prepare_avc_invoice_edi_file_data(self, requisition, instance, invoice_lines, price_qualifier_values):
        """

        :param requisition: amazon.sale.requisition.ept()
        :param instance: amazon.vendor.instance
        :param invoice_lines: account.move.line()
        :param price_qualifier_values: Price Qualifier, such as NTP or RTP
        :return: invoice_acknowledgment_data
        """
        _logger.info("Invoice Acknowledgment Data Process Started...!")
        invoice_seq = self.env['ir.sequence'].next_by_code('amazon.edi.invoice.message.number')

        # Prepare the Invoice Acknowledgment Data
        invoice_acknowledgment_data, total_segment = self.prepare_avc_invoice_acknowledgment_data(
            requisition, instance, invoice_seq)

        # Prepare the Invoice Lines With Tax Acknowledgment Data
        invoice_acknowledgment_data, total_segment, line_no, tax_list, gst_dict, invoice_tax_rate = \
            invoice_lines.prepare_avc_invoice_lines_acknowledgment_data(invoice_acknowledgment_data, requisition,
                                                                        instance, total_segment,
                                                                        price_qualifier_values)

        # Prepare the Invoice Acknowledgment Data of Ending Segments
        invoice_acknowledgment_data = self.prepare_remaining_invoice_acknowledgment_data(
            invoice_acknowledgment_data, total_segment, line_no,
            tax_list, gst_dict, invoice_tax_rate, invoice_seq)
        _logger.info("Invoice Acknowledgment Data Process Started...!")
        return invoice_acknowledgment_data

    def check_avc_invoice_with_lines_mismatch_details(self, common_log_book, invoice_lines):
        """
            Usage: Check required field values and mismatch data.
            :param job: common.log.lines.ept()
            :param invoice_lines: account.move.line()
            @Author: Dipak Gogiya
            :return: Boolean
        """
        common_log_lines_obj = self.env['common.log.lines.ept']
        is_mismatch_details = False
        # Check invoice is validated or not.
        if self.state != 'posted':
            message = "The invoice : [{}] Must be Validated for Export to Amazon Vendor Central".format(self.name)
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
            _logger.info(message)
            is_mismatch_details = True

        if not invoice_lines:
            message = "No any Stockable Product is set in the invoice lines of Invoice : [{}]!".format(
                self.name)
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
            _logger.info(message)
            is_mismatch_details = True

        if not self.company_id.vat:
            message = "Vat is not set in the Company of Invoice : [{}]".format(self.name)
            common_log_lines_obj.create_avc_log_lines(message, common_log_book)
            _logger.info(message)
            is_mismatch_details = True

        return is_mismatch_details

    def prepare_avc_invoice_acknowledgment_data(self, requisition, instance, invoice_seq):
        """
            Usage: Used for, prepare invoice acknowledgment data for sending to the
            amazon vendor central
            :param requisition: amazon.sale.requisition.ept()
            :param instance: amazon.vendor.instance()1
            :return: invoice_acknowledgment_data
        """
        total_segment = 0

        invoice_acknowledgment_data = """UNB+%s:2+%s:%s+%s:%s+%s:%s+%s+++++EANCOM'""" % (
            requisition.syntax_identifier, requisition.recipient_id or '',
            instance.avc_amazon_qualifier, requisition.sender_id or '',
            instance.avc_amazon_qualifier, time.strftime("%y%m%d"), time.strftime("%H%M"),
            str(invoice_seq))
        total_segment += 1

        invoice_acknowledgment_data += """UNH+1+INVOIC:D:96A:UN:%s'""" % (requisition.association_code)
        total_segment += 1

        inv_no = self.name[self.name.rfind('/') + 1:] if self.name else ''
        invoice_acknowledgment_data += """BGM+380+%s+9'""" % (str(inv_no))
        total_segment += 1

        invoice_acknowledgment_data += """DTM+137:%s:185'""" % (time.strftime("%Y%m%d"))
        total_segment += 1

        invoice_acknowledgment_data += """DTM+35:%s:102'""" % (time.strftime("%Y%m%d"))
        total_segment += 1

        invoice_acknowledgment_data += """FTX+SUR+1++Intra-EU supply of goods+EN'"""
        total_segment += 1

        # Prepare the Supplier Segment Data of Invoice
        invoice_acknowledgment_data, total_segment = self.prepare_avc_invoice_supplier_acknowledgment_data(
            invoice_acknowledgment_data, instance, total_segment)

        # Prepare the Supplier Segment Data of Invoice
        invoice_acknowledgment_data, total_segment = self.prepare_avc_invoice_delivery_address_acknowledgment(
            invoice_acknowledgment_data, requisition, total_segment)

        invoice_acknowledgment_data += """CUX+2:%s:4'""" % (self.currency_id.name or '')
        total_segment += 1

        invoice_acknowledgment_data += """PAT+1++5::D:30'"""  # payment Term 30 days Net
        total_segment += 1

        return invoice_acknowledgment_data, total_segment

    def prepare_avc_invoice_supplier_acknowledgment_data(self, invoice_acknowledgment_data, instance, total_segment):
        """
            Usage: Used for, prepare the invoice supplier acknowledgment data
            :param invoice_acknowledgment_data: invoice acknowledgment data
            :param instance: amazon.vendor.instance()
            :param total_segment: Total number of segment of invoice acknowledgment data
            :return: updated invoice_acknowledgment_data
        """
        invoice_company = self.company_id
        # Supplier Segment
        company_name = invoice_company.name.replace("'", '') or ''
        company_street = invoice_company.street.replace("'", '') if invoice_company \
            else "10 passage de l'industrie".replace("'", '')
        company_city = invoice_company.city.replace("'", '') or ''
        company_zip = invoice_company.zip.replace("'", '') or ''
        country_code = invoice_company.country_id.code if invoice_company.country_id else "FR"

        invoice_acknowledgment_data += """NAD+SU+%s::9++%s+%s+%s++%s+%s'""" % (
            instance.supplier_id or '', company_name, company_street, company_city,
            company_zip or '', country_code)
        total_segment += 1

        # MGC(Supplier) VAT Number
        invoice_acknowledgment_data += """RFF+VA:%s'""" % (invoice_company.vat or '')
        total_segment += 1

        return invoice_acknowledgment_data, total_segment

    def prepare_avc_invoice_delivery_address_acknowledgment(self, invoice_acknowledgment_data, requisition,
                                                            total_segment):
        """
            Usage: Used for, prepare the Invocie and Delivery Address acknowledgment data
            :param invoice_acknowledgment_data: invoice acknowledgment data
            :param requisition: amazon.sale.requisition.ept()
            :param total_segment: Total number of segment of invoice acknowledgment data
            :param requisition: amazon.sale.requisition.ept()
            :return: updated invoice_acknowledgment_data
        """
        invoice_address_id = self.partner_id

        invoice_acknowledgment_data += """NAD+DP+%s::9+++++++%s'""" % (
            requisition.delivery_party_id or '', invoice_address_id.country_id.code)
        total_segment += 1

        invoice_acknowledgment_data += "NAD+IV+%s::9++%s:%s+%s+%s++%s+%s'" % (
            requisition.invoice_party_id, invoice_address_id.name,
            invoice_address_id.country_id.name,
            invoice_address_id.street, invoice_address_id.city,
            invoice_address_id.zip,
            invoice_address_id.country_id.code)
        total_segment += 1

        invoice_acknowledgment_data += """RFF+VA:%s'""" % (requisition.vat_number or '')
        total_segment += 1

        return invoice_acknowledgment_data, total_segment

    def prepare_remaining_invoice_acknowledgment_data(self, acknowledgment_data, total_segment, line_no, tax_list,
                                                      gst_dict, invoice_tax_rate, invoice_seq):
        """
            Usage: Prepare the Remaining Invoice Acknowledgment Data of Ending Segments
            :param acknowledgment_data: Invoice Acknowledgment Data
            :param total_segment: Total number of segment
            :param line_no: Total Number of invoice and its tax lines segments
            :param tax_list: List of taxes
            :param gst_dict: GST Tax Dict
            :param invoice_seq: Invoice Sequence
            :param invoice_tax_rate: Invoice Tax Rate
            :return:
        """
        currency_code = self.currency_id.name
        acknowledgment_data += """UNS+S'"""
        total_segment += 1
        acknowledgment_data += """CNT+2:%s'""" % (str(line_no - 1))
        total_segment += 1
        acknowledgment_data += """MOA+77:%s:%s:4'""" % (str(self.amount_total), str(
            currency_code))  # Whole Invoice Amount total with tax included
        total_segment += 1
        if currency_code == 'INR':
            for taxes in tax_list:
                for tax, tax_rate in taxes.items():
                    amt_tax = gst_dict.get(tax + '_' + str(int(tax_rate)) + '_tax')
                    amt_total = gst_dict.get(tax + '_' + str(int(tax_rate)) + '_total')
                    acknowledgment_data += """TAX+7+GST%s+++:::%s'""" % (tax, str(int(tax_rate)))
                    acknowledgment_data += """MOA+124:%s:%s:4'""" % (
                        str(amt_tax), str(currency_code))  # Tax Amount
                    acknowledgment_data += """MOA+125:%s:%s:4'""" % (
                        str(amt_total), str(currency_code))  # Untaxed Amount
                    total_segment += 3
        else:
            acknowledgment_data += """TAX+7+VAT+++:::%s'""" % (str(int(
                invoice_tax_rate)))  # Whole invoice Tax Rate
            acknowledgment_data += """MOA+124:%s:%s:4'""" % (
                str(self.amount_tax), str(currency_code))  # Tax Amount
            acknowledgment_data += """MOA+125:%s:%s:4'""" % (
                str(self.amount_untaxed), str(currency_code))  # Untaxed Amount
            total_segment += 3

        acknowledgment_data += """UNT+%s+1'""" % (str(total_segment))
        acknowledgment_data += """UNZ+1+%s'""" % (str(invoice_seq))

        return acknowledgment_data
