# -*- coding: utf-8 -*-
from odoo import models


class sumex_apps_imports_csv_library(models.AbstractModel):

	def rollback_and_get_exception_msg(self, e):

		import sys
		exc_type, exc_obj, exc_tb = sys.exc_info()
		exception_line_num = exc_tb.tb_lineno
		msg = "EXCEPTION '%s' (line=%s) msg = %s" % (str(exc_tb.tb_frame), exception_line_num, str(e))
		self._cr.rollback()
		return msg

	def get_sql_fecha(self, fecha):

		import time
		if not fecha:
			return False
		fecha = fecha.split(".")[0]
		for format in ['%Y-%m-%d %H:%M:%S']:
			try:
				result = time.strptime(fecha, format)
				if result:
					return fecha
			except:
				return False
		return False

	def update_extendedd_fields(self, model_obj, import_fields, file_csv_content_row, dict_other_fields = False):

		if dict_other_fields:
			try:
				model_obj.write(dict_other_fields)
				model_obj._cr.commit()
			except Exception as e:
				exception_msg = self.rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}

		list_values = {}
		for field_item in import_fields:
			field_csv_name = field_item['csv_column_name'].lower()
			if 'save_as_inherit_fieldname' not in field_item or not field_item['save_as_inherit_fieldname']:
				continue
			field_odoo_name = field_item['save_as_inherit_fieldname']
			list_values[field_odoo_name] = ''
			value = ''
			if field_csv_name in file_csv_content_row:
				value = file_csv_content_row[field_csv_name]
			if field_odoo_name == "False":
				continue
			list_values[field_odoo_name] = value
		try:
			model_obj.write(list_values)
			model_obj._cr.commit()
		except Exception as e:
			exception_msg = self.rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		return True

	def get_country(self, country_name):
		
		if not country_name:
			return False

		""" CUIDADO, NO HACER QUERIES COMO EN PROVINCIAS, PORQUE LOS NOMBRES DE PAISES ESTÁN EN INGLÉS, Y EL ORM HACE LA BUSQUEDA TRADUCIDA, EL SQL A PELO NO """
		country = self.env['res.country'].sudo().search([('name', 'ilike', country_name)], limit=1)
		if country:
			return country

	def get_state(self, country, state_name):

		if not country:
			return False
		if not state_name:
			return False

		""" AQUÍ SE EJECUTA SQL SIN EL ORM, PARA PODER USAR EL 'unaccent' PARA PODER BUSCAR LAS PROVINCIAS SIN SENSIBILIDAD A LAS TILDES """
		state_name_sanitized = state_name.replace("'", "\\'")  # un simbolo ' provoca un error en la query
		state_mask = "%" + state_name_sanitized + "%"
		if country:
			sql = "CREATE EXTENSION IF NOT EXISTS unaccent; SELECT id FROM res_country_state WHERE country_id = '%s' AND unaccent(lower(name)) ilike unaccent(lower(E'%s')) LIMIT 1" % (country.id, state_mask)
		else:
			sql = "CREATE EXTENSION IF NOT EXISTS unaccent; SELECT id FROM res_country_state WHERE unaccent(lower(name)) ilike unaccent(lower(E'%s')) LIMIT 1" % state_mask
		self.env.cr.execute(sql)
		row = self.env.cr.fetchall()
		if row:
			id = row[0][0]
			state = self.env['res.country.state'].sudo().browse(id)
			return state

	def get_or_create_product_template(self, company_id, product_referencia, product_name, descripcion, precio_venta, precio_compra):

		model = self.env['product.template'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		row = model.search([
			('default_code', '=', product_referencia),
			('company_id', '=', company_id),
			('active', 'in', [True, False])
		], limit = 1)
		if row:
			try:
				row.write({
					'type': 'product',
					'company_id': company_id,
					'default_code': product_referencia,
					'name': product_name,
					'description': descripcion,
					'list_price': precio_venta,
					'standard_price': precio_compra
				})
				row._cr.commit()
			except Exception as e:
				exception_msg = self.rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
			return row
		try:
			row = model.create({
				'type': 'product',
				'company_id': company_id,
				'default_code': product_referencia,
				'name': product_name,
				'description': descripcion,
				'list_price': precio_venta,
				'standard_price': precio_compra
				# pricelist_id
			})
			row._cr.commit()
		except Exception as e:
			exception_msg = self.rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		return row

	def get_or_create_marca(self, product_template, marca_nombre):

		if not marca_nombre:
			marca_nombre = "no-name"
		photostock_marca_model = self.env['product.brand'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		marca_nombre = marca_nombre.title()
		marca_row = photostock_marca_model.search([('name', '=', marca_nombre)], limit=1)
		if marca_row:
			return marca_row
		if not marca_row:
			try:
				marca_row = photostock_marca_model.create({'name': marca_nombre})
				photostock_marca_model._cr.commit()
			except Exception as e:
				exception_msg = self.rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
		try:
			product_template.write({'brand_id': marca_row.id})
			product_template._cr.commit()
		except Exception as e:
			exception_msg = self.rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		return True

	def get_or_create_partner(
		self,
		is_company = False,
		company_id = False,
		nombre = '',
		parent_id = False,
		vat = '',
		country_name = '',
		state_name = '',
		ciudad = '',
		domicilio = '',
		cp = '',
		telefono = '',
		mobile = '',
		email = ''
	):

		domain = [
			('name', '=', nombre),
			('active', 'in', [True, False])
		]
		if vat:
			domain.append(('vat', '=', vat))
		if company_id:
			domain.append(('company_id', '=', company_id))
		if is_company:
			domain.append(('is_company', '=', True))
		else:
			domain.append(('is_company', '=', False))
		if parent_id:
			domain.append(('parent_id', '=', parent_id))
		else:
			domain.append(('parent_id', '=', False))

		country = self.get_country(country_name)
		state = self.get_state(country, state_name)

		values = {'name': nombre}
		if parent_id:
			values['parent_id'] = parent_id
		if is_company:
			values['is_company'] = is_company
		if company_id:
			values['company_id'] = company_id
		if country:
			values['country_id'] = country.id
		if state:
			values['state_id'] = state.id
		if ciudad:
			values['city'] = ciudad
		if cp:
			values['zip'] = cp
		if domicilio:
			values['street'] = domicilio
		if telefono:
			values['phone'] = telefono
		if mobile:
			values['mobile'] = mobile
		if email:
			values['email'] = email
		if vat:
			values['vat'] = vat
		if parent_id:
			values['parent_id'] = parent_id

		model_res_partner = self.env['res.partner'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		partner = model_res_partner.search(domain, limit=1)
		if not partner:
			try:
				partner = model_res_partner.create(values)
				partner._cr.commit()
			except Exception as e:
				exception_msg = self.rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
		else:
			try:
				partner.write(values)
				partner._cr.commit()
			except Exception as e:
				exception_msg = self.rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}

		return partner

	def get_or_create_payment_term(self, payment_name):

		model_account_payment = self.env['account.payment.term'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		payment_term = model_account_payment.search([
			('name', '=', payment_name),
			('active', 'in', [True, False])
		])
		if payment_term:
			return payment_term
		try:
			payment_term = model_account_payment.create({'name': payment_name})
			payment_term._cr.commit()
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		return payment_term

	def get_or_create_location(self, company_id, location_parent_name, location_name, posx = 0, posy = 0, posz = 0):

		stock_model = self.env['stock.location'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		location_parent_id = False
		if location_parent_name:
			location_parent = stock_model.search([
				('company_id', '=', company_id),
				('name', '=', location_parent_name),
				('active', 'in', [True, False])
			], limit = 1)
			if location_parent:
				location_parent_id = location_parent.id
			if not location_parent:
				return {'error': "No existe la ubicación '%s'" % location_parent_name}
		location_row = stock_model.search([
			('company_id', '=', company_id),
			('name', '=', location_name),
			('active', 'in', [True, False])
		], limit=1)
		if not location_row:
			try:
				location_row = location_row.create({'name': location_name})
				stock_model._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
		try:
			location_row.write({
				'company_id': company_id,
				'location_id': location_parent_id,
				'posx': posx,  # Pasillo (X)
				'posy': posy,  # Estantería (Y)
				'posz': posz,  # Altura (Z)
			})
			stock_model._cr.commit()
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}

		return location_row

	def get_or_create_company(self, company_id, company_name, vat, country_name, state_name, domicilio, ciudad, cp, telefono, email):

		country = self.env['sumex_apps_imports_csv_library'].sudo().get_country(country_name)
		state = self.env['sumex_apps_imports_csv_library'].sudo().get_state(country, state_name)
		company_model = self.env['res.company'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		company_row = company_model.search([('name', '=', company_name)], limit=1)
		if not company_row:
			try:
				company_row = company_model.create({
					'name': company_name,
					'city': ciudad,
					'zip': cp,
					'street': domicilio,
					'phone': telefono,
					'email': email,
					'vat': vat,
					'country_id': country.id if country else False,
					'state_id': state.id if state else False
				})
				company_model._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
		try:
			company_row.write({
				'name': company_name,
				'city': ciudad,
				'zip': cp,
				'street': domicilio,
				'phone': telefono,
				'email': email,
				'vat': vat,
				'country_id': country.id if country else False,
				'state_id': state.id if state else False
			})
			company_model._cr.commit()
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}

		return company_row
