""" Inherit the existing functionality and added the new functionality """
import logging
from odoo import models

_logger = logging.getLogger("Amazon Vendor Central Ept")


class AccountMoveLine(models.Model):
    """
        Inherit the existing functionality and added the new functionality
    """
    _inherit = 'account.move.line'

    def prepare_avc_invoice_lines_acknowledgment_data(self, acknowledgment_data, requisition,
                                                      instance, total_segment,
                                                      price_qualifier_values):
        """
            Usage: Used for, prepare the invoice acknowledgment lines with tax info and return it
            :param acknowledgment_data: invoice acknowledgment data
            :param requisition: amazon.sale.requisition.ept()
            :param instance: amazon.vendor.instance()
            :param total_segment: Total number of segment
            :param price_qualifier_values: Price Qualifier, such as NTP or RTP
            :return: updated acknowledgment_data
        """
        _logger.info("Invoice Lines segments preparation process started...!")
        vendor_central_product_obj = self.env['amazon.vendor.central.product.ept']
        tax_list, gst_dict, invoice_tax_rate, line_no = [], {}, 0, 1
        for invoice_line in self:
            amazon_product = vendor_central_product_obj.search_avc_existing_amazon_product \
                (invoice_line.product_id, instance)
            price_qualifier = 'NTP'
            if invoice_line.product_id.id in price_qualifier_values:
                price_qualifier = price_qualifier_values.get(invoice_line.product_id.id)
            acknowledgment_data, total_segment, line_no = invoice_line. \
                prepare_avc_invoice_line_item_ack_data(amazon_product, acknowledgment_data,
                                                       total_segment, price_qualifier, line_no)
            # Order Name
            acknowledgment_data += """RFF+ON:%s'""" % (requisition.amazon_edi_order_id)
            total_segment += 1

            # Prepare the invoice line taxes segments.
            acknowledgment_data, total_segment, line_no, tax_list, gst_dict, invoice_tax_rate = \
                invoice_line.tax_ids.prepare_avc_invoice_line_tax_acknowledgment_data \
                    (acknowledgment_data, total_segment, invoice_line, line_no, tax_list,
                     gst_dict, invoice_tax_rate)
        _logger.info("Invoice Lines segments preparation process Ended...!")

        return acknowledgment_data, total_segment, line_no, tax_list, gst_dict, invoice_tax_rate

    def prepare_avc_invoice_line_item_ack_data(self, amazon_product, acknowledgment_data,
                                               total_segment, price_qualifier, line_no):
        """
            Usage: Used for, prepare the invoice acknowledgment line and return it
            :param amazon_product: amazon.vendor.central.product.ept()
            :param acknowledgment_data: Invoice Acknowledgment Data
            :param total_segment: Total number of segment
            :param price_qualifier: Price Qualifier, such as NTP or RTP
            :param line_no: Total Line number of invoice line acknowledgment data
            :return: updated acknowledgment_data, total_segment, line_no
        """
        product_id = self.product_id

        if amazon_product.product_type == 'EN':
            acknowledgment_data += """LIN+%s++%s:EN'""" % (str(line_no),
                                                           amazon_product.barcode or '')
            total_segment += 1
        else:
            acknowledgment_data += """LIN+%s'""" % (str(line_no))
            total_segment += 1
            acknowledgment_data += """PIA+5+%s:%s'""" % (product_id.default_code or '',
                                                         amazon_product.product_type)
            total_segment += 1

        acknowledgment_data += """QTY+47:%s'""" % (int(self.quantity) or 0)
        total_segment += 1

        currency_code = self.currency_id.name
        acknowledgment_data += """MOA+203:%s:%s:4'""" % (self.price_subtotal,
                                                         currency_code)  # Invoice Line Subtotal.
        total_segment += 1

        acknowledgment_data += """PRI+AAA:%s:CT:%s'""" % (
            str(self.price_unit), price_qualifier or 'NTP')  # Net Price Unit
        total_segment += 1

        return acknowledgment_data, total_segment, line_no
