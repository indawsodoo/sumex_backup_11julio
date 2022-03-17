""" This file creating and managing the Amazon Requisition Order Lines functionality """
import logging
from datetime import datetime
from odoo import models, fields, api

_logger = logging.getLogger("Amazon Vendor Center")


class AmazonSaleRequisitionLine(models.Model):
    """
        Create and Manage the Amazon Requisition Order Lines Functionality
    """
    _name = 'amazon.sale.requisition.line.ept'
    _description = 'Amazon Sale Requisition Order Lines'

    @api.depends('product_id', 'amazon_sale_requisition_id.amazon_vendor_instance_id.warehouse_id')
    def _compute_qty_available(self):
        for requisition_line in self:
            requisition_line.qty_available = requisition_line.product_id. \
                with_context(
                warehouse=requisition_line.amazon_sale_requisition_id.amazon_vendor_instance_id.warehouse_id.id). \
                qty_available

    amazon_sale_requisition_id = fields.Many2one('amazon.sale.requisition.ept',
                                                 string='Requisition',
                                                 help='Amazon sale requisition', ondelete="cascade")

    product_id = fields.Many2one('product.product', string='Product', help='Product')
    order_qty = fields.Float(string='Order Quantity', help='Order Quantity')
    is_backorder = fields.Boolean(string='Backorder', help='Backorder')
    acknowledge_qty = fields.Float(string='Acknowledge Quantity', help='Acknowledge Quantity')
    backorder_qty = fields.Float(string='Backorder Quantity', help='Backorder Quantity')
    # unit_price = fields.Float(string='Price', help='Help Price')
    requisition_currency_id = fields.Many2one(related='amazon_sale_requisition_id.currency_id',
                                              string='Requisition Currency',
                                              readonly=True, required=True,
                                              help='Utility field to express amount currency')
    unit_price = fields.Monetary(string='Subtotal',
                                 currency_field='requisition_currency_id')
    delivery_date = fields.Date(string='Delivery Date', help='Delivery Date', readonly=True)
    max_delivery_date = fields.Date(string='Max Delivery Date', help='Max Delivery Date', readonly=True)
    amazon_edi_line_code = fields.Char('Amazon Line code')
    amazon_edi_line_code_type = fields.Selection([('barcode', 'Barcode'), ('sku', 'SKU')])
    product_availability = fields.Selection([('IA', 'Accepted'),
                                             ('IB', 'Backorder'),
                                             ('IR', 'Cancel : out of stock'),
                                             ('R2', 'Cancel invaild product information'),
                                             ('R3', 'Cancel : Not yet available/Discontinued/Cancelled')],
                                            string="Product Availability", default='IA')
    item_type = fields.Selection([('BP', 'BP'),
                                  ('EN', 'EN'),
                                  ('SA', 'SA')], string="Item Type")
    price_qualifier = fields.Selection([('NTP', 'NTP'),
                                        ('RTP', 'RTP')], string="Price Type Qualifier")
    qty_available = fields.Float(string="Quantity On Hand", digits='Product Unit of Measure',
                                 help="Onhand Quantity", compute=_compute_qty_available, store=True)

    def create_amazon_sale_requisition_lines(self, order_line_info, requisition_id, common_log_book, instance):
        """
            Used for creating the amazon requisition order lines based on order line info
            and attach those line with requisition record
            :param order_line_info: Order Line Info, Type: Dict
            :param requisition_id: amazon.sale.requisition.ept()
            :param common_log_book: common.log.book.ept()
            :param instance: amazon.vendor.instance()
            :@author: Dipak Gogiya, 02/12/2020
            :return: True
        """
        avc_product_ept_obj = self.env['amazon.vendor.central.product.ept']
        common_log_lines_obj = self.env['common.log.lines.ept']
        odoo_product = self.env['product.product']
        amazon_code, amazon_edi_line_code_type = '', ''
        for line_info in order_line_info.values():
            default_code = line_info.get('default_code', '')
            ean = line_info.get('ean', False)
            item_type = line_info.get('item_type', False)
            if not default_code and not ean:
                _logger.info("Skip Line: [{}] because Default Code and Barcode Not available".format(line_info))
                continue
            if default_code:
                odoo_product = avc_product_ept_obj. \
                    search_odoo_product_by_default_code(default_code, item_type, instance)
                amazon_code = default_code
                amazon_edi_line_code_type = 'sku'
            if ean:
                odoo_product = avc_product_ept_obj. \
                    search_odoo_product_by_default_ean(ean, item_type, instance)
                amazon_code = ean
                amazon_edi_line_code_type = 'barcode'

            line_values = self.prepare_requisition_line_values(line_info, amazon_code, amazon_edi_line_code_type,
                                                               requisition_id, odoo_product)
            _logger.info("Amazon Requisition Order Line Values Dict. : {}".format(line_values))
            self.create(line_values)
            if not odoo_product:
                product_info = "Internal Reference (SKU) : {}".format(
                    default_code) if default_code else "Ean (Barcode) : {}".format(ean)
                message = "Product not found with item_type : {}, ". \
                              format(item_type) + product_info
                _logger.info(message)
                common_log_lines_obj.create_avc_log_lines(message, common_log_book, default_code=default_code)

        return True

    def prepare_requisition_line_values(self, line_info, amazon_code, amazon_edi_line_code_type, requisition_id,
                                        odoo_product):
        """
            Used for prepare the requisition lines values for create the nre order line.
            :param line_info: Order Line Info, Type: Dict
            :param amazon_code: Internal Reference (SKU), Type: String
            :param amazon_edi_line_code_type: Amazon Edi line Code, Type: String.
            :param requisition_id: amazon.sale.requisition.ept()
            :param odoo_product: product.product()
            :@author: Dipak Gogiya, 02/12/2020
            :return: Dict.
        """
        return {
            'order_qty': line_info.get('qty', 0.0),
            'item_type': line_info.get('item_type', False),
            'acknowledge_qty': line_info.get('qty', 0.0),
            'product_availability': 'IA',
            'unit_price': float(line_info.get('price', 0.0)),
            'amazon_edi_line_code': amazon_code,
            'amazon_edi_line_code_type': amazon_edi_line_code_type,
            'delivery_date': requisition_id.delivery_date,
            'product_id': odoo_product.id,
            'max_delivery_date': requisition_id.max_delivery_date,
            'amazon_sale_requisition_id': requisition_id.id,
            'price_qualifier': line_info.get('price_qualifier', 'NTP')}

    def prepare_avc_acknowledgment_lines_data(self, po_ack_file_string, total_segment, common_log_book,
                                              amazon_products):
        """
            Used for prepare the acknowledgment lines data
            :param po_ack_file_string: acknowledgment data, Type: String
            :param total_segment: total number of segments, Type: Integer
            :param common_log_book: common.log.book.ept()
            :param amazon_products: Amazon Products
            :@author: Dipak Gogiya, 04/12/2020
            :return: updated -> po_ack_file_string, total_segment, line_no
        """
        tax_amount, line_no = 0.0, 0
        requisition = self[0].amazon_sale_requisition_id
        instance = requisition.amazon_vendor_instance_id
        amazon_edi_order_id = requisition.amazon_edi_order_id
        amz_avc_product_obj = self.env['amazon.vendor.central.product.ept']
        common_log_lines_obj = self.env['common.log.lines.ept']

        for req_order_line in self:
            line_no += 1
            acknowledge_qty = int(req_order_line.acknowledge_qty)
            backorder_qty = int(req_order_line.backorder_qty)

            # Search Amazon Product
            amazon_product = amazon_products.get(req_order_line.id)

            po_ack_file_string, total_segment, line_no = \
                req_order_line.prepare_avc_acknowledgment_lines_by_barcode_or_sku(
                    po_ack_file_string, line_no,
                    amazon_product.product_type, total_segment)

            if req_order_line.product_availability in ['IA'] and acknowledge_qty > 0.0 and backorder_qty == 0.0:
                po_ack_file_string += "QTY+12:%s'" % (acknowledge_qty)
                total_segment += 1
            elif backorder_qty > 0.0 and req_order_line.product_availability == 'IB':
                po_ack_file_string, total_segment = \
                    req_order_line.prepare_avc_acknowledgment_lines_of_backorder(po_ack_file_string, total_segment,
                                                                                 acknowledge_qty, backorder_qty)
            elif req_order_line.product_availability in ['R2', 'R3']:
                po_ack_file_string += "QTY+182:%s'" % (int(req_order_line.order_qty))
                total_segment += 1
            elif req_order_line.product_availability in ['IR']:
                po_ack_file_string += "QTY+185:%s'" % (int(req_order_line.order_qty))
                total_segment += 1

            po_ack_file_string += "PRI+AAA:%s:CT:%s'" % (req_order_line.unit_price,
                                                         req_order_line.price_qualifier or 'NTP')
            total_segment += 1
            if tax_amount > 0.0:
                po_ack_file_string += "TAX+7+VAT+++:::%s'" % (str(tax_amount))
                total_segment += 1
            message = 'Sent Acknowledgement For Requisition Name :  [%s]' % (amazon_edi_order_id or '')
            _logger.info(message)
        return po_ack_file_string, total_segment, line_no

    def prepare_avc_acknowledgment_lines_by_barcode_or_sku(self, po_ack_file_string,
                                                           line_no, product_type,
                                                           total_segment):
        """
            Type: Selection
            :param po_ack_file_string: acknowledgment data, Type: String
            :param line_no: Requisition order line number, Type: Integer
            :param product_type: Product Type
            :param total_segment: total number of segments, Type: Integer
            :@author: Dipak Gogiya, 02/12/2020
            :return: updated -> po_ack_file_string, total_segment, line_no
        """
        if self.amazon_edi_line_code_type == 'barcode':
            po_ack_file_string += "LIN+%s++%s:%s'" % (
                str(line_no), self.amazon_edi_line_code, product_type)
            total_segment += 1
        if self.amazon_edi_line_code_type == 'sku':
            po_ack_file_string += "LIN+%s'" % (str(line_no))
            total_segment += 1
            po_ack_file_string += "PIA+5+%s:%s'" % (self.amazon_edi_line_code, product_type)
            total_segment += 1
        return po_ack_file_string, total_segment, line_no

    def prepare_avc_acknowledgment_lines_of_backorder(self, po_ack_file_string, total_segment,
                                                      acknowledge_qty, backorder_qty):
        """
            Used for prepare the acknowledgment lines of back order
            :param po_ack_file_string: acknowledgment data, Type: String
            :param total_segment: total number of segments, Type: Integer
            :param acknowledge_qty: Acknowledgement Quantity
            :param backorder_qty: Backorder Quantity
            :@author: Dipak Gogiya, 02/12/2020
            :return: updated acknowledgment data
        """
        backorder_date = self.max_delivery_date.strftime("%Y%m%d")
        po_ack_file_string += "QTY+12:%s'" % (int(acknowledge_qty))
        total_segment += 1
        po_ack_file_string += "QTY+83:%s'" % (int(backorder_qty))
        total_segment += 1
        po_ack_file_string += "DTM+11:%s:102'" % (backorder_date)
        total_segment += 1
        return po_ack_file_string, total_segment

    def prepare_asn_lines_data(self, file_asn_string, total_segment, order_lines_info, line_no=0):
        """
            Used for prepare the amazon advance shipment notice lines data
            :param file_asn_string:  advance shipment notice data, Type: String
            :param total_segment: total number of segments, Type: Integer
            :param order_lines_info: Line info of picking, Type: Char
            :param line_no: Total Number of lines, Type: Integer
            :@author: Dipak Gogiya, 07/12/2020
            :return: Updated -> po_asn_file_string, total_segment, line_no
        """
        for order_line in order_lines_info:
            line_no += 1
            if order_line.get('amazon_edi_code_type') == 'barcode':
                file_asn_string += "LIN+%s++%s:EN'" % (str(line_no), order_line.get('amazon_edi_code'))
                total_segment += 1
            if order_line.get('amazon_edi_code_type') == 'sku':
                file_asn_string += "LIN+%s'" % (str(line_no))
                total_segment += 1
                file_asn_string += "PIA+5+%s:SA'" % (order_line.get('amazon_edi_code', ''))
                total_segment += 1
            """
                Usage : Below Segment "QTY+12"
                Code        Name
                12          Despatch quantity
            """
            file_asn_string += "QTY+12:%s'" % (int(order_line.get('qty_done', 0)))
            total_segment += 1
            file_asn_string += "RFF+ON:%s'" % (order_line.get('amazon_edi_order_id', ''))
            total_segment += 1
            if order_line.get('expiry_date', ''):
                expiry_date = datetime.strftime(
                    datetime.strptime(order_line.get('expiry_date'), '%Y-%m-%d %H:%M:%S'),
                    "%Y%m%d")
                file_asn_string += "PCI+17'"
                total_segment += 1
                file_asn_string += "DTM+36:%s:102'" % (expiry_date)
                total_segment += 1
                """
                    Usage : Below Segment "GIN+BX"
                    Code        Name
                    BX          Batch Number
                """
                file_asn_string += "GIN+BX+%s'" % (str(order_line.get('lot_id', 0)))
                total_segment += 1

            message = 'Sent Advance Shipment Notice for requisition name %s' % \
                      (order_line.get('amazon_edi_order_id', '') or '')
            _logger.info(message)
        return file_asn_string, total_segment

    def prepare_inventory_and_stock_edi_lines_segment_data(self, file_inventory, total_segment, product_lines,
                                                           instance):
        """
            Used for prepare the file inventory edi lines data.
            :param file_inventory: Export Inventory and Cost Report data, Type: String
            :param total_segment: total number of segments, Type: Integer
            :param product_lines: product info, Type: Dict
            :param instance: amazon.vendor.instance()
            :return: Updated, file_inventory, total_segment
        """
        amz_avc_product_obj = self.env['amazon.vendor.central.product.ept']
        odoo_product_obj = self.env['product.product']
        currency_name = instance.pricelist_id.currency_id.name
        line_no = 0
        for line in product_lines:
            product_qty = line.get('product_qty', 0)
            price = line.get('price', 0)
            line_no += 1
            odoo_product = odoo_product_obj.browse(line.get('product_id'))
            amazon_product = amz_avc_product_obj. \
                search_avc_existing_amazon_product(odoo_product, instance)
            product_type = amazon_product.product_type

            file_inventory += """LIN+%s++%s:%s'""" % \
                              (str(line_no), amazon_product.amazon_sku, str(product_type))
            total_segment += 1

            file_inventory += """QTY+145:%s'""" % (str(product_qty))
            total_segment += 1

            file_inventory += """PRI+AAA:%s'""" % (str(price))
            total_segment += 1

            file_inventory += """CUX+2:%s:10'""" % (currency_name)
            total_segment += 1

        return file_inventory, total_segment

    # def action_avc_product_forecast_report(self):
    #     self.ensure_one()
    #     action = self.product_id.action_product_forecast_report()
        # warehouse = self.amazon_sale_requisition_id.amazon_vendor_instance_id.warehouse_id
        # action['context'] = {'warehouse': warehouse.id} if warehouse else {}
        # return action
