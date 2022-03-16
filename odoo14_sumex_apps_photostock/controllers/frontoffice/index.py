# -*- coding: utf-8 -*-

from odoo import http
# from odoo.http import request


class Index(http.Controller):

    @http.route(['/photostock/'], auth='user', methods=['GET'], website=True)
    def index(self, **kw):

        return self.indexPage(1)

    @http.route(['/photostock/index/'], auth='user', methods=['GET'], website=True)
    def index2(self, **kw):

        return self.indexPage(1)

    @http.route(['/photostock/index/<int:page>'], auth='user', methods=['GET'], website=True)
    def indexPage(self, page, **kw):

        limit_per_page = 20

        product_model = http.request.env['product.template'].sudo()

        total_products = product_model.search_count([('photostock_include', '=', '1')])
        total_pages = int(total_products / limit_per_page)
        offset = ((page - 1) * limit_per_page)
        if offset > total_products:
            offset = total_products
        paginator_top_left = page - 4
        if paginator_top_left < 1:
            paginator_top_left = 1
        paginator_top_right = page + 5
        if paginator_top_right > (total_pages + 1):
            paginator_top_right = (total_pages + 1)
        products = product_model.search(
            [('photostock_include', '=', '1')],
            limit = limit_per_page,
            # order = "name",
            order = "id",
            offset = offset
        )

        products_td = []
        products_tr = []
        c = 0
        for product in products:
            c += 1
            products_td.append(product)
            if c == 4:
                c = 0
                products_tr.append(products_td)
                products_td = []

        total_products_in_page = total_products - offset
        if total_products_in_page > limit_per_page:
            total_products_in_page = limit_per_page
        num = 0
        range_products = [num]
        for i in range(int(limit_per_page / 4)):
            num += 4
            range_products.append(num)

        return http.request.render('odoo14_sumex_apps_photostock.photostock_frontoffice_page_index', {
            'products': products,
            'page': page,
            'total_pages': total_pages,
            'total_products': total_products,
            'paginator_buttons_num': range(paginator_top_left, paginator_top_right),
            'paginator_top_right': paginator_top_right,
            'carrito': self._get_cart(),
            'range_products': range_products,
            'total_products_in_page': total_products_in_page,
            'products_tr': products_tr
        })

    @http.route(['/photostock/product/<int:page>/<int:product_id>'], auth='user', methods=['GET'], website=True)
    def productPage(self, page, product_id, **kw):

        product_model = http.request.env['product.template'].sudo()
        product = product_model.search([('photostock_include', '=', '1'), ('id', '=', product_id)], limit = 1)
        if not product:
            return self.indexPage(page)

        return http.request.render('odoo14_sumex_apps_photostock.photostock_frontoffice_page_product', {
            'product': product,
            'page': page,
            'carrito': self._get_cart()
        })

    @http.route(['/photostock/download_manual/<int:manual_id>'], auth='user', methods=['GET'], website=True)
    def download_manual(self, manual_id, **kw):

        import base64
        record = http.request.env['sumex.photostock_manuales'].browse(int(manual_id))
        binary_file = record.file
        filecontent = base64.b64decode(binary_file or '')
        content_type, disposition_content = False, False

        if not filecontent:
            return http.request.not_found()
        else:
            filename = 'manual_%s.pdf' % (manual_id)
            content_type = ('Content-Type', 'application/octet-stream')
            disposition_content = ('Content-Disposition', http.content_disposition(filename))
        return http.request.make_response(filecontent, [content_type, disposition_content])

    @http.route(['/photostock/add/<int:page>/<int:product_id>'], auth='user', methods=['GET'], website=True)
    def cartAdd(self, page, product_id, **kw):

        # AÑADIR AL CARRO
        carrito = http.request.env['sumex.photostock_carrito']
        result = carrito.create({
            'user_id': '1',
            'product_id': product_id
        })
        return self.indexPage(page, **kw)

    @http.route(['/photostock/del/<int:page>/<int:product_id>'], auth='user', methods=['GET'], website=True)
    def cartDelete(self, page, product_id, **kw):

        # ELIMINAR DEL CARRO
        carritoMem = http.request.env['sumex.photostock_carrito'].search(['&', ('user_id', '=', 1), ('product_id', '=', product_id)], limit=1)
        carritoMem.unlink()
        return self.indexPage(page, **kw)

    def _get_cart(self):

        # RECOGO EL CONTENIDO DEL CARRITO
        carrito_model = http.request.env['sumex.photostock_carrito'].sudo()
        carrito = carrito_model.search([('user_id', '=', 1)])
        return carrito
