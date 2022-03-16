# -*- coding: utf-8 -*-

from odoo import api, fields, models


class photostock_manuales(models.Model):

	_name = 'sumex.photostock_manuales'
	_description = "photostock lista de documentos de manuales"
	_sql_constraints = [('name_uniq', 'UNIQUE (name)', 'photostock_manuales unique name fault')]

	name = fields.Char(string = "Certificado", required = True)
	file = fields.Binary(string = "Archivo", required = True)
