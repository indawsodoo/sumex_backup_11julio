# -*- coding: utf-8 -*-

from odoo import models, fields, api

class my_module(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    
    
    unidades_cs = fields.Integer(string="Unidades/cs")
    vol_cl = fields.Float(string="Vol. Cl")
    avb_porcentaje = fields.Float(string="AVB %")
    
    TIPOS_REF = [('REF','REF'),   
                ('NRF','NRF'),
                ('CAN','CAN'),
                ('PET','PET'),
                ('NRB','NRB'),
             ]
    type_ref = fields.Selection(selection=TIPOS_REF, string='Tipo')
    
    grado_plato = fields.Float(string="Grado plato")
    peso_kg_botella = fields.Float(string="Peso kg/bot")
    cajas_palet = fields.Integer(string="Cajas/Palet")
    cajas_capa = fields.Integer(string="Cajas/Capa")
    capas_palet = fields.Integer(string="Capas/Palet")
    botellas_palet = fields.Integer(string="Botellas/Palet")
    peso_kg_caja = fields.Float(string="Peso kg/caja")
    peso_kg_palet = fields.Float(string="Peso kg/palet")
    largo_mm_caja = fields.Integer(string="Largo mm caja")
    ancho_mm_caja = fields.Integer(string="Ancho mm caja")
    alto_mm_caja = fields.Integer(string="Alto mm caja")
    cod_excise = fields.Char(string="Código Excise")
    cod_tiba = fields.Char(string="Código TIBA")
    grupo_cotizacion = fields.Char(string="Grupo cotización")
    iiee_precinta_spain = fields.Float(string="IIEE precinta España", digits=(12,6))
    iiee_precinta_canario = fields.Float(string="IIEE precinta Canarias", digits=(12,6))
    iiee_precinta_portugal = fields.Float(string="IIEE precinta Portugal", digits=(12,6))
    
    