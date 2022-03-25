{
    'name': 'Sumex Prestashop export products',
    'description': 'Sumex Prestashop export products',
    'author': 'Sumex S.A.',
    'license': "Other proprietary",
    "version": "15.0",
    'depends': [
        'base',
        # 'contacts',
        # 'account',
        'stock',
        # 'sale_management',
        # 'purchase'
    ],
    'data': [
        'views/forms_inherit_product_template.xml',
    ],
    'application': False,
    'installable': True,
}
