# -*- coding: utf-8 -*-

from odoo import models
import base64
import os
from urllib.parse import urlparse


class sumex_apps_imports_csv_import_photostock_productos(models.AbstractModel):

	_description = __name__

	_import_fields = [

		# Campos que participan en la importacion del modelo
		{'csv_column_name': 'referencia', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'ean', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'nombre_es', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'observaciones_es', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'creado_en', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'creado_por', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'marca_nombre', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'categoria_nombre_es', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'fotos', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'manuales', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'certificados', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'actualizado_en', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'actualizado_por', 'required_header_field': True, 'required_value': False},
		{'csv_column_name': 'imagen_num_defecto', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_imagen_num_defecto'},

		# Campos que NO participan en la importacion del modelo, pero se incluyen a nivel informativo
		{'csv_column_name': 'catalogo_pagina', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_catalogo_pagina'},
		{'csv_column_name': 'homologaciones', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_homologaciones'},
		{'csv_column_name': 'proveedor', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_proveedor'},
		{'csv_column_name': 'fabricado_en', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_fabricado_en'},
		{'csv_column_name': 'material_producto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_material_producto'},
		{'csv_column_name': 'color', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_color'},
		{'csv_column_name': 'tipo_packaging', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_tipo_packaging'},
		{'csv_column_name': 'medidas_packaging_cm', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_medidas_packaging_cm'},
		{'csv_column_name': 'peso_packaging_kg', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_peso_packaging_kg'},
		{'csv_column_name': 'medidas_producto_cm', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_medidas_producto_cm'},
		{'csv_column_name': 'peso_producto_kg', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_peso_producto_kg'},
		{'csv_column_name': 'cantidad_master_box', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_cantidad_master_box'},
		{'csv_column_name': 'medidas_master_box_cm', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_medidas_master_box_cm'},
		{'csv_column_name': 'peso_bruto_master_kg', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_peso_bruto_master_kg'},
		{'csv_column_name': 'peso_neto_master_kg', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_peso_neto_master_kg'},
		{'csv_column_name': 'volumen_master_box_m3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_volumen_master_box_m3'},
		{'csv_column_name': 'cantidad_inner_box', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_cantidad_inner_box'},
		{'csv_column_name': 'medidas_inner_box_cm', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_medidas_inner_box_cm'},
		{'csv_column_name': 'peso_bruto_inner_kg', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_peso_bruto_inner_kg'},
		{'csv_column_name': 'peso_neto_inner_kg', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_peso_neto_inner_kg'},
		{'csv_column_name': 'volumen_inner_box_m3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_volumen_inner_box_m3'},
		{'csv_column_name': 'disponible_en_region_espana', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_disponible_en_region_espana'},
		{'csv_column_name': 'disponible_en_region_portugal', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_disponible_en_region_portugal'},
		{'csv_column_name': 'disponible_en_region_francia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_disponible_en_region_francia'},
		{'csv_column_name': 'disponible_en_region_europa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_disponible_en_region_europa'},
		{'csv_column_name': 'disponible_en_region_usa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': 'photostock_disponible_en_region_usa'},

		# {'csv_column_name': 'id', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'hay_productos_relacionados', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'productos_grupos_id', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'codigo_fiscal', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'nombre_EN', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'observaciones_EN', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'nombre_FR', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'observaciones_FR', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'nombre_PT', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},
		# {'csv_column_name': 'observaciones_PT', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': True},

	]

	def get_import_fields(self):

		return self._import_fields

	def hook_pre_process(self, company_id, file_csv_header, file_csv_content):

		pass

	def hook_post_process(self, company_id, file_csv_header, file_csv_content_row_dict, file_csv_content):

		pass

	def _filter_wrong_value(self, file_csv_content_row):

		for fieldname in file_csv_content_row:
			if not isinstance(file_csv_content_row[fieldname], str):
				file_csv_content_row[fieldname] = str(file_csv_content_row[fieldname])
			if file_csv_content_row[fieldname].upper() == "NULL":
				file_csv_content_row[fieldname] = ''
			if file_csv_content_row[fieldname].upper() == "FALSE":
				file_csv_content_row[fieldname] = ''

	def validate_row(self, file_csv_content_row_num, company_id, file_csv_content_row):

		"""
			El importador ya realiza automaticamente las validaciones de 'required_header_field' y 'required_value'file_csv_content_row
			Aquí podemos validar el formato de valores y otras cuestiones

			Este método "validate_row" es ejecutado en un bucle antes de realizar la importación
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			Se puede retornar {'error':''} {'warning':''} o {'info':''} o simplemente nada.
		"""

		self._filter_wrong_value(file_csv_content_row)
		warnings = []
		product_template_model = self.env['sumex_apps_imports_csv_library'].get_model('product.template')

		if 'referencia' not in file_csv_content_row or not file_csv_content_row['referencia']:
			return {'error': "Este producto tiene campo '%s'=nulo. No se puede procesar" % 'referencia'}

		if 'nombre_es' not in file_csv_content_row or not file_csv_content_row['nombre_es']:
			warnings.append("Este producto tiene campo '%s'=nulo. Se creará el producto con referencia y número aleatorio en el nombre" % 'nombre_es')

		if file_csv_content_row['ean']:
			if product_template_model.search([('barcode', '=', file_csv_content_row['ean']), ('default_code', '!=', file_csv_content_row['referencia'])]):
				warnings.append("Este producto con referencia('%s') pretende asignar el mismo barcode('%s') que ya está asignado a otro producto, el producto se procesará sin el barcode" % (file_csv_content_row['referencia'], file_csv_content_row['ean']))

		if file_csv_content_row['nombre_es']:
			if product_template_model.search([('name', '=', file_csv_content_row['nombre_es']), ('default_code', '!=', file_csv_content_row['referencia'])]):
				warnings.append("Este producto con referencia('%s') pretende asignar el mismo nombre('%s') que ya está asignado a otro producto, el producto se procesará con otro nombre" % (file_csv_content_row['referencia'], file_csv_content_row['nombre_es']))

		if warnings:
			return {'warning': ("; ").join(warnings)}

		return True

	def import_row(self, file_csv_content_row_num, company_id, file_csv_header, file_csv_content_row):

		"""
			Este método "import_row" es ejecutado en un bucle del objeto importador(sumex_apps_imports_csv)
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			El retorno se asumirá como correcto al no ser que se retorne {'error':}
		"""

		import random
		self._filter_wrong_value(file_csv_content_row)
		product_template_model = self.env['sumex_apps_imports_csv_library'].get_model('product.template')

		if 'referencia' not in file_csv_content_row or not file_csv_content_row['referencia']:
			return True

		if 'nombre_es' in file_csv_content_row and file_csv_content_row['nombre_es']:
			if product_template_model.search([('name', '=', file_csv_content_row['nombre_es']), ('default_code', '!=', file_csv_content_row['referencia'])]):
				random_name = "pretended name repeat: %s [%s]" % (file_csv_content_row['nombre_es'], random.randint(1, 999999999))
				file_csv_content_row['nombre_es'] = random_name
		else:
			random_name = "pretended null: %s [%s]" % (file_csv_content_row['referencia'], random.randint(1, 999999999))
			file_csv_content_row['nombre_es'] = random_name

		product_template = product_template_model.search([('default_code', '=', file_csv_content_row['referencia'])], limit = 1)
		if not product_template:
			try:
				product_template = product_template_model.create({'default_code': file_csv_content_row['referencia'], 'name': file_csv_content_row['nombre_es']})
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}

		dict_other_fields = {}
		if file_csv_content_row['creado_en']:
			fecha = self.env['sumex_apps_imports_csv_library'].get_sql_fecha(file_csv_content_row['creado_en'])
			if fecha:
				dict_other_fields['create_date'] = fecha
		if file_csv_content_row['actualizado_en']:
			fecha = self.env['sumex_apps_imports_csv_library'].get_sql_fecha(file_csv_content_row['actualizado_en'])
			if fecha:
				dict_other_fields['write_date'] = fecha
		result = self.env['sumex_apps_imports_csv_library'].update_extendedd_fields(product_template, self._import_fields, file_csv_content_row, dict_other_fields)
		if isinstance(result, dict) and 'error' in result:
			return result

		# ean
		if file_csv_content_row['ean']:
			if not product_template_model.search([('barcode', '=', file_csv_content_row['ean']), ('default_code', '!=', file_csv_content_row['referencia'])]):
				try:
					product_template.write({'barcode': file_csv_content_row['ean']})
					product_template._cr.commit()
				except Exception as e:
					exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
					return {'error': exception_msg}

		# marca
		result = self._get_or_create_photostock_marca(file_csv_content_row, product_template)
		if isinstance(result, dict) and 'error' in result:
			return result

		# categoría
		result = self._set_categoria(file_csv_content_row, product_template)
		if isinstance(result, dict) and 'error' in result:
			return result

		# manuales
		manuales_url = file_csv_content_row['manuales'].split("|")
		if manuales_url:
			result = self._set_photostock_manuales(product_template, manuales_url)
			if isinstance(result, dict) and 'error' in result:
				return result

		# certificados
		certificados_url = file_csv_content_row['certificados'].split("|")
		if certificados_url:
			result = self._set_photostock_certificados(product_template, certificados_url)
			if isinstance(result, dict) and 'error' in result:
				return result

		# imagenes
		images_url = file_csv_content_row['fotos'].split("|")
		imagen_num_defecto = file_csv_content_row['imagen_num_defecto']
		if images_url:
			result = self._set_photostock_images(product_template, images_url, imagen_num_defecto)
			if isinstance(result, dict) and 'error' in result:
				return result
		return True

	def _get_or_create_photostock_marca(self, file_csv_content_row, product_template):

		try:
			photostock_marca_model = self.env['sumex_apps_imports_csv_library'].get_model('sumex.photostock_marcas')
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		marca_nombre = file_csv_content_row['marca_nombre']
		if not marca_nombre:
			return False
		marca_nombre = marca_nombre.title()
		marca = False
		marca = photostock_marca_model.search([('name', '=', marca_nombre)], limit=1)
		if not marca:
			try:
				marca = photostock_marca_model.create({'name': marca_nombre})
				photostock_marca_model._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
		try:
			product_template.write({'photostock_marca_id': marca.id})
			product_template._cr.commit()
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		return True

	def _set_categoria(self, file_csv_content_row, product_template):

		try:
			photostock_categoria_model = self.env['sumex_apps_imports_csv_library'].get_model('sumex.photostock_categorias')
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		categoria_nombre = file_csv_content_row['categoria_nombre_es']
		categoria = False
		if categoria_nombre:
			categoria = photostock_categoria_model.search([('name', '=', categoria_nombre)], limit=1)
			if not categoria:
				try:
					categoria = photostock_categoria_model.create({'name': categoria_nombre})
					photostock_categoria_model._cr.commit()
				except Exception as e:
					exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
					return {'error': exception_msg}

		if categoria:
			try:
				product_template.write({'photostock_categoria_id': categoria.id})
				product_template._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
		return True

	def _load_remote_content(self, url, cache_path = ''):

		if cache_path:
			filename = urlparse(url)
			filename = os.path.basename(filename.path)
			filename = cache_path + "/" + filename

			if os.path.isfile(filename):
				with open(filename, "rb") as f:
					content = f.read()
					try:
						encoded_string = base64.b64encode(content)
						decoded_string = base64.b64decode(encoded_string)
						return decoded_string
					except Exception as e:
						print(str(e))

		import requests
		try:
			response = requests.get(url)
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}

		if response.ok and response.content:
			return response.content

	def _set_photostock_model_related_content(self, name, model_name, model_field_name, content, item_num):

		model = self.env['sumex_apps_imports_csv_library'].get_model(model_name)
		model_row = model.search([('name', '=', name)], limit=1)
		if not model_row:
			try:
				model_row = model.create(({
					'name': name,
					model_field_name: content
				}))
				model_row._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
		return model_row

	def _set_photostock_images(self, product_template, images_url, imagen_num_defecto = 0):

		ids = []
		image_num = 0
		if imagen_num_defecto == '':
			imagen_num_defecto = 0
		imagen_num_defecto = int(imagen_num_defecto)
		imagen_num_defecto += 1
		for image_url in images_url:
			if not image_url:
				continue
			image_url = image_url.strip()
			image_num += 1
			image_remote_content = self._load_remote_content(image_url, os.path.dirname(__file__) + '/photostock_cache_files/images')
			if isinstance(image_remote_content, dict) and 'error' in image_remote_content:
				return image_remote_content
			image_name = "%s_%s" % (product_template.default_code, image_num)
			if image_remote_content:
				try:
					image_content = base64.b64encode(image_remote_content)
				except Exception as e:
					exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
					return {'error': exception_msg}
				if image_content:
					if image_num == imagen_num_defecto:
						try:
							product_template.write({'image_1920': image_content})
						except Exception as e:
							exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
							return {'error': exception_msg}
					result = self._set_photostock_model_related_content(
						name = image_name,
						model_name = 'product.image',
						model_field_name = 'image_1920',
						content = image_content,
						item_num = image_num
					)
					if isinstance(result, dict) and 'error' in result:
						return result
					ids.append(result.id)
		if ids:
			try:
				product_template.write({
					'photostock_product_template_image_ids': [(6, 0, ids)]
				})
				product_template._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}

	def _set_photostock_certificados(self, product_template, certificados_url):

		ids = []
		item_num = 0
		for item_url in certificados_url:
			if not item_url:
				continue
			item_url = item_url.strip()
			item_num += 1
			item_remote_content = self._load_remote_content(item_url, os.path.dirname(__file__) + '/photostock_cache_files/certificados')
			if isinstance(item_remote_content, dict) and 'error' in item_remote_content:
				return item_remote_content
			item_name = "%s_%s" % (product_template.default_code, item_num)
			if item_remote_content:
				try:
					item_content = base64.b64encode(item_remote_content)
				except Exception as e:
					exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
					return {'error': exception_msg}
				if item_content:
					result = self._set_photostock_model_related_content(
						name = item_name,
						model_name = 'sumex.photostock_certificados',
						model_field_name = 'file',
						content = item_content,
						item_num = item_num
					)
				if isinstance(result, dict) and 'error' in result:
					return result
				ids.append(result.id)
		if ids:
			try:
				product_template.write({
					'photostock_certificado_ids': [(6, 0, ids)]
				})
				product_template._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}

	def _set_photostock_manuales(self, product_template, manuales_url):

		ids = []
		item_num = 0
		for item_url in manuales_url:
			if not item_url:
				continue
			item_url = item_url.strip()
			item_num += 1
			item_remote_content = self._load_remote_content(item_url, os.path.dirname(__file__) + '/photostock_cache_files/manuales')
			if isinstance(item_remote_content, dict) and 'error' in item_remote_content:
				return item_remote_content
			item_name = "%s_%s" % (product_template.default_code, item_num)
			if item_remote_content:
				try:
					item_content = base64.b64encode(item_remote_content)
				except Exception as e:
					exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
					return {'error': exception_msg}
				if item_content:
					result = self._set_photostock_model_related_content(
						name = item_name,
						model_name = 'sumex.photostock_manuales',
						model_field_name = 'file',
						content = item_content,
						item_num = item_num
					)
				if isinstance(result, dict) and 'error' in result:
					return result
				ids.append(result.id)
		if ids:
			try:
				product_template.write({
					'photostock_manual_ids': [(6, 0, ids)]
				})
				product_template._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
