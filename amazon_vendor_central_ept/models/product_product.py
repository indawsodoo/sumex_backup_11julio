""" Inherit the existing functionality and added the new functionality"""

from odoo import models


class ProductProduct(models.Model):
    """
        Inherit the existing functionality and added the new functionality
    """
    _inherit = "product.product"

    def prepare_products_info(self, products_and_quantity, pricelist_id):
        """
            Used for products info for prepare the EDI file to sending to amazon vendor central
            :param self: list of products, product.product()
            :param products_and_quantity: Contains products with quantity info, Type: Dictionary.
            :param pricelist_id: product.pricelist()
            :return: Product lines, Type: List od Dict.
        """
        product_lines, product_stock_details = [], {}
        for product_detail in products_and_quantity:
            # Used for sum the quantity of same product id
            product_stock_details = {k: product_stock_details.get(k, 0) +
                                        product_detail.get(k, 0) for k in
                                     set(product_stock_details) | set(product_detail)}

        for product in self:
            product_qty = product_stock_details.get(product.id, 0.0)

            price = pricelist_id.with_context(uom=product.uom_id.id).price_get \
            (product.id, 1.0, partner=False)[pricelist_id.id] if pricelist_id else 0.0

            product_info = {
                'product_id': product.id,
                'product_qty': int(product_qty) if product_qty > 0 else 0,
                'price': price,
                'default_code': product.default_code,
                'pricelist_id': pricelist_id.id,
                'barcode': product.barcode,
                'currency': product.currency_id.name,
            }
            product_lines.append(product_info)

        return product_lines

    def search_avc_odoo_product(self, default_code, barcode):
        """
            Usage: Used for search the odoo product based on the default code or barcode
            :param default_code: Default Code
            :param barcode: Barcode
            :return: product.product
        """
        odoo_product = self.search([('default_code', '=', default_code)], limit=1)
        if not odoo_product:
            odoo_product = self.search([('barcode', '=', barcode)], limit=1)
        return odoo_product
