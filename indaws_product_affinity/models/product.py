# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ProductLabelLine(models.Model):
    _inherit = "product.label.line"

    _sql_constraints = [('product_tmpl_id', 'unique (product_tmpl_id,website_id,label)',
                         'Duplicate records in label line not allowed !')]

class my_module(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'


    unidades_cs = fields.Integer(string="Unidades/cs")
    vol_cl = fields.Float(digits=(10, 2), string="Vol. Cl")
    avb_porcentaje = fields.Float(digits=(10, 2), string="AVB %")

    TIPOS_REF = [('REF','REF'),
                ('NRF','NRF'),
                ('CAN','CAN'),
                ('PET','PET'),
                ('NRB','NRB'),
             ]
    type_ref = fields.Selection(selection=TIPOS_REF, string='Tipo')

    grado_plato = fields.Float(digits=(10, 2), string="Grado plato")
    peso_kg_botella = fields.Float(digits=(10, 3), string="Peso kg/bot")
    cajas_palet = fields.Integer(string="Cajas/Palet")
    cajas_capa = fields.Integer(string="Cajas/Capa")
    capas_palet = fields.Integer(string="Capas/Palet")
    botellas_palet = fields.Integer(string="Botellas/Palet")
    peso_kg_caja = fields.Float(digits=(10, 0), string="Peso kg/caja")
    peso_kg_palet = fields.Float(digits=(10, 2), string="Peso kg/palet")
    largo_mm_caja = fields.Integer(string="Largo mm caja")
    ancho_mm_caja = fields.Integer(string="Ancho mm caja")
    alto_mm_caja = fields.Integer(string="Alto mm caja")
    cod_excise = fields.Char(string="Código Excise")
    cod_tiba = fields.Char(string="Código TIBA")
    grupo_cotizacion = fields.Char(string="Grupo cotización")
    iiee_precinta_spain = fields.Float(string="IIEE precinta España", digits=(12, 3))
    iiee_precinta_canario = fields.Float(string="IIEE precinta Canarias", digits=(12, 3))
    iiee_precinta_portugal = fields.Float(string="IIEE precinta Portugal", digits=(12, 3))
    label = fields.Char(compute="_compute_label", string="Label", store=True)

    @api.depends('label_line_ids')
    def _compute_label(self):
        for record in self:
            aux = ''
            if record.label_line_ids:
                for item in record.label_line_ids:
                    if aux != '':
                        record.label = record.label + aux + item.label.name
                    else:
                        record.label = item.label.name
                        aux = ' - '
            else:
                record.label = ''

    def write(self, vals):
        for record in self:
            result = super(my_module, record).write(vals)
            if 'label' in vals:
                record._onchange_label()
        return result

    def _onchange_label(self):
        for record in self:
            if record.label:
                label = record.env['product.label'].search([('name', 'like', '%' + record.label + '%')], limit=1)
                if len(label) <= 1:
                    label = record.env['product.label'].create({
                        'name': record.label,
                        'label_style': 'style_1'
                    })
                record.label_line_ids.unlink()
                record.label_line_ids.create({
                    'product_tmpl_id': record.id,
                    'website_id': record.env['website'].search([('theme_id.author', 'like', 'Emipro Technologies Pvt. Ltd.')], limit=1).id,
                    'label': label.id
                })
            else:
                record.label_line_ids.unlink()