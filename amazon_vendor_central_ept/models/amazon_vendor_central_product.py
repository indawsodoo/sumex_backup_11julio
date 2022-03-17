""" This file create the new functionality of amazon product. """
from odoo import models, fields


class AmazonVendorCentralProduct(models.Model):
    """
        This model is store amazon_product_sku and odoo_sku with vendor id
    """
    _name = 'amazon.vendor.central.product.ept'
    _description = 'Amazon Products'
    _rec_name = 'amazon_sku'

    amazon_sku = fields.Char(string='Amazon SKU', help='Amazon vendor product SKU')
    product_id = fields.Many2one('product.product', string='Product', help='Product')
    amazon_vendor_instance_id = fields.Many2one('amazon.vendor.instance', string='Vendor',
                                                help='Amazon Vendor Instance')
    barcode = fields.Char(string="Barcode", help='Product Barcode')

    product_type = fields.Selection([('EN', 'EN'),
                                     ('UP', 'UP'),
                                     ('SRV', 'SRV'),
                                     ('BP', 'BP'),
                                     ('SA', 'SA'),
                                     ('IB', 'IB')], string="Item Type",
                                    help="EN: EAN/ISBN13"
                                         "UP: UPC"
                                         "SRV: GTIN"
                                         "BP: ASIN"
                                         "SA: Vendor SKU"
                                         "IB: ISBN10")

    def search_avc_amazon_product(self, amazon_sku, instance, item_type):
        """
            Usage: Used for, Search the amazon product and return it.
            :param amazon_sku: Internal Reference (SKU), Type: String
            :param instance: amazon.vendor.instance()
            :param item_type: Contain the amazon product item type, Such as ['EN', 'SA'] etc.
            :return: amazon.vendor.central.product.ept()
        """
        amazon_product = self.search([('amazon_sku', '=', amazon_sku),
                                      ('amazon_vendor_instance_id', '=', instance.id or False),
                                      ('product_type', '=', item_type)])
        return amazon_product

    def search_avc_existing_amazon_product(self, product_id, instance):
        """
            Usage: Used for, Search the amazon product and return it.
            :param amazon_sku:  Internal Reference (SKU), Type: String
            :param instance: amazon.vendor.instance()
            :param item_type: Contain the amazon product item type, Such as ['EN', 'SA'] etc.
            :return: amazon.vendor.central.product.ept()
        """
        amazon_product = self.search([('product_id', '=', product_id.id),
                                      ('amazon_vendor_instance_id', '=', instance.id or False)],
                                     limit=1)
        return amazon_product

    def search_odoo_product_by_default_code(self, default_code, item_type, instance):
        """
            This method is used for find the odoo product based on default code
            and item type getting from file and return it.
            :param default_code: Internal Reference (SKU), Type: String
            :param item_type: Amazon Item Type, Type: String
            :param instance: amazon.vendor.instance()
            :return: product.product()
        """
        return self.search([('amazon_sku', '=', default_code),
                            ('product_type', '=', item_type),
                            ('amazon_vendor_instance_id', '=', instance.id)], limit=1).product_id

    def search_odoo_product_by_default_ean(self, ean, item_type, instance):
        """
            This method is used for find the odoo product based on ean (barcode) code
            and item type getting from file and return it.
            :param ean: It contain the Barcode, Type: string
            :param item_type:  Amazon Item Type, Type: String
            :param instance: amazon.vendor.instance()
            :return: product.product()
        """
        return self.search([('barcode', '=', ean),
                            ('product_type', '=', item_type),
                            ('amazon_vendor_instance_id', '=', instance.id)], limit=1).product_id

    def search_avc_amazon_product_by_edit_line_code(self, instance, edi_line_code_type, edi_line_code):
        """
            Used for find the amazon product based on method parameters
            :param instance: amazon.vendor.instance()
            :param edi_line_code_type: product type, SKU or Barcode
            :param edi_line_code: product default code or barcode
            :return: amazon.vendor.central.product.ept()
        """
        domain = [('amazon_vendor_instance_id', '=', instance.id)]
        if edi_line_code_type == 'barcode':
            domain.append(('barcode', '=', edi_line_code))
        elif edi_line_code_type == 'sku':
            domain.append(('amazon_sku', '=', edi_line_code))
        return self.search(domain, limit=1)
