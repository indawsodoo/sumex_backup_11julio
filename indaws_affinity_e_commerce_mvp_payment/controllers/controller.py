# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
# from odoo.addons.website_excel_sheet.controllers.main import WebsiteSale
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.osv import expression

class EmiproThemeBase(http.Controller):

    @http.route(['/ajax_cart_sucess_data_1'], type='json', auth="public", website=True)
    def get_ajax_cart_sucess(self, product_id=None, product_product=None):
        """
        This controller return the template for Ajax Add to Cart with product details
        :param product_id: get product id
        :return: ajax cart template for success html
        """
        if product_id:
            product_variant = request.env['product.product'].search([['id', '=', product_product]])
            product = request.env['product.template'].search([['id', '=', product_variant.product_tmpl_id.id]])
            values = {
                'product': product,
                'product_variant': product_variant,
            }
            response = http.Response(template="theme_clarico_vega.ajax_cart_success_template", qcontext=values)
            return response.render()

class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):

        domains = [request.website.sale_product_domain()]

        if search:
            for srch in search.split(" "):
                subdomains = [
                    [('name', 'ilike', srch)],
                    [('product_variant_ids.default_code', 'ilike', srch)],
                    [('ean2', 'ilike', srch)]
                ]
                if search_in_description:
                    subdomains.append([('description', 'ilike', srch)])
                    subdomains.append([('description_sale', 'ilike', srch)])
                    subdomains.append([('ean2', 'ilike', srch)])
                domains.append(expression.OR(subdomains))

        if category:
            domains.append([('public_categ_ids', 'child_of', int(category))])

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domains.append([('attribute_line_ids.value_ids', 'in', ids)])
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domains.append([('attribute_line_ids.value_ids', 'in', ids)])

        return expression.AND(domains)


    @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        """ Overwrite base method
        """
        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')
        order.action_confirm()
        if transaction_id:
            tx = request.env['payment.transaction'].sudo().browse(transaction_id)
            assert tx in order.transaction_ids()
        elif order:
            tx = order.get_portal_last_transaction()
        else:
            tx = None

        if not order or (order.amount_total and not tx):
            return request.redirect('/shop')

        if order and not order.amount_total and not tx:
            order.with_context(send_email=True).action_confirm()
            return request.redirect(order.get_portal_url())

        # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        if tx and tx.state == 'draft':
            return request.redirect('/shop')

        PaymentProcessing.remove_payment_transaction(tx)
        return request.redirect('/shop/confirmation')