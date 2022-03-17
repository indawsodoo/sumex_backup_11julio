""" The usage of this file is inherit the existing res config settings
functionality and added its new functionality. """
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """
        Usage: Inherit the existing functionality and added its new functionality
    """
    _inherit = 'res.config.settings'

    def _get_current_company_instances(self):
        """
            Usage: Return the domain which will display the current company instances
            :return: Domain
        """
        return [('company_id', '=', self.env.company.id)]

    avc_vendor_instance_id = fields.Many2one('amazon.vendor.instance', string='Vendor', ondelete="cascade",
                                             domain=_get_current_company_instances)
    avc_supplier = fields.Char("Supplier ID", help="Amazon Supplier Id available in Global Settings -> "
                                                   "Message Format -> Message Format Identifiers -> "
                                                   "Your identifiers of Vendor Central Portal")
    avc_file_format = fields.Selection([('edi_fact', 'EDI FACT'), ], default='edi_fact',
                                       string='File Format for Export',
                                       help="File format for import and export to Vendor central")
    avc_connection_type = fields.Selection([('test_connection', 'Test Connection'),
                                            ('production_connection', 'Production Connection')],
                                           string='Connection Type',
                                           help="Used for, Identifying the created instance is used in the"
                                                "Test Environment or Production Environment")
    avc_price_list_id = fields.Many2one('product.pricelist', string="Pricelist",
                                        help="List of prices of different products for customers and avc_suppliers")

    avc_order_dispatch_lead_time = fields.Integer(string="Order Lead Time", default=1,
                                                  help="The average delay in days between the Routing Request send and "
                                                       "ready for order shipment.")
    avc_edi_carrier_method = fields.Many2one('delivery.carrier', string="Amazon carrier",
                                             help="Carrier which is set in Sale Order")
    avc_is_production_environment = fields.Boolean("Production Environment",
                                                   help="This will identifying the instance is used for "
                                                        "test or production environment")
    avc_sender_ftp_connection_id = fields.Many2one('ftp.server.ept', string="Test Sender FTP server",
                                                   domain=[('ftp_type', '=', 'sender')],
                                                   help="Used for, identifying in which place "
                                                        "the file should be uploaded")
    avc_receiver_ftp_connection_id = fields.Many2one('ftp.server.ept', string="Test Receiver FTP server",
                                                     domain=[('ftp_type', '=', 'receiver')],
                                                     help="Used for, identifying from which place the file "
                                                          "should be downloaded")
    avc_production_sender_ftp_connection_id = fields.Many2one('ftp.server.ept', string="Production Sender FTP server",
                                                              domain=[('ftp_type', '=', 'sender')],
                                                              help="Used for, identifying in which place the file "
                                                                   "should be uploaded")
    avc_production_receiver_ftp_connection_id = fields.Many2one('ftp.server.ept',
                                                                string="Production Receiver FTP server",
                                                                domain=[('ftp_type', '=', 'receiver')],
                                                                help="Used for, identifying from which place the file "
                                                                     "should be downloaded")
    avc_warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse",
                                       help='Warehouse for Sale Order Import')
    avc_vendor_code = fields.Char('Vendor code', help="Vendor Central code")
    avc_amazon_qualifier = fields.Char("Amazon Qualifier", default="14",
                                       help="Amazon Qualifier available in Global Settings "
                                            "-> Message Format -> Message Format Identifiers -> "
                                            "Your identifiers of Vendor Central Portal")
    avc_so_customer_id = fields.Many2one('res.partner', string="Sale Order Partner")
    avc_picking_policy = fields.Selection([('direct', 'Deliver each product when available'),
                                           ('one', 'Deliver all products at once')],
                                          string='Shipping Policy', default='direct', )
    avc_amazon_gln_number = fields.Char("Amazon GLN Number",
                                        help="Define Unique Amazon GLN(Global Location Number)")
    avc_warehouse_code = fields.Char("Warehouse Code",
                                     help="Warehouse Code which is configure in the vendor central portal")
    avc_warehouse_ids = fields.Many2many('stock.warehouse', string="Warehouses",
                                         help="These warehouses will be used for stock export if "
                                              "stock is available in the multiple warehouses, "
                                              "Otherwise it will take stock from that warehouse "
                                              "which is selected for Sale Order.")
    avc_product_stock_field_id = fields.Selection([('free_quantity', 'Free Quantity'),
                                                   ('forecast_quantity', 'Forecast Quantity')],
                                                  default="free_quantity",
                                                  string="Stock Type",
                                                  help="Choose the field of the product which will "
                                                       "be used for stock inventory updates."
                                                       "\nIf empty, Quantity Available is used.")
    avc_amazon_unb_id = fields.Char(string='Amazon UNB ID', help="Amazon Qualifier available in Global Settings -> "
                                                              "Message Format -> Message Format Identifiers -> "
                                                              "Test UNB ID or Production UNB ID")
    avc_journal_id = fields.Many2one('account.journal', 'Account Journal',
                                     help='Invoice is created in selected Journal')
    avc_team_id = fields.Many2one('crm.team', string="Sales Team")
    group_avc_packages = fields.Boolean("Advance Shipment Notice Packages",
                                        implied_group='amazon_vendor_central_ept.group_avc_packages',
                                        help="Send the Package details with Advance Shipment Notice "
                                             "to the Amazon Vendor Central")

    @api.onchange('group_avc_packages')
    def onchange_group_avc_packages(self):
        if self.group_avc_packages and not self.group_stock_tracking_lot:
            self.group_stock_tracking_lot = True
        elif not self.group_avc_packages:
            self.env['amazon.vendor.instance'].search([]).write({'is_use_packages': self.group_avc_packages})

    def execute(self):
        """
            Usage: Write all the changes in the amazon vendor instance.
            :return: res
        """
        vendor = self.avc_vendor_instance_id
        values = {}
        if vendor:
            values['supplier_id'] = self.avc_supplier or False
            values['avc_file_format'] = self.avc_file_format or False

            values['is_production_environment'] = False
            if self.avc_connection_type == 'production_connection':
                values['is_production_environment'] = True

            values['pricelist_id'] = self.avc_price_list_id.id
            values['order_dispatch_lead_time'] = self.avc_order_dispatch_lead_time or False
            values['amazon_edi_carrier_method'] = self.avc_edi_carrier_method.id
            values['sender_ftp_connection_id'] = self.avc_sender_ftp_connection_id.id
            values['receiver_ftp_connection_id'] = self.avc_receiver_ftp_connection_id.id
            values['production_sender_ftp_connection_id'] = self.avc_production_sender_ftp_connection_id.id
            values['production_receiver_ftp_connection_id'] = self.avc_production_receiver_ftp_connection_id.id
            values['warehouse_id'] = self.avc_warehouse_id.id
            values['avc_vendor_code'] = self.avc_vendor_code or False
            values['avc_amazon_qualifier'] = self.avc_amazon_qualifier or False
            values['so_customer_id'] = self.avc_so_customer_id.id
            values['picking_policy'] = self.avc_picking_policy or False
            values['amazon_gln_number'] = self.avc_amazon_gln_number or False
            values['warehouse_code'] = self.avc_warehouse_code or False
            values['warehouse_ids'] = [(6, 0, self.avc_warehouse_ids.ids)] if self.avc_warehouse_ids else False
            values['product_stock_field_id'] = self.avc_product_stock_field_id or False
            values['amazon_unb_id'] = self.avc_amazon_unb_id or False
            values['journal_id'] = self.avc_journal_id.id
            values['team_id'] = self.avc_team_id.id

            vendor.write(values)
        return super(ResConfigSettings, self).execute()

    @api.onchange('avc_vendor_instance_id')
    def onchange_avc_vendor_instance_id(self):
        """
            Usage: Set the values of amazon vendor instance of its corresponding res config settings fields.
        """
        vendor = self.avc_vendor_instance_id
        if vendor:
            self.avc_supplier = vendor.supplier_id or False
            self.avc_file_format = vendor.avc_file_format or False
            self.avc_connection_type = 'production_connection' if vendor.is_production_environment else 'test_connection'
            self.avc_price_list_id = vendor.pricelist_id.id
            self.avc_order_dispatch_lead_time = vendor.order_dispatch_lead_time or False
            self.avc_edi_carrier_method = vendor.amazon_edi_carrier_method or False
            self.avc_sender_ftp_connection_id = vendor.sender_ftp_connection_id.id
            self.avc_receiver_ftp_connection_id = vendor.receiver_ftp_connection_id.id
            self.avc_production_sender_ftp_connection_id = vendor.production_sender_ftp_connection_id.id
            self.avc_production_receiver_ftp_connection_id = vendor.production_receiver_ftp_connection_id.id
            self.avc_warehouse_id = vendor.warehouse_id.id
            self.avc_vendor_code = vendor.avc_vendor_code or False
            self.avc_amazon_qualifier = vendor.avc_amazon_qualifier or False
            self.avc_so_customer_id = vendor.so_customer_id.id
            self.avc_picking_policy = vendor.picking_policy or False
            self.avc_amazon_gln_number = vendor.amazon_gln_number or False
            self.avc_warehouse_code = vendor.warehouse_code or False
            self.avc_warehouse_ids = [(6, 0, vendor.warehouse_ids.ids)] if vendor.warehouse_ids else False
            self.avc_product_stock_field_id = vendor.product_stock_field_id or False
            self.avc_amazon_unb_id = vendor.amazon_unb_id or False
            self.avc_journal_id = vendor.journal_id.id
            self.avc_team_id = vendor.team_id.id
