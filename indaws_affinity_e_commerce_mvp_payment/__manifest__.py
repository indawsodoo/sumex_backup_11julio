# -*- coding: utf-8 -*-
{
    'name': "E-commerce MVP Payment",
    'summary': """
        E-commerce MVP Payment""",
    'description': """
        E-commerce MVP Payment module add sale order Payment Terms calculation on website payment page""",
    'author': "inDAWS",
    'website': "http://www.indaws.es",
    'category': 'website',
    'version': '14.0.1.0.52',
    'sequence': 1,
    'installable': True,
    'application': False,
    'auto_install': False,
    'depends': ['sale_management', 'website_sale', 'website', 'product', 'uom', 'purchase', 'stock',
                'theme_clarico_vega', 'mail', 'sale'],
    'data': [
        'views/assets.xml',
        'security/ir.model.access.csv',
        'views/sale_view.xml',
        'views/payment_template.xml',
        'views/product.xml',
        'views/product_template.xml',
        'data/sale_confirmation_email.xml',

    ],
    'qweb': [
        'static/src/xml/website_sale_utils.xml',
    ],
}
