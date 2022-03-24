# -*- coding: utf-8 -*-

"""
	ESTE IMPORTADOR USA CAMPOS EXTENDIDOS EN EL MODULO 'sumex_apps_sage_inherits'
"""

from odoo import models
from odoo.exceptions import UserError


class sumex_apps_imports_csv_import_genesis_stock(models.AbstractModel):

	_description = __name__

	_import_fields = [

		# Campos que participan en la importacion del modelo
		{'csv_column_name': 'idEmpresa', 'required_header_field': True, 'required_value': True},
		{'csv_column_name': 'idAlmacen', 'required_header_field': True, 'required_value': True},
		{'csv_column_name': 'idUbicacion', 'required_header_field': True, 'required_value': True},
		{'csv_column_name': 'idProducto', 'required_header_field': True, 'required_value': True},
		# {'csv_column_name': 'idLote', 'required_header_field': False, 'required_value': False},
		# {'csv_column_name': 'idNSerie', 'required_header_field': False, 'required_value': False},
		# {'csv_column_name': 'FechaEntrada', 'required_header_field': False, 'required_value': False},
		{'csv_column_name': 'QExistencias', 'required_header_field': False, 'required_value': False},
		# {'csv_column_name': 'FechaModificacion', 'required_header_field': False, 'required_value': False},
		# {'csv_column_name': 'QInventario', 'required_header_field': False, 'required_value': False},
	]

	def get_import_fields(self):

		return self._import_fields

	def hook_pre_process(self, company_id, file_csv_header, file_csv_content):

		pass

	def hook_post_process(self, company_id, file_csv_header, file_csv_content_row_dict, file_csv_content):

		pass

	def validate_row(self, file_csv_content_row_num, company_id, file_csv_content_row):

		"""
			El importador ya realiza automaticamente las validaciones de 'required_header_field' y 'required_value'file_csv_content_row
			Aquí podemos validar el formato de valores y otras cuestiones

			Este método "validate_row" es ejecutado en un bucle antes de realizar la importación
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			Se puede retornar {'error':''} {'warning':''} o {'info':''} o simplemente nada.
		"""

		if file_csv_content_row['idempresa'] != "1":
			return True

		stock_model = self.env['sumex_apps_imports_csv_library'].get_model('stock.location')
		location_name = file_csv_content_row['idubicacion']
		try:
			location_name = int(location_name)
		except:
			pass
		if not location_name:
			return {'error': "Location wrong name '%s'" % file_csv_content_row['idubicacion']}
		location = stock_model.search([
			('company_id', '=', company_id),
			('name', '=', location_name),
			('active', 'in', [True, False])
		], limit = 1)
		if not location:
			return {'error': "Location '%s' no existe" % file_csv_content_row['idubicacion']}

		return True

	def import_row(self, file_csv_content_row_num, company_id, file_csv_header, file_csv_content_row):

		"""
			Este método "import_row" es ejecutado en un bucle del objeto importador(sumex_apps_imports_csv)
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			El retorno se asumirá como correcto al no ser que se retorne {'error':}
		"""

		if file_csv_content_row['idempresa'] != "1":
			return True

		stock_model = self.env['sumex_apps_imports_csv_library'].get_model('stock.location')
		location_name = file_csv_content_row['idubicacion']
		try:
			location_name = int(location_name)
		except:
			pass
		if not location_name:
			return {'error': "Location wrong name '%s'" % file_csv_content_row['idubicacion']}
		location = stock_model.search([
			('company_id', '=', company_id),
			('name', '=', location_name),
			('active', 'in', [True, False])
		], limit = 1)
		if not location:
			return {'error': "Location '%s' no existe" % file_csv_content_row['idubicacion']}

		product_referencia = file_csv_content_row['idproducto']
		product_name = "no-name %s" % product_referencia
		# stock = file_csv_content_row['qexistencias']

		product_template = self.env['sumex_apps_imports_csv_library'].get_or_create_product_template(
			company_id = company_id,
			product_referencia = product_referencia,
			product_name = product_name,
			descripcion = '',
			precio_venta = 0,
			precio_compra = 0
		)
		if isinstance(product_template, dict) and 'error' in product_template:
			return product_template

		stock_quant_model = self.env['sumex_apps_imports_csv_library'].get_model('stock.quant')
		try:
			stock_quant_model.create({
				'location_id': location.id,
				'product_id': product_template.product_variant_id.id,
				'inventory_quantity': file_csv_content_row['qexistencias']
			})
			stock_quant_model._cr.commit()
		except Exception as e:
			exception_msg = self.rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}

		return True
