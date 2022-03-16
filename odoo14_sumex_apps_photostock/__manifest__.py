# -*- coding: utf-8 -*-
{
    'name': 'Sumex PhotoStock',
    'description': """
        Stock de fotos
        Inherit product template with new layer for create products Photostock type.
        Photostock product has new fields and use website_sale multiimages.
        Photostock backoffice manager show in web menu
        Photostock frontoffice show in url/photostock
        User need Photostock group (managed from user odoo interface)
    """,
    'author': 'Sumex S.A.',
    'license': "Other proprietary",
    "version": "14.0",
    'depends': [
        'base',
        'stock',
        'web',
        'website_sale',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/backoffice/product_template_inherit_view.xml',
        'views/backoffice/photostock_view_products.xml',
        'views/backoffice/photostock_view_imagenes.xml',
        'views/backoffice/photostock_view_manuales.xml',
        'views/backoffice/photostock_view_certificados.xml',
        'views/backoffice/photostock_menu.xml',

        'views/frontoffice/frontoffice_header.xml',
        'views/frontoffice/frontoffice_page_index.xml',
        'views/frontoffice/snippets/frontoffice_page_index_pagination.xml',
        'views/frontoffice/snippets/frontoffice_page_index_search.xml',
        'views/frontoffice/snippets/frontoffice_page_index_product.xml',
        'views/frontoffice/frontoffice_page_product.xml'
    ],

    'qweb': [
        'views/templates.xml',
    ],

    'application': True,
}
