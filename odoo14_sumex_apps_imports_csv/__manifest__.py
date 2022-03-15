{
	'name': 'Sumex Imports Csv',
	'description': 'Interfaz de importaciones CSV',
	'author': 'Sumex S.A.',
	'license': "Other proprietary",
	"version": "14.0",
	'depends': [
		'base',
		'contacts',
		'account',
		'stock',
		'sale_management',
		'purchase',
		'product_brand_sale',
		'product_brand_ecommerce'
	],
	'data': [
		'security/ir.model.access.csv',
		'wizard/csv_instructions_wizard_forms.xml',
		'views/forms.xml',
		'views/menu.xml',
		# 'views/templates.xml'
	],

	"assets": {
		"web.assets_backend": [
			"odoo14_sumex_apps_imports_csv/static/src/js/file_size.js"
		]
	},

	'qweb': [
		'views/templates.xml'
	],
	'application': True,
	'installable': True,
}
