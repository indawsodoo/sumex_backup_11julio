{
	'name': 'Sumex migrate',
	'description': 'Sumex migrate actions and inherits',
	'author': 'Sumex S.A.',
	'license': "Other proprietary",
	"version": "14.0",
	'depends': [
		'base',
		# 'contacts',
		# 'account',
		'stock',
		# 'sale_management',
		# 'purchase',
		# 'product_brand_sale',
		# 'product_brand_ecommerce'
	],
	'data': [
		# 'security/ir.model.access.csv',
        'views/forms_inherit_product_template.xml',
	],

	'application': True,
	'installable': True,
}
