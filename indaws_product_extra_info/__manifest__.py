# -*- coding: utf-8 -*-

{
    'name': "Extra info product tree view",

    'summary': """
    last sale price and last purchase price update on tree view of product
       """,
    'description': """
    last sale price and last purchase price update on tree view of product
    """,
    'author': "inDAWS",
    'website': "http://www.indaws.es",
    'category': 'Tools',
    'version': '14.0.1.0.15',
    'depends': ['sale_stock', 'sale_management', 'purchase', 'product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/last_purchase_view.xml',
        'wizard/last_sale_view.xml',
        'wizard/current_stock_view.xml',
        'views/product_product_views.xml',
        'views/product_template_kanban_views.xml',
    ],
}
