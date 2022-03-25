# -*- coding: utf-8 -*-

"""
	ESTE IMPORTADOR USA CAMPOS EXTENDIDOS EN EL MODULO 'sumex_apps_sage_inherits'
"""

from odoo import models
from odoo.exceptions import UserError


class sumex_apps_imports_csv_import_genesis_companies_locations(models.AbstractModel):

	_description = __name__

	_import_fields = [

		# Campos que participan en la importacion del modelo
		{'csv_column_name': 'idAlmacen', 'required_header_field': True, 'required_value': True},
		{'csv_column_name': 'idEmpresa', 'required_header_field': True, 'required_value': True},
		{'csv_column_name': 'idUbicacion', 'required_header_field': True, 'required_value': True},
		{'csv_column_name': 'idPasillo', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'idColumna', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'idNivel', 'required_header_field': True, 'required_value': False},

	]

	def get_import_fields(self):

		return self._import_fields

	def hook_pre_process(self, company_id, file_csv_header, file_csv_content):

		if not company_id:
			raise UserError("Este importador necesita una compañía vinculada")

		# Actualizo compañía
		company_model = self.env['sumex_apps_imports_csv_library'].get_model('res.company')
		company_row = company_model.search([('id', '=', 1)], limit=1)
		if company_row.name.upper() != 'SUMEX S.A.':
			country = self.env['sumex_apps_imports_csv_library'].get_country('España')
			state = self.env['sumex_apps_imports_csv_library'].get_state(country, 'Barcelona')
			company_row.write({
				'name': 'SUMEX S.A.',
				'city': 'Sant Joan Despí',
				'zip': '08970',
				'street': 'Montilla, 9',
				'phone': '+34 93 373 67 13',
				'email': 'racesport@sumex.com',
				'vat': 'A-08-242992',
				'country_id': country.id,
				'state_id': state.id
			})

		# Creamos las empresas
		companies = [
			{
				'name': "AMPLUSMART S.L.U​.",
				'domicilio': "C/ Alguer 8",
				'ciudad': "Sant Boi De Llobregat",
				'cp': "08830",
				'provincia': "Barcelona",
				'pais': "España",
				'cif': "ESB66234121",
				'telefono': "+34 930 153 388",
				'email': "info@accesoriosyllantas.com"
			},
			{
				'name': "SUMEX PORTUGAL, LDA.",
				'domicilio': "Rua das Lagoas nº 186",
				'ciudad': "Pavilhao A – Touguinha",
				'cp': "4480",
				'provincia': "Vila do Conde",
				'pais': "Portugal",
				'cif': "PT504981609",
				'telefono': "+351 252 63 75 50",
				'email': "encomendas@sumex.pt"
				#  Fax +351 252 63 75 52
			},
			{
				'name': "SUMEX FRANCE SAS",
				'domicilio': "Avenue de la Martelle. Albipole",
				'ciudad': "France",
				'cp': "81150",
				'provincia': "France",
				'pais': "France",
				'cif': '',
				'telefono': "+33 (0)5 63 45 68 55",
				'email': "contact@sumex.fr"
				#  Fax +33 (0)5 63 47 61 24
			},
			{
				'name': "SUMEX AMERICA CORP.",
				'domicilio': "Calle 5tª. Avenida 5tª",
				'ciudad': "France Field.",
				'cp': '0302 – 00472',
				'provincia': "Zona Libre de Colón",
				'pais': "Rep. de Panamá",
				'cif': '',
				'telefono': "+(507) 431-1458 / 431-1459",
				'email': "ventas.america@sumex.com"
				#  Fax. +(507) 431-1460
			},
			{
				'name': "Sumex International LLC.",
				'domicilio': "8321 NW 66th",
				'ciudad': "St. Miami",
				'cp': "33166",
				'provincia': "Florida",
				'pais': "USA",
				'cif': '',
				'telefono': "+1 305-591-4420",
				'email': "manuel@sumex.com"
			}
]
		almacen_principal = self.env['sumex_apps_imports_csv_library'].get_model('stock.warehouse').search([], limit = 1)
		ubicacion_padre_code = almacen_principal.code
		if not ubicacion_padre_code:
			return {'error': "no se encuentra el code del almacen principal %s"% almacen_principal.name}
		ubicacion_padre = self.env['sumex_apps_imports_csv_library'].get_model('stock.location').search([('name', '=', ubicacion_padre_code)], limit=1)
		if not ubicacion_padre:
			return {'error': "no se encuentra la ubicación padre de la ubicacion %s" % ubicacion_padre_code}

		for company in companies:

			result = self.env['sumex_apps_imports_csv_library'].get_or_create_company(
				company_id = False,
				company_name = company['name'],
				vat = company['cif'],
				country_name = company['pais'],
				state_name = company['provincia'],
				ciudad = company['ciudad'],
				domicilio = company['domicilio'],
				cp = company['cp'],
 				telefono = company['telefono'],
 				email = company['email'],
			)
			if isinstance(result, dict) and 'error' in result:
				raise UserError(result['error'])

		#  Creamos categoria de location tipo PLANTA
		# stock_storage_category_model = self.env['sumex_apps_imports_csv_library'].get_model('stock.storage.category')
		# stock_storage_category_row = stock_storage_category_model.search([('name', '=', 'PLANTA')], limit = 1)
		# if not stock_storage_category_row:
		# 	try:
		# 		stock_storage_category_row = stock_storage_category_model.create({'name': 'PLANTA'})
		# 		stock_storage_category_row._cr.commit()
		# 	except Exception as e:
		# 		exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
		# 		raise UserError(exception_msg)
		# storage_category_id = stock_storage_category_row.id

		#  Creamos los locations padre
		stock_location_model = self.env['sumex_apps_imports_csv_library'].get_model('stock.location')
		locations = ['PLANTA ARRIBA', 'PLANTA ABAJO']
		for location in locations:
			row = stock_location_model.search([('name', '=', location)])
			if not row:
				try:
					stock_location_model.create({
						'company_id': company_id,
						'location_id': ubicacion_padre.id,
						'name': location,
						# 'storage_category_id': storage_category_id
					})
					stock_location_model._cr.commit()
				except Exception as e:
					exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
					raise UserError(exception_msg)

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

		return True

	def import_row(self, file_csv_content_row_num, company_id, file_csv_header, file_csv_content_row):

		"""
			Este método "import_row" es ejecutado en un bucle del objeto importador(sumex_apps_imports_csv)
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			El retorno se asumirá como correcto al no ser que se retorne {'error':}
		"""

		if file_csv_content_row['idempresa'] != "1":
			return True

		posx = 0
		try:
			posx = int(file_csv_content_row['idPasillo'])
		except:
			pass

		posy = 0
		try:
			posy = file_csv_content_row['idColumna']
		except:
			pass

		posz = 0
		try:
			posz = file_csv_content_row['idNivel']
		except:
			pass

		result = self.get_or_create_location(
			company_id = company_id,
			idempresa = file_csv_content_row['idempresa'],
			location_name = file_csv_content_row['idubicacion'],
			posx = posx,
			posy = posy,
			posz = posz
		)

		return result

	def get_or_create_location(self, company_id, idempresa, location_name, posx, posy, posz):

		location_parent_name = "PLANTA ARRIBA"
		try:
			location_name = int(location_name)
		except:
			location_name = 0
			pass
		if location_name >= 40000:
			location_parent_name = "PLANTA ABAJO"

		location = self.env['sumex_apps_imports_csv_library'].get_or_create_location(
			company_id = company_id,
			location_parent_name = location_parent_name,
			location_name = location_name,
			posx = posx,  # Pasillo (X)
			posy = posy,  # Estantería (Y)
			posz = posz,  # Altura (Z)
		)
		if isinstance(location, dict) and 'error' in location:
			return location

		return True
