from odoo import models, fields


class InventoryProductWise(models.TransientModel):
    _name = "inventory.product.wise"
    _description = 'Send Inventory Product Wise'

    product_ids = fields.Many2many("amazon.vendor.central.product.ept", string="Products")
    instance_id = fields.Many2one('amazon.vendor.instance', string='Instance', help='Amazon Vendor Instance')

    def action_process(self):
        self.instance_id.export_inventory_and_stock_report()
