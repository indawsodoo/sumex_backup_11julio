""" This file is inherit the existing sale order and sale order line functionality and
added its new functionality
"""
from odoo import models, fields


class SaleOrder(models.Model):
    """
        Inherit the existing functionality and added the new functionality
    """
    _inherit = "sale.order"
    _description = "Sale Order"

    amazon_vendor_order_id = fields.Many2one('amazon.sale.requisition.ept',
                                             string='Amazon Vendor Order Reference',
                                             ondelete='cascade')
    amazon_vendor_instance_id = fields.Many2one('amazon.vendor.instance',
                                                string='Amazon Vendor Instance')
    is_amazon_edi_order = fields.Boolean('is Amazon Order')
    amazon_order_ack_uploaded = fields.Boolean(related='amazon_vendor_order_id.is_acknowledgement_sent',
                                               string='Amazon order Acknowledgement Uploaded')
    is_backorder = fields.Boolean('Is BackOrder?')

    def action_confirm(self):
        """
            In this doing the Super call of action confirm method and pass the value in picking
            carrier type and vendor id.
            :return: result
        """
        res = super(SaleOrder, self).action_confirm()
        for sale_order in self:
            if sale_order.is_amazon_edi_order:
                sale_order.picking_ids.write({'is_amazon_vendor_central_picking': True,
                                              'amazon_vendor_order_id': sale_order.amazon_vendor_order_id.id})
                if sale_order.amazon_vendor_order_id.state == 'processed' or \
                        not sale_order.amazon_vendor_order_id.is_acknowledgement_sent:
                    sale_order.amazon_vendor_order_id.export_po_acknowledgment()
        return res

    def action_cancel(self):
        """
            USage: In this method, doing the Super call of action cancel method for execute
            the default functionality and after cancel the order set the
            is_acknowledgement_sent = False of the requisition
        :return:
        """
        res = super(SaleOrder, self).action_cancel()
        if res:
            for sale_order in self.filtered(lambda order: order.state == 'cancel' and order.is_amazon_edi_order):
                sale_order.amazon_vendor_order_id.is_acknowledgement_sent = False
        return res

    def _prepare_invoice(self):
        """
        Usage: Added the instance for identifying the invoice is create for amazon vendor central
        @author: Dipak Gogiya
        :return: updated res
        """
        res = super(SaleOrder, self)._prepare_invoice()
        if self.is_amazon_edi_order:
            res.update({'is_amazon_edi_invoice': self.is_amazon_edi_order})
        return res

    def create_avc_sale_order(self, requisition, backorder=False):
        """
            Usage: Create the sale order based on amazon requisition order
            :param requisition: amazon.sale.requisition.ept()
            :param backorder: Boolean
            Added by: Dipak Gogiya, 04/12/2020
            :return: sale.order()
        """
        instance = requisition.amazon_vendor_instance_id
        sale_order_values = {
            'partner_id': requisition.partner_id.id,
            'partner_shipping_id': requisition.shipping_partner_id.id,
            'date_order': str(requisition.order_date),
            'payment_term_id': requisition.partner_id.property_payment_term_id.id,
            'warehouse_id': instance.warehouse_id.id,
            'partner_invoice_id': requisition.invoice_partner_id.id,
            'pricelist_id': instance.pricelist_id.id,
            'company_id': instance.company_id.id,
            'picking_policy': instance.picking_policy,
            'carrier_id': instance.amazon_edi_carrier_method.id or False,
            'state': 'draft',
            'team_id': instance.team_id.id or False,
            'client_order_ref': requisition.amazon_edi_order_id or False
        }
        order_vals = self.create_sales_order_vals_ept(sale_order_values)
        order_vals.update(
            {
                'amazon_vendor_order_id': requisition.id or False,
                'amazon_vendor_instance_id': instance.id or False,
                'is_backorder': backorder,
                'is_amazon_edi_order': True})
        order_id = self.create(order_vals)
        return order_id


class SaleOrderLine(models.Model):
    """
        Inherit the existing functionality and added the new functionality
    """
    _inherit = "sale.order.line"

    def create_avc_sale_order_lines(self, order_id, requisition_lines):
        """
            Usage: Create the sale order lines based on amazon order requisition lines
             and odoo sale order
            :param order_id: sale.order()
            :param requisition_lines: amazon.sale.requisition.line.ept()
            Added by: Dipak Gogiya, 04/12/2020
            :return: True
        """
        for requisition_line in requisition_lines:
            so_line_values = {
                'order_id': order_id.id,
                'product_id': requisition_line.product_id.id,
                'company_id': order_id.company_id.id,
                'name': requisition_line.product_id.name,
                'order_qty': requisition_line.acknowledge_qty,
                'price_unit': requisition_line.unit_price
            }
            so_line_values = self.create_sale_order_line_ept(so_line_values)
            self.create(so_line_values)
        return True
