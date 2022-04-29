""" Inherit the existing functionality and added the new functionality """
import logging
from odoo import models

_logger = logging.getLogger("Amazon Vendor Central Ept")


class AccountTax(models.Model):
    """
        Inherit the existing functionality and added the new functionality
    """
    _inherit = 'account.tax'

    def prepare_avc_invoice_line_tax_acknowledgment_data(self, acknowledgment_data, total_segment,
                                                         invoice_line, line_no, tax_list,
                                                         gst_dict, invoice_tax_rate):
        """
            Usage: Used for, Prepare the tax acknowledgment data based on invoice line
            :param acknowledgment_data: Invoice Acknowledgment Data
            :param total_segment: Total Number if segment
            :param invoice_line: account.move.line()
            :param line_no: Total number of lines
            :param tax_list: List of taxes
            :param gst_dict: GST Tax Dict
            :param invoice_tax_rate: Invoice Tax Rate
            :return: updated acknowledgment_data, total_segment, line_no, tax_list, gst_dict
        """
        account_move = invoice_line.move_id
        for account_tax in self:
            if account_tax.amount_type == 'group':
                for tax in account_tax.children_tax_ids:
                    acknowledgment_data, total_segment, gst_dict, tax_list, invoice_tax_rate = tax. \
                        prepare_avc_tag_segment_info(invoice_line, invoice_tax_rate, acknowledgment_data,
                                                     total_segment, tax_list, gst_dict)
                    line_no += 1
            else:
                acknowledgment_data, total_segment, gst_dict, tax_list, invoice_tax_rate = account_tax. \
                    prepare_avc_tag_segment_info(invoice_line, invoice_tax_rate, acknowledgment_data,
                                                 total_segment, tax_list, gst_dict)
                line_no += 1
        if not self:
            if account_move.currency_id.name == 'INR':
                acknowledgment_data += """TAX+7+GST+++:::0'"""
                total_segment += 1
            else:
                acknowledgment_data += """TAX+7+VAT+++:::0'"""
                total_segment += 1
            line_no += 1

        return acknowledgment_data, total_segment, line_no, tax_list, gst_dict, invoice_tax_rate

    def prepare_avc_tag_segment_info(self, invoice_line, invoice_tax_rate, acknowledgment_data,
                                     total_segment, tax_list, gst_dict):
        """
            Usage: Used for prepare the tax line items of invoice line
            :param invoice_line: account.move.line()
            :param invoice_tax_rate: Invoice Tax Rate, Type: Int
            :param acknowledgment_data: Invoice Acknowledgment Data
            :param total_segment: Total number of segment
            :param tax_list: List of taxes
            :param gst_dict: GST Tax Dict
            :return: updated acknowledgment_data, total_segment, gst_dict, tax_list
        """
        move = invoice_line.move_id
        tax_amount = self.amount
        tag = self.get_tax_tags(is_refund=False, repartition_type='tax')
        tax_tag = tag[0].tax_report_line_ids[0].name if tag and tag[0].tax_report_line_ids else ''
        tax_tag = tax_tag and ':::' + str(tax_tag)
        if tax_tag and move.currency_id.name == 'INR':
            tax_dict = {tax_tag: tax_amount}
            if tax_dict not in tax_list:
                tax_list.append(tax_dict)
            gst_tax = tax_tag + '_' + str(int(tax_amount)) + '_tax'
            gst_total = tax_tag + '_' + str(int(tax_amount)) + '_total'
            tax_price = invoice_line.price_subtotal * tax_amount / 100
            if not gst_dict.get(gst_tax):
                gst_dict.update({gst_tax: tax_price, gst_total: invoice_line.price_subtotal})
            else:
                existing_tax = float(gst_dict.get(gst_tax)) + tax_price
                existing_sub = float(gst_dict.get(gst_total)) + invoice_line.price_subtotal
                gst_dict.update({gst_tax: existing_tax, gst_total: existing_sub})
        invoice_tax_rate += tax_amount
        if move.currency_id.name == 'INR':
            acknowledgment_data += """TAX+7+GST%s+++:::%s+S'""" % (tax_tag, str(tax_amount))
            total_segment += 1
        else:
            acknowledgment_data += """TAX+7+VAT%s+++:::%s+S'""" % (tax_tag, str(int(tax_amount)))
            total_segment += 1

        return acknowledgment_data, total_segment, gst_dict, tax_list, invoice_tax_rate
