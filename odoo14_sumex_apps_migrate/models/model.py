# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class sumex_apps_migrate(models.AbstractModel):

	_name = 'sumex_apps_migrate'
	_description = "sumex_apps_migrate"

	_existe_producto_como_referencia_sage = fields.Boolean("PRODUCTO EXISTE EN REFERENCIAS SAGE", required = False, default = False)
	_existe_variante_como_referencia_sage = fields.Char("VARIANTE EXISTE EN REFERENCIAS SAGE", required = False, default = False)

	def productos_prestashop_pasar_precios_a_tarifa_accesorios(self):

		"""
			SE EJECUTA CON:
			self.env['sumex_apps_migrate'].sudo().productos_prestashop_pasar_precios_a_tarifa_accesorios()

			OBJETIVO:
			Pasar todos los precios a tarifa accesorios (finalmente no se usa)
		"""

		tarifa_nombre = 'Accesorios y llantas'
		domain = [('name', '=', tarifa_nombre)]
		pricelist_model = self.env['product.pricelist'].sudo()
		pricelist_id = pricelist_model.search(domain)
		if not pricelist_id:
			pricelist_id = pricelist_model.create({
				'name': tarifa_nombre,
				'selectable': True
			})
			pricelist_model._cr.commit()
			print("created")
			print(pricelist_id)

		pricelist_items_model = self.env['product.pricelist.item'].sudo()
		for product in self.env['product.product'].search([
			('type', '=', 'product')
			('_created_from_import_prestashop_product_id', ">", 0)
			]):

			pricelist_item = pricelist_items_model.search([
				('pricelist_id', '=', pricelist_id.id),
				('product_tmpl_id', '=', product.product_tmpl_id.id),
				('product_id', '=', product.id)
			])
			if pricelist_item:
				continue
			pricelist_items_model.create({
				'pricelist_id': pricelist_id.id,
				'fixed_price': product.list_price,
				'product_tmpl_id': product.product_tmpl_id.id,
				'product_id': product.id
			})
			pricelist_items_model._cr.commit()


		# for product in self.env['product.product'].search([('type', '=', 'product')]):

		# 	self.sale_pricelist_id = self.env['product.pricelist'].create({
		# 		'name': 'Sale pricelist',
		# 		'item_ids': [(0, 0, {
		# 			'base': 1,
		# 			'product_id': product.id
		# 		})]
		# 	})

		return

	def productos_prestashop_marcar_existe_como_referencia_sage(self):

		"""
			SE EJECUTA CON:
			self.env['sumex_apps_migrate'].sudo().productos_prestashop_marcar_existe_como_referencia_sage()

			OBJETIVO:
			Desde la lista de referencias sage, se comprueba todos los productos.
			Se recorre todos los productos y sus variantes comparando sus referencia contra la lista de referencias sage.
			Se marcan los campos '_existe_producto_como_referencia_sage' y '_existe_variante_como_referencia_sage' según las coincidencias
		"""

		from .lista_referencias_sage import get_referencias_sage
		product_template_model = self.env['product.template'].sudo()
		product_product_model = self.env['product.product'].sudo()
		referencias_sage = get_referencias_sage()
		total = len(referencias_sage)
		counter = 0

		for referencia_sage in referencias_sage:
			counter += 1
			print("%s/%s" % (counter, total))
			row = product_template_model.search([
				('default_code', '=', referencia_sage),
				('_created_from_import_prestashop_product_id', ">", 0)
				('active', 'in', [True, False])
			])
			if row:
				row.write({'_existe_producto_como_referencia_sage': True})
			else:
				row.write({'_existe_producto_como_referencia_sage': False})
			row = product_product_model.search([
				('default_code', '=', referencia_sage),
				('_created_from_import_prestashop_product_id', ">", 0)
				('active', 'in', [True, False])
			])
			if row:
				row.write({'_existe_variante_como_referencia_sage': referencia_sage})
			else:
				row.write({'_existe_producto_como_referencia_sage': False})
			self._cr.commit()

	def productos_prestashop_precio_cero(self):

		"""
			SE EJECUTA CON:
			self.env['sumex_apps_migrate'].sudo().productos_prestashop_precio_cero()

		"""

		product_template_model = self.env['product.template'].sudo()
		products_templates = product_template_model.search([('_created_from_import_prestashop_product_id', ">", 0)])
		total = len(products_templates)
		counter = 0
		for product_template in products_templates:
			counter += 1
			print("%s/%s" % (counter, total))
			product_template.standard_price = 0
			product_template.lst_price = 0
			product_template.list_price = 0
			products = product_template.product_variant_id
			if products:
				for product in products:
					product.lst_price = 0
					product.list_price = 0
					product.price_extra = 0
		self._cr.commit()

	def productos_prestashop_pasar_a_amplusmart_company(self):

		"""
			SE EJECUTA CON:
			self.env['sumex_apps_migrate'].sudo().productos_prestashop_pasar_a_amplusmart_company()

			OBJETIVO:
			De todos los productos importados desde prestashop (_created_from_import_prestashop_product_id>0) los pasamos a la compañía "AMPLUSMART"
		"""
		company_name = 'AMPLUSMART S.L.U​.'

		company_model = self.env['res.company'].sudo()
		company = company_model.search([('name', '=', company_name)])
		if not company:
			raise UserError("No encuentro la compañía %s" % company_name)

		product_template_model = self.env['product.template'].sudo()
		products = product_template_model.search([('_created_from_import_prestashop_product_id', ">", 0)])
		products.write({'company_id': company.id})
		self._cr.commit()

	def productos_prestashop_pasar_a_sumex_company(self):

		"""
			SE EJECUTA CON:
			self.env['sumex_apps_migrate'].sudo().productos_prestashop_pasar_a_sumex_company()

			OBJETIVO:
			De todos los productos importados desde prestashop (_created_from_import_prestashop_product_id>0) los pasamos a la compañía "SUMEX"
		"""
		company_name = 'SUMEX S.A.'

		company_model = self.env['res.company'].sudo()
		company = company_model.search([('name', '=', company_name)])
		if not company:
			raise UserError("No encuentro la compañía %s" % company_name)

		product_template_model = self.env['product.template'].sudo()
		products = product_template_model.search([('_created_from_import_prestashop_product_id', ">", 0)])
		products.write({'company_id': company.id})
		self._cr.commit()

	def contactos_sage_pasar_a_sumex_company(self):

		"""
			SE EJECUTA CON:
			self.env['sumex_apps_migrate'].sudo().contactos_sage_pasar_a_sumex_company()

			OBJETIVO:
			De todos los contactos importados de sage (_created_from_sumex_apps_imports_csv_of_sage_contactos>0) los pasamos a la compañía "SUMEX"
		"""

		company_name = 'SUMEX S.A.'

		company_model = self.env['res.company'].sudo()
		company = company_model.search([('name', '=', company_name)])
		if not company:
			raise UserError("No encuentro la compañía %s" % company_name)

		partner_model = self.env['res.partner'].sudo()
		partners = partner_model.search([('_created_from_sumex_apps_imports_csv_of_sage_contactos', "=", True)])
		partners.write({'company_id': company.id})
		self._cr.commit()

	def pasar_empleados_sumex_a_sumex_company(self):

		"""
			SE EJECUTA CON:
			self.env['sumex_apps_migrate'].sudo().pasar_empleados_sumex_a_sumex_company()

			OBJETIVO:
			Todos los empleados y sus usuarios a la compañía SUMEX"
		"""

		company_name = 'SUMEX S.A.'
		company_model = self.env['res.company'].sudo()
		company = company_model.search([('name', '=', company_name)])
		if not company:
			raise UserError("No encuentro la compañía %s" % company_name)

		partner_model = self.env['res.partner'].sudo()
		employee_model = self.env['hr.employee'].sudo()
		employees = employee_model.search([])
		for employee in employees:
			print("employee=%s" % employee.name)
			employee.write({'company_id': company.id})
			employee.user_id.write({'company_id': company.id})
			employee.user_id.partner_id.write({'company_id': company.id})
			# employee.user_id.partner_id.parent_id.write({'company_id': company.partner_id})
			print(employee.user_id.partner_id.name)
			partner = partner_model.search([('id', "=", employee.user_id.partner_id.id)])
			partner.write({'company_id': company.id})
			partner.write({'parent_id': company.partner_id.id})

		self._cr.commit()
