# -*- coding: utf-8 -*-

from odoo import models, fields, api

class my_module(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    
    
    purchase_price_usd = fields.Float(compute="_value_purchase_price", string="Precio compra USD")
    

    @api.depends('variant_seller_ids', 'variant_seller_ids.price', 'variant_seller_ids.currency_id')
    def _value_purchase_price(self):
        purchase_price_usd = 0.0
        for elem in self.variant_seller_ids:
            if elem.currency_id:
                if elem.currency_id.name == 'USD':
                    purchase_price_usd = elem.price
                    break
        self.purchase_price_usd = purchase_price_usd
        
        
    tasa_cambio_divisa = fields.Float(string="Tasa cambio divisa", default=1.1)
    tasa_arancel = fields.Float(string="Arancel (%)", default=17.0)
    tasa_transporte = fields.Float(string="Transporte (%)", default=10)
    
    
    purchase_cost_final = fields.Float(compute="_calculate_cost", string="Precio de coste calculado (€)")
    
    incremento_venta = fields.Float(string="Incremento venta (%)")
    
    precio_venta = fields.Float(compute="_calculate_sale_price", string="Precio de venta calculado (€)")
    

    @api.depends('variant_seller_ids', 'tasa_cambio_divisa', 'tasa_arancel', 'tasa_transporte')
    def _calculate_cost(self):
        for record in self:
            purchase_cost_final = record.purchase_price_usd
            purchase_cost_final = purchase_cost_final / record.tasa_cambio_divisa
            
            
            if record.tasa_arancel > 0:
                precio_arancel = (record.tasa_arancel/100) * purchase_cost_final
            if record.tasa_transporte > 0:
                precio_trasnporte = (record.tasa_transporte/100) * purchase_cost_final
                
            purchase_cost_final = purchase_cost_final + precio_arancel + precio_trasnporte
            
            
            
            
            record.precio_venta = purchase_cost_final
            if record.incremento_venta > 0.0:
                incremento = 1 + (record.incremento_venta / 100)
                record.precio_venta = purchase_cost_final * incremento
            
    
        

    def update_costs(self):
        for record in self:
        
            if record.product_variant_count > 1:
                for variant in record.product_variant_ids:
                    variant.standard_price = record.purchase_cost_final

            record.standard_price = record.purchase_cost_final
            
    def update_sale_price(self):
        for record in self:
        
            if record.product_variant_count > 1:
                for variant in record.product_variant_ids:
                    variant.standard_price = record.purchase_cost_final

            record.standard_price = record.purchase_cost_final
            
            
    
    

    @api.depends('variant_seller_ids', 'tasa_cambio_divisa', 'tasa_arancel', 'tasa_transporte')
    def _calculate_cost(self):
        purchase_cost_final = self.purchase_price_usd
        purchase_cost_final = purchase_cost_final / self.tasa_cambio_divisa
