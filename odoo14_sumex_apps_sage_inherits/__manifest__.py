{
    'name': 'Sumex Apps Sage Inherits',
    'description': 'Extension de campos en modelos y vistas para valores de Sage',
    'author': 'Sumex S.A.',
    'license': "Other proprietary",
    "version": "15.0",
    'depends': ['base', 'contacts', 'account', 'stock', 'sale_management', 'purchase'],
    'data': [
        'views/forms_inherit_partner.xml',
        'views/forms_inherit_order.xml',
        'views/forms_inherit_product.xml',
    ],
    'application': False,
    'installable': True,
}
