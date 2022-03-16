# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PhotostockProductTemplateInherit(models.Model):

	_description = "photostock extension de producto_template"
	_inherit = 'product.template'


	photostock_include = fields.Boolean(string = "Photostock Inclusión", required = False)

	photostock_marca_id = fields.Many2one('sumex.photostock_marcas', string = 'Marca', required = False)
	photostock_categoria_id = fields.Many2one('sumex.photostock_categorias', string = 'Categoria', required = False)
	photostock_catalogo_pagina = fields.Integer(string = "Catálogo página", required = False)
	photostock_homologaciones = fields.Char(string = "Homologaciones", required = False)
	photostock_proveedor = fields.Char(string = "Proveedor", required = False)
	photostock_fabricado_en = fields.Char(string = "Fabricado_en", required = False)
	photostock_material_producto = fields.Char(string = "Material_producto", required = False)
	photostock_color = fields.Char(string = "Color", required = False)
	photostock_tipo_packaging = fields.Char(string = "Tipo packaging", required = False)
	photostock_medidas_packaging_cm = fields.Char(string = "Medidas packaging cm", required = False)
	photostock_peso_packaging_kg = fields.Char(string = "Peso packaging kg", required = False)
	photostock_medidas_producto_cm = fields.Char(string = "Medidas producto cm", required = False)
	photostock_peso_producto_kg = fields.Char(string = "Peso producto kg", required = False)
	photostock_cantidad_master_box = fields.Char(string = "Cantidad master box", required = False)
	photostock_medidas_master_box_cm = fields.Char(string = "Medidas master box cm", required = False)
	photostock_peso_bruto_master_kg = fields.Char(string = "Peso bruto master kg", required = False)
	photostock_peso_neto_master_kg = fields.Char(string = "Peso neto master kg", required = False)
	photostock_volumen_master_box_m3 = fields.Char(string = "Volumen master box m3", required = False)
	photostock_cantidad_inner_box = fields.Char(string = "Cantidad inner box", required = False)
	photostock_medidas_inner_box_cm = fields.Char(string = "Medidas inner box cm", required = False)
	photostock_peso_bruto_inner_kg = fields.Char(string = "Peso bruto inner kg", required = False)
	photostock_peso_neto_inner_kg = fields.Char(string = "Peso neto inner kg", required = False)
	photostock_volumen_inner_box_m3 = fields.Char(string = "Volumen inner box m3", required = False)
	photostock_imagen_num_defecto = fields.Char(string = "Imagen num defecto", required = False)
	photostock_disponible_en_region_espana = fields.Char(string = "Disponible en region espana", required = False)
	photostock_disponible_en_region_portugal = fields.Char(string = "Disponible en region portugal", required = False)
	photostock_disponible_en_region_francia = fields.Char(string = "Disponible en region francia", required = False)
	photostock_disponible_en_region_europa = fields.Char(string = "Disponible en region europa", required = False)
	photostock_disponible_en_region_usa = fields.Char(string = "Disponible en region usa", required = False)

	# imagenes
	photostock_product_template_image_ids = fields.One2many('product.image', 'photostock_product_tmpl_id', string = "Photostock imagenes")  # Este hace que el dialogo de adjuntar fotos pete
	photostock_product_template_image_ids_count = fields.Integer(string="Total de imágenes", store=True, compute="_compute_photostock_product_template_image_ids_count")

	# manuales
	photostock_manual_ids = fields.Many2many('sumex.photostock_manuales', string='PhotoStock Manuales', required = False)
	photostock_manual_ids_count = fields.Integer(string="Total de manuales", store=True, compute="_compute_photostock_manual_ids_count")

	# certificados
	photostock_certificado_ids = fields.Many2many('sumex.photostock_certificados', string='PhotoStock Certificados', required = False)
	photostock_certificado_ids_count = fields.Integer(string="Total de certificados", store=True, compute="_compute_photostock_certificado_ids_count")

	@api.depends('photostock_product_template_image_ids')
	def _compute_photostock_product_template_image_ids_count(self):

		for record in self:
			record.photostock_product_template_image_ids_count = len(record.photostock_product_template_image_ids)

	@api.depends('photostock_manual_ids')
	def _compute_photostock_manual_ids_count(self):

		for record in self:
			record.photostock_manual_ids_count = len(record.photostock_manual_ids)

	@api.depends('photostock_certificado_ids')
	def _compute_photostock_certificado_ids_count(self):

		for record in self:
			record.photostock_certificado_ids_count = len(record.photostock_certificado_ids)

	@api.model
	def create(self, vals_list):

		if 'from_import_csv_name' not in self._context or self._context['from_import_csv_name'] != 'sumex_apps_imports_csv_import_photostock_productos':
			return super(PhotostockProductTemplateInherit, self).create(vals_list)
		vals_list['photostock_include'] = True
		rows = super(PhotostockProductTemplateInherit, self).create(vals_list)
		return rows

	def write(self, vals_list):

		if 'from_import_csv_name' not in self._context or self._context['from_import_csv_name'] != 'sumex_apps_imports_csv_import_photostock_productos':
			return super(PhotostockProductTemplateInherit, self).write(vals_list)
		vals_list['photostock_include'] = True
		rows = super(PhotostockProductTemplateInherit, self).write(vals_list)
		return rows
