# -*- coding: utf-8 -*-

from odoo import api, fields, models


class photostock_certificados(models.Model):

	_name = 'sumex.photostock_certificados'
	_description = "photostock lista de de documentos de certificados"
	_sql_constraints = [('name_uniq', 'UNIQUE (name)', 'photostock_certificados_name unique name fault')]

	name = fields.Char(string = "Certificado", required = True)
	file = fields.Binary(string = "Archivo", required = True)
