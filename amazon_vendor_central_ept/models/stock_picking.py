""" This file inherit the existing functionality and added the new functionality """
import time
import logging
import itertools as it
from dateutil.relativedelta import relativedelta
from odoo import models, fields

_logger = logging.getLogger("Amazon Vendor Central Ept")


class StockPicking(models.Model):
    """
        Inherit the existing functionality and added the new functionality
    """
    _inherit = 'stock.picking'

    is_amazon_vendor_central_picking = fields.Boolean(string='Is Amazon Picking')
    amazon_vendor_order_id = fields.Many2one('amazon.sale.requisition.ept',
                                             string='Amazon Vendor Order Reference',
                                             ondelete='cascade')
    amazon_vendor_instance_id = fields.Many2one('amazon.vendor.instance', string='Amazon Instance',
                                                related="amazon_vendor_order_id.amazon_vendor_instance_id",
                                                store=True)
    bol_number = fields.Char(string='Bill of Lading Number')
    sscc_code = fields.Char(string='Serial Shipping Container Code', copy=False)
    shipment_notice_sent = fields.Boolean(string="Shipment Notice Send", default=False, copy=False)

    # amazon_order_ack_uploaded = fields.Boolean(related='sale_id.amazon_order_ack_uploaded',
    #                                            string='Amazon order Acknowledgement Uploaded')
    code = fields.Selection(related="picking_type_id.code", string='Code', readonly=True)

    def _get_package_qty(self, package):
        qty = 0
        for l in self.move_line_ids:
            if l.product_id in package.quant_ids.mapped('product_id')
        return sum([l.quantity for l in package.quant_ids])

    def prepare_asn_data(self):
        """"
            Usage: Prepare the Advance Shipment Notice EDI Data for sending to the amazon vendor central
            :return EDI Segments Data
        """
        _logger.info("Advance Shipment Notice Data File Preparation Process Started!")
        total_segment = 0
        requisition = self.amazon_vendor_order_id
        instance = requisition.amazon_vendor_instance_id

        # Write the bol_number in the picking
        bol_number = self.bol_number
        if not bol_number:
            bol_number_seq = self.env['ir.sequence'].next_by_code('amazon.edi.bol.number')
            bol_number = str(requisition.avc_vendor_code) + str(bol_number_seq)
        self.write({'bol_number': bol_number})

        amazon_edi_order_id = str(requisition.amazon_edi_order_id) or ''
        seq = self.env['ir.sequence'].next_by_code('amazon.edi.order.dispatch.advice')
        seq_interchange = self.env['ir.sequence'].next_by_code('amazon.edi.ship.message.trailer')

        file_asn_string = "UNB+UNOC:2+%s:%s+%s:%s+%s:%s+%s+++++EANCOM'" % (
            requisition.recipient_id or '', instance.avc_amazon_qualifier,
            requisition.sender_id or '', instance.avc_amazon_qualifier, time.strftime("%y%m%d"),
            time.strftime("%H%M"), str(seq_interchange))
        total_segment += 1

        file_asn_string += "UNH+%s+DESADV:D:96A:UN:EAN005'" % (str(seq))
        total_segment += 1

        """
            below segment 'BGM+351 in that segment last value 9 is the Code indicating the function of the message.'
            Code        Name
            9           Original
            5           Replace
        """
        file_asn_string += "BGM+351+%s+9'" % ("DES" + amazon_edi_order_id)
        total_segment += 1

        date_done = self.scheduled_date.strftime("%Y%m%d")
        date_arrival = self.scheduled_date + relativedelta(days=instance.order_dispatch_lead_time)
        date_arrival = date_arrival.strftime("%Y%m%d")

        # 11 means Order Dispatch date and or time and 102 = CCYYMMDD
        file_asn_string += "DTM+11:%s:102'" % (date_done)
        total_segment += 1

        """
          Usage of codes of below segment 'DTM+132'
          Code        Name
          132         Delivery date/time, estimated
          17          Arrival date/time, estimated
        """
        file_asn_string += "DTM+132:%s:102'" % (date_arrival)  # 102 = CCYYMMDD
        total_segment += 1

        """ 137 = Document/message date/time """
        file_asn_string += "DTM+137:%s:102'" % (time.strftime("%Y%m%d"))
        total_segment += 1

        """
            Usage of codes of below segment 'RFF+BM'
            Code        Name
            BM          Bill of lading number
            DQ          Delivery note number
        """
        file_asn_string += "RFF+BM:%s'" % (bol_number)
        total_segment += 1

        """
            This segment is used to provide references that apply to the whole transaction.
            Usage of codes of below segment 'RFF+ON'
            Code        Name
            ON          Order number (purchase)
        """
        file_asn_string += "RFF+ON:%s'" % (amazon_edi_order_id)
        total_segment += 1

        file_asn_string += "NAD+DP+%s::9+++++++%s'" % (
            requisition.delivery_party_id or '', requisition.country_code or '')
        total_segment += 1

        file_asn_string += "NAD+SU+%s::9'" % (instance.supplier_id or '')
        total_segment += 1

        warehouse = requisition.sale_order_id.warehouse_id
        file_asn_string += "NAD+SF+%s::9++++++%s+%s'" % (
            instance.amazon_gln_number or '', warehouse.partner_id.zip,
            warehouse.partner_id.country_id.code)
        total_segment += 1

        file_asn_string += "CPS+1'"  # Define Entire shipment and represents the highest hierarchical level
        total_segment += 1

        """
            Usage : Coded description of the form in which goods are presented.
            Usage of codes of below segment 'RFF+ON'
            201 = ISO EURO pallet
            202 = UK industrial size pallets (might only be applicable for UK)
        """
        # file_asn_string += "PAC+%s++201'" % (
        #     str(no_of_pallet))  # Number of pallets
        # total_segment += 1

        # file_asn_string += "PAC+%s++PK'" % (
        #     str(no_of_package))  # Number of carton in One shipment [PK = carton]
        # total_segment += 1
        if instance.is_use_packages and self.mapped('package_ids'):
            packages_info = self.prepare_packages_info(requisition)
            file_asn_string, total_segment = self.prepare_packages_acknowledgment_data(file_asn_string, total_segment,
                                                                                       packages_info, requisition)
        else:
            # Prepare the advance shipment notice line items data
            prepare_order_lines_info = self.prepare_order_line_info(requisition)

            file_asn_string += "CPS+%s+1'" % (str(0))  # First packing unit
            total_segment += 1
            file_asn_string += "PAC+1+:52+PK'"
            total_segment += 1
            file_asn_string += "PCI+33E'"
            total_segment += 1
            file_asn_string += "GIN+BJ+%s'" % (str(self.sscc_code))
            total_segment += 1

            file_asn_string, total_segment = requisition.amazon_sale_requisition_line_ids. \
                prepare_asn_lines_data(file_asn_string, total_segment, prepare_order_lines_info)

        file_asn_string += "UNT+%s+%s'" % (str(total_segment), str(seq))
        file_asn_string += "UNZ+1+%s'" % (str(seq_interchange))

        _logger.info("Total Segments : {}".format(total_segment))
        _logger.info("Advance Shipment Notice Data File Preparation Process Started!")
        return file_asn_string

    def prepare_packages_info(self, requisition):
        """
            Prepare the Package Information
            :param requisition: get the number of packages
            :@task:
            :@author: Dipak Gogiya, 30/12/2020
            :return: order line info, number of pallet or carton and number of package.
        """
        order_line_info = {}
        stock_move_line_obj = self.env['stock.move.line']
        for package in self.mapped('package_ids'):
            package_info = {
                'height': package.packaging_id.height or 0,
                'width': package.packaging_id.width or 0,
                'length': package.packaging_id.packaging_length or 0,
            }
            stock_move_lines = stock_move_line_obj.search([('result_package_id', '=', package.id),
                                                           ('picking_id', '=', self.id)])
            package_lines = stock_move_lines and self.prepare_order_line_info(requisition, stock_move_lines)
            if order_line_info.get(package.name):
                order_line_info.update({package.name: {'package_lines': package_lines,
                                                       'package_info': package_info}})
            else:
                order_line_info[package.name] = {'package_lines': package_lines,
                                                 'package_info': package_info}
        return order_line_info

    def prepare_order_line_info(self, requisition, stock_move_lines=None):
        """
            Used for prepare the order line info for sending the amazon vendor central
            :param requisition: amazon.sale.requisition.ept()
            :return: order_line_info, Type: List of Dict
        """
        stock_move = self.env['stock.move']
        order_lines = []
        amazon_edi_order_id = requisition.amazon_edi_order_id
        amazon_requisition_lines = {requisition_line.product_id.id: requisition_line
                                    for requisition_line in requisition.amazon_sale_requisition_line_ids.filtered(
                lambda req_order_line: req_order_line.product_id and req_order_line.acknowledge_qty > 0)}
        moves_with_done_qty_info = self.get_avc_picking_product_with_qty_info(self.move_lines)
        for move_id in moves_with_done_qty_info:
            move_id = stock_move.browse(move_id)
            requisition_line = amazon_requisition_lines.get(move_id.sale_line_id.product_id.id)
            order_line = {
                'amazon_edi_code': requisition_line.amazon_edi_line_code,
                'amazon_edi_code_type': requisition_line.amazon_edi_line_code_type,
                'qty_done': moves_with_done_qty_info[move_id.id],
                'product_id': move_id.product_id.id,
                'amazon_edi_order_id': amazon_edi_order_id,
                'sale_order_line_id': move_id.sale_line_id.id
            }
            for stock_move_line in move_id.move_line_ids if not stock_move_lines else stock_move_lines.filtered(
                    lambda stock_move_line: stock_move_line.move_id.id == move_id.id):
                if stock_move_line.product_id.tracking == 'lot':
                    quant_ids = stock_move_line.result_package_id.quant_ids.filtered(
                        lambda quant_id: quant_id.product_id.id == stock_move_line.product_id.id)
                    for quant_id in quant_ids:
                        order_line.update({'expiry_date': quant_id.removal_date or '',
                                           'lot_id': quant_id.lot_id.name or ''})
                        break
            order_lines.append(order_line)
        order_lines_info = self.get_avc_updated_order_lines(order_lines)
        return order_lines_info

    def get_avc_picking_product_with_qty_info(self, move_ids):
        product_with_qty_info, bom_ids = {}, set()
        for move_id in move_ids:
            if self._check_avc_kit_type_product(move_id.sale_line_id.product_id, move_id.picking_id.company_id.id):
                boms = move_id.mapped('bom_line_id.bom_id')
                sale_line_id = move_id.sale_line_id
                relevant_bom = boms.filtered(lambda b: b.type == 'phantom' and
                                                       (b.product_id == sale_line_id.product_id or
                                                        (b.product_tmpl_id == sale_line_id.product_id.product_tmpl_id
                                                         and not b.product_id)))
                if relevant_bom:
                    if relevant_bom[0].id in bom_ids:
                        continue
                    product_with_qty_info.update(
                        {move_id.id: self.get_acv_kit_product_quantity_done(move_id, relevant_bom)})
                    bom_ids.add(relevant_bom[0].id)
            else:
                product_with_qty_info.update({move_id.id: move_id.quantity_done})
        return product_with_qty_info

    def _check_avc_kit_type_product(self, product_id, company_id):
        """
        This method is used to check current product is kit type product or not
        @author: Dipak Gogiya
        Task ID -
        :param product_id: product.product()
        :param company_id: res.company()
        :return: Boolean
        """
        return_value = False
        mpr_install = self.env['ir.module.module'].sudo().search([
            ('name', '=', 'mrp'), ('state', '=', 'installed')], limit=1)
        if mpr_install:
            bom_product = self.env['mrp.bom'].sudo()._bom_find(
                product=product_id, company_id=company_id, bom_type='phantom')
            if bom_product:
                return_value = True
        return return_value

    def get_acv_kit_product_quantity_done(self, move_id, relevant_bom):
        sale_line_id = move_id.sale_line_id
        picking_id = move_id.picking_id
        quantity_done = 0.0
        if relevant_bom:
            filters = {
                'incoming_moves': lambda m: m.location_dest_id.usage == 'customer' and (
                        not m.origin_returned_move_id or (m.origin_returned_move_id and m.to_refund)),
                'outgoing_moves': lambda m: m.location_dest_id.usage != 'customer' and m.to_refund
            }
            order_qty = sale_line_id.product_uom._compute_quantity(sale_line_id.product_uom_qty,
                                                                   relevant_bom.product_uom_id)
            moves = sale_line_id.move_ids.filtered(
                lambda m: m.state == 'done' and not m.scrapped and m.picking_id.id == move_id.picking_id.id)
            quantity_done = moves._compute_kit_quantities(sale_line_id.product_id, order_qty, relevant_bom, filters)
        return quantity_done

    def get_avc_updated_order_lines(self, order_lines):
        """
            Usage: This method is used for prepare the new dict based on order lines and sum the quantity of
            same product
            @Migration by: Dipak Gogiya
            @Task: 179124 - Migrate Amazon Vendor Central module into V15.
            :return: order_lines_info -> Dict
        """
        lines = []
        for line in order_lines:
            qty = line.get('qty_done')
            if lines:
                duplicates = [l for l in lines if line.get('product_id') == l.get('product_id')]
                if len(duplicates):
                    for duplicate in duplicates:
                        duplicate.update({
                            'qty_done': qty + duplicate.get('qty_done')
                        })
                else:
                    # If line is not exist in updated variable then add it
                    lines.append(line)
            else:
                # If line is not exist in updated variable then add it
                lines.append(line)
        return lines

    def prepare_packages_acknowledgment_data(self, file_asn_string, total_segment,
                                             packages_info, requisition):
        """
            Usage: Used for preparing the packages information of picking for sending to the AVC
            :param file_asn_string: ASN Acknowledgment Data, Type: String
            :param total_segment: Total Number of segments, Type: Int
            :param packages_info: packages information, Type: Dict
            :@task:
            :@author: Dipak Gogiya, 30/12/2020
            :return: updated file_asn_string, total_segment
        """
        package_number, line_no = 1, 0
        for package_details in packages_info.values():
            package_info = package_details.get('package_info', {})
            order_lines = package_details.get('package_lines', {})
            package_number += 1
            file_asn_string += "CPS+%s+1'" % (str(package_number))  # First packing unit
            total_segment += 1
            file_asn_string += "PAC+1+:52+PK'"
            total_segment += 1
            file_asn_string += "MEA+PD+LN+CMT:%s'" % (
                str(package_info.get('length')))
            total_segment += 1
            file_asn_string += "MEA+PD+WD+CMT:%s'" % (
                str(package_info.get('width')))
            total_segment += 1
            file_asn_string += "MEA+PD+HT+CMT:%s'" % (
                str(package_info.get('height')))
            total_segment += 1
            file_asn_string += "PCI+33E'"
            total_segment += 1
            file_asn_string += "GIN+BJ+%s'" % (self.sscc_code)
            total_segment += 1

            # Preparing the items detail
            file_asn_string, total_segment = requisition.amazon_sale_requisition_line_ids. \
                prepare_asn_lines_data(file_asn_string, total_segment, order_lines, line_no)
            line_no += 1

        return file_asn_string, total_segment
