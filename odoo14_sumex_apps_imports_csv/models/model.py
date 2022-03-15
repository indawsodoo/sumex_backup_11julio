# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
from time import process_time


class sumex_apps_imports_csv(models.Model):

	_name = 'sumex_apps_imports_csv'
	_description = "Importador csv"
	_order = 'name'

	import_names = [
		('sumex_apps_imports_csv_import_photostock_productos', 'PhotoStock - Productos'),
		('sumex_apps_imports_csv_import_genesis_companies_locations', 'Genesis - Compañías Almacenes Ubicaciones'),
		('sumex_apps_imports_csv_import_genesis_stock', 'Genesis - Stock'),
		('sumex_apps_imports_csv_import_sage_articulos', 'Sage - Artículos'),
		('sumex_apps_imports_csv_import_sage_clientes', 'Sage - Clientes'),
		('sumex_apps_imports_csv_import_sage_proveedores', 'Sage - Proveedores'),
		('sumex_apps_imports_csv_import_sage_ventas_cabeceras', 'Sage - Pedidos ventas (Cabecera)'),
		('sumex_apps_imports_csv_import_sage_ventas_lineas', 'Sage - Pedidos ventas (Lineas)'),
		# ('sumex_apps_imports_csv_import_sage_compras_cabeceras', 'Sage - Pedidos compras (Cabecera)'),
		# ('sumex_apps_imports_csv_import_sage_compras_lineas', 'Sage - Pedidos compras (Lineas)'),
	]

	description = fields.Char(string = 'Descripcion')
	name = fields.Char(string = 'Nombre')
	company_id = fields.Many2one(
		'res.company',
		'Company',
		default = False,
		help = "No indiques una compañía si no quieres limitar el objeto a una empresa determinada"
	)
	stop_in_error = fields.Boolean(string = 'Detener en error', default = False)
	print_progress_in_console = fields.Boolean(string = 'Mostrar progreso en consola', default = False)
	separator = fields.Char(string = 'Separador Csv', required = True,)
	import_name = fields.Selection(
		string = 'Plantilla',
		selection = import_names,
		required = True,
	)
	file = fields.Binary(string = "Fichero CSV")
	state = fields.Selection(
		string = 'Resultado',
		default = '',
		required = False,
		selection = [
			('testeando', 'Testeando'),
			('ejecutando', 'Ejecutando'),
			('finok', 'Fin Ok'),
			('finerror', 'Fin Error'),
			('cancelado', 'Cancelado'),
		],
	)
	progress = fields.Char(string="Progreso")
	last_progress = fields.Datetime(string="Último progreso")
	logger_count_infos = fields.Integer(string="Total %s" % 'infos')
	logger_count_warnings = fields.Integer(string="Total %s" % 'warnings')
	logger_count_errors = fields.Integer(string="Total %s" % 'errors')

	logs = fields.One2many('sumex_apps_imports_csv_logger', 'import_id', string="Logs")

	cancel_now = fields.Boolean()
	last_progress_commit_time = fields.Float()

	def cancel_action(self):

		self._update({
			'cancel_now': True,
			'state': "cancelado"
		})

	def test_now_action(self):

		self._import_now(True)
		return

	def import_now_action(self):

		self._import_now()
		return

	def _import_now(self, test = False):

		self.last_progress_commit_time = False
		if self.state == "ejecutando":  # No permitir ejecutar esta tarea si ya está marcada como ejecutando
			raise UserError("Esta importación está marcada como 'ejecutando'")
		if self.state == "testeando":  # No permitir ejecutar esta tarea si ya está marcada como ejecutando
			raise UserError("Esta importación está marcada como 'testeando'")

		if not self.import_name:  # Comprobar que el objeto importador existe
			self._update({'state': 'finerror'})
			self._insert_log(self.id, 'error', False, 'import name not found as object')
			raise UserError("Has de seleccionar 'Nombre de importador'")

		try:
			import_obj = self.env[self.import_name].sudo()
		except Exception as e:
			raise UserError(str(e))

		import_fields = import_obj.get_import_fields()

		if not self.file:
			self._update({'state': 'finerror'})
			self._insert_log(self.id, 'error', False, 'csv file is empty')
			return

		self._clear_log(self.id)  # Borrar log de esta tarea

		# Leer fichero CSV
		csv_content = self._read_csv_content()
		if not csv_content:
			self._insert_log(self.id, 'error', False, 'csv file has no content or wrong format')
			self._update({'state': 'finerror'})
			return
		file_csv_header = csv_content[0]
		file_csv_header = self._get_sanitized_csv_row(file_csv_header)
		file_csv_content = csv_content[1:]  # remove header from csv content
		if len(file_csv_header) < 2:
			self._insert_log(self.id, 'error', False, 'csv file has no content or wrong format')
			self._update({'state': 'finerror'})
			return

		required_nameitems = ['csv_column_name', 'required_header_field', 'required_value']
		import_field_num = 0
		for import_field in import_fields:
			import_field_num += 1
			for required_nameitem in required_nameitems:
				if required_nameitem not in import_field:
					self._update({'state': "finerror"})
					self._insert_log(self.id, 'error', False, "Bad format in 'import_fields' structure. Item num '%s'. Required name-item '%s'" % (import_field_num, required_nameitem))
					return False

		# Formatear header del fichero CSV como diccionario tipo {nombre_columna: posicion_columna}
		list_csv_header_fields_positions = self._get_and_test_csv_header(file_csv_header, import_fields)
		if not list_csv_header_fields_positions:
			self._insert_log(self.id, 'error', False, 'csv file has no header or wrong format')
			self._update({'state': 'finerror'})
			return

		# Setear variables iniciales y hacer commit
		row = self._get_row()
		modo = "ejecutando"
		if test:
			modo = "testeando"
		self._update({
			'state': modo,
			'cancel_now': False,
			'logger_count_infos': 0,
			'logger_count_warnings': 0,
			'logger_count_errors': 0,
			'progress': "iniciando...",
		})

		if hasattr(import_obj, 'hook_pre_process'):
			import_obj.hook_pre_process(self.company_id.id, file_csv_header, file_csv_content)

		#  Importar lineas
		file_csv_content_total_rows = len(file_csv_content) + 1
		file_csv_content_row_num = 1
		tic_start = process_time()
		self.last_progress_commit_time = process_time()
		self._progress_and_continue(file_csv_content_total_rows, file_csv_content_row_num, True)

		for file_csv_content_row in file_csv_content:

			do_continue = self._progress_and_continue(file_csv_content_total_rows, file_csv_content_row_num, False)
			if not do_continue:
				break

			file_csv_content_row_num += 1
			file_csv_content_row_dict = self._get_csv_row_as_dict_with_names(import_fields, list_csv_header_fields_positions, file_csv_content_row)  # Reestructurar la fila con formato {columna_nombre: valor, ...}

			#  Validar la fila con los campos requeridos definidos en el importador
			validate_row = self._validate_csv_value_row(import_fields, file_csv_content_row_dict)
			validate_result = self._validate_result(validate_row, file_csv_content_row_num)
			if not validate_result:
				continue

			# Validaciones del importador
			validate_row = import_obj.validate_row(file_csv_content_row_num, self.company_id.id, file_csv_content_row_dict)
			validate_result = self._validate_result(validate_row, file_csv_content_row_num)
			if not validate_result:
				continue

			if test:
				continue

			# Importación de la fila
			result = import_obj.import_row(file_csv_content_row_num, self.company_id.id, file_csv_header, file_csv_content_row_dict)
			self._validate_result(result, file_csv_content_row_num)
			if not validate_result:
				continue

		# Fin de la importacion con marca del tiempo empleado
		self._progress_and_continue(file_csv_content_total_rows, file_csv_content_row_num, True)
		t_secs = round(process_time() - tic_start)
		message = 'FIN %s secs' % t_secs
		self._insert_log(self.id, 'info', False, message)
		row = self._get_row()
		row.state = "finok"
		row._cr.commit()

		if hasattr(import_obj, 'hook_post_process'):
			import_obj.hook_post_process(self.company_id.id, file_csv_header, file_csv_content_row_dict, file_csv_content)

	def _read_csv_content(self):

		import csv
		import io
		csv_data = base64.b64decode(self.file)
		data_file = io.StringIO(csv_data.decode("utf-8"))
		data_file.seek(0)
		file_reader = []
		try:
			csv_reader = csv.reader(data_file, delimiter=self.separator)
			file_reader.extend(csv_reader)
		except Exception as e:
			self._insert_log(self.id, 'error', 0, "Exception reading file '%s'" % str(e))
			return False
		return file_reader

	def _validate_csv_value_row(self, import_fields, file_csv_content_row):

		if not file_csv_content_row:
			return {'error': "Fila vacía"}

		for import_fields_item in import_fields:
			# validar si existe el valor en la columna requerida
			fieldname = import_fields_item['csv_column_name']
			if fieldname:
				fieldname = fieldname.lower()
			required_field_value = bool(import_fields_item['required_value'])
			if required_field_value is True:
				if fieldname not in file_csv_content_row or not file_csv_content_row[fieldname] or file_csv_content_row[fieldname] == '':
					return {'error': "En esta fila la columna '%s' no tiene valor" % fieldname}
		return True

	def _get_row(self):

		row = self.env['sumex_apps_imports_csv'].sudo().search([['id', '=', self.id]], limit=1)
		if not row:
			return False
		return row

	def _validate_result(self, result, file_csv_content_row_num):

		row = False
		if isinstance(result, dict):
			type = False
			if 'info' in result:
				type = 'info'
				row = self._get_row()
				row.logger_count_infos += 1
			if 'warning' in result:
				type = 'warning'
				row = self._get_row()
				row.logger_count_warnings += 1
			if 'error' in result:
				type = 'error'
				row = self._get_row()
				row.logger_count_errors += 1
			message = result[type]
			self._insert_log(self.id, type, file_csv_content_row_num, message)
			if type == 'error':
				if row.stop_in_error:
					self._update({'state': 'finerror'})
				return False
		return True

	def _progress_and_continue(self, total, value, force = False):

		row = self._get_row()
		if not row:
			return False

		if row.print_progress_in_console:
			print("Importador CSV - %s - %s/%s" %  (row.name, value, total))

		self = row

		# Comprobar que el usuario no ha cancelado el proceso
		if row.cancel_now:
			return False

		if row.state == 'finerror':
			return False

		pass_time = process_time() - float(self.last_progress_commit_time)
		if not force and pass_time < 2:
			return True
		percent = int((100 / total) * value)
		try:
			row._update({
				'last_progress': fields.datetime.now(),
				'last_progress_commit_time': str(int(process_time())),
				'progress': "%s/%s (%s%%)" % (value, total, percent)
			})
			row._cr.commit()
		except:
			pass

		return True

	def _get_and_test_csv_header(self, file_csv_header, import_fields):

		list_csv_header_fields_positions = {}
		if len(file_csv_header) < 2:
			self._update({'state': "finerror"})
			self._insert_log(self.id, 'error', False, 'csv file header wrong format')
			return False
		for import_fields_item in import_fields:
			found = False
			i = -1
			for file_csv_header_item in file_csv_header:
				if not file_csv_header_item:
					pass
				i += 1
				try:
					file_csv_header_item = file_csv_header_item.lower()
				except:
					pass
				if file_csv_header_item == import_fields_item['csv_column_name'].lower():
					found = True
					list_csv_header_fields_positions[i] = file_csv_header_item
					break
			if import_fields_item['required_header_field'] is True and not found:
				self._update({'state': "finerror"})
				self._insert_log(self.id, 'error', False, 'csv file has no header text %s' % import_fields_item['csv_column_name'])
				return False
		return list_csv_header_fields_positions

	def _get_sanitized_csv_row(self, file_csv_row):

		new_csv_list = []
		for item in file_csv_row:
			item = item.strip().replace('"', '')
			new_csv_list.append(item)
		return new_csv_list

	def _get_csv_row_as_dict_with_names(self, import_fields, list_csv_header_fields_positions, file_csv_content_row):

		file_csv_content_row_list = {}
		for import_field in import_fields:
			csv_column_name = import_field['csv_column_name'].strip().lower()
			file_csv_content_row_list[csv_column_name] = ''

		sanitized_file_csv_content_row = self._get_sanitized_csv_row(file_csv_content_row)
		i = -1
		for file_csv_content_row_value in sanitized_file_csv_content_row:
			i += 1
			if i in list_csv_header_fields_positions:
				csv_column_name = list_csv_header_fields_positions[i].lower()
				file_csv_content_row_value = str(file_csv_content_row_value)
				if file_csv_content_row_value.lower() == "false":
					file_csv_content_row_value = ''
				file_csv_content_row_list[csv_column_name] = file_csv_content_row_value

		return file_csv_content_row_list

	def _clear_log(self, import_id):

		import_logger_obj = self.env['sumex_apps_imports_csv_logger'].sudo()
		import_logger_obj._clear_log(import_id)

	def _insert_log(self, import_id, type, line_num, message):

		import_logger_obj = self.env['sumex_apps_imports_csv_logger'].sudo()
		import_logger_obj._insert_log(import_id, type, line_num, message)

	def _update(self, dict_values):

		try:
			row = self._get_row()
			row.write(dict_values)
			self._cr.commit()
		except Exception as e:
			self._insert_log(self.id, 'error', '0', str(e))
			print("Excepcion '%s' msg = %s" % (__name__, str(e)))
			exit(1)


class sumex_apps_imports_csv_logger(models.Model):

	_name = 'sumex_apps_imports_csv_logger'
	_description = "Logs del importador csv"

	import_id = fields.Many2one(
		comodel_name = "sumex_apps_imports_csv",
		string="Import ID",
		required=True
	)

	type = fields.Selection(
		string = 'Tipo',
		selection = [
			('info', 'info'),
			('warning', 'warning'),
			('error', 'error'),
		],
	)

	line_num = fields.Integer(string = "Linea")

	message = fields.Char(string = "mensaje")

	def _clear_log(self, import_id):

		import_logger_obj = self.env['sumex_apps_imports_csv_logger'].sudo()
		obj_rows = import_logger_obj.search([('import_id', '=', import_id)])
		if obj_rows:
			obj_rows.sudo().unlink()
		import_logger_obj._cr.commit()

	def _insert_log(self, import_id, type, line_num, message):

		import_logger_obj = self.env['sumex_apps_imports_csv_logger'].sudo()
		if not line_num:
			line_num = 0
		import_logger_obj.sudo().create({
			'import_id': import_id,
			'type': type,
			'line_num': line_num,
			'message': message
		})
		import_logger_obj._cr.commit()
