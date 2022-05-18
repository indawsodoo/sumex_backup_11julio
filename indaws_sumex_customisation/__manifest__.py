# -*- coding: utf-8 -*-
{
    'name': "Indaws Sumex Customisation",

    'summary': """
        Indaws Sumex Customisation
    """,

    'description': """
        Indaws Sumex Customisation
    """,

    'author': "inDAWS",
    'website': "http://www.indaws.es",
    'category': 'Product',
    'version': '14.0.1.0.25',
    'sequence': 1,
    'installable': True,
    'application': False,
    'auto_install': False,
    'depends': ['base', 'contacts', 'sale_management','account',],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/email.xml',
        'views/res_partner_view.xml',
        'views/sale_config.xml',
        'views/sale_order_views.xml',
	'views/account_move_inherit.xml',
    ],
}
