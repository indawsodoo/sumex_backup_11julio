# -*- coding: utf-8 -*-

"""
	ESTE IMPORTADOR USA CAMPOS EXTENDIDOS EN EL MODULO 'sumex_apps_sage_inherits'
"""

from odoo import models


class sumex_apps_imports_csv_import_sage_proveedores(models.AbstractModel):

	_description = "modulo importador"

	def hook_pre_process(self, company_id, file_csv_header, file_csv_content):

		pass

	def get_import_fields(self):

		import_client = self.env['sumex_apps_imports_csv_import_sage_clientes']
		return import_client.get_import_fields()

	def hook_post_process(self, company_id, file_csv_header, file_csv_content_row_dict, file_csv_content):

		import_client = self.env['sumex_apps_imports_csv_import_sage_clientes']
		return import_client.hook_post_process(company_id, file_csv_header, file_csv_content_row_dict, file_csv_content)

	def validate_row(self, file_csv_content_row_num, company_id, file_csv_content_row):

		"""
			El importador ya realiza automaticamente las validaciones de 'required_header_field' y 'required_value'file_csv_content_row
			Aquí podemos validar el formato de valores y otras cuestiones

			Este método "validate_row" es ejecutado en un bucle antes de realizar la importación
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			Se puede retornar {'error':''} {'warning':''} o {'info':''} o simplemente nada.
		"""

		import_client = self.env['sumex_apps_imports_csv_import_sage_clientes']
		return import_client.validate_row(file_csv_content_row_num, company_id, file_csv_content_row)

	def import_row(self, file_csv_content_row_num, company_id, file_csv_header, file_csv_content_row):

		import_client = self.env['sumex_apps_imports_csv_import_sage_clientes']
		"""
			Este método "import_row" es ejecutado en un bucle del objeto importador(sumex_apps_imports_csv)
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			El retorno se asumirá como correcto al no ser que se retorne {'error':}
		"""
		
		import_client = self.env['sumex_apps_imports_csv_import_sage_clientes']
		return import_client.import_row(file_csv_content_row_num, company_id, file_csv_header, file_csv_content_row)
