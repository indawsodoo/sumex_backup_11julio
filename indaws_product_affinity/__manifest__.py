# -*- coding: utf-8 -*-
{
    'name': "Product Affinity",

    'summary': "Ampliación de campos productos",


    'author': "INDAWS",
    'website': "http://www.indaws.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'product', 'purchase', 'emipro_theme_base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
