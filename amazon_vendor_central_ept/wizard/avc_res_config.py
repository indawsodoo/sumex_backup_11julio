""" This file used for manage the functionality of amazon vendor instance."""
from odoo import models, fields, _
from odoo.exceptions import UserError, Warning


class AvcResConfig(models.TransientModel):
    """
        Usage: Manage the functionality of Amazon Vendor Instance.
    """
    _name = 'avc.res.config'
    _description = 'Amazon Vendor Central Instance Config'

    name = fields.Char(string="Vendor Name", help="Specify the Unique Name of the Vendor")
    avc_vendor_code = fields.Char('Vendor code', help="Vendor Central code, Goto Amazon Vendor Central Portal ->"
                                                  " Message Dashboard -> Current Profile")
    country_id = fields.Many2one(comodel_name='res.country', string="Country",
                                 help="The Order Requisitions are creates based on below selected country")
    company_id = fields.Many2one(comodel_name='res.company', string='Vendor Company',
                                 default=lambda self: self.env.company,
                                 help="The Order Requisitions are creates based on below selected company")
    supplier = fields.Char(string="Supplier Id",
                           help="Amazon Supplier Id available in Global Settings -> Message Format -> "
                                "Message Format Identifiers -> Your identifiers of Vendor Central Portal")
    amazon_vendor_qualifier = fields.Char(string="Amazon Qualifier", default="14",
                                          help="Amazon Qualifier available in Global Settings "
                                               "-> Message Format -> "
                                               "Message Format Identifiers -> "
                                               "Your identifiers of Vendor Central Portal")
    # account_type = fields.Selection(string='Account Type',
    #                                 selection=[('first_order', 'First Order'), ('back_order', 'Back Order'), ],
    #                                 default='first_order', help="This will identifying the type of the Vendor Account")
    is_production_environment = fields.Boolean(string="Production Environment",
                                               help="This will identifying the instance is used for "
                                                    "test or production environment")
    sender_ftp_connection_id = fields.Many2one(comodel_name='ftp.server.ept',
                                               string="Test Sender FTP server",
                                               domain=[('ftp_type', '=', 'sender')],
                                               help="Used for, identifying in which place the "
                                                    "file should be uploaded")
    receiver_ftp_connection_id = fields.Many2one(comodel_name='ftp.server.ept',
                                                 string="Test Receiver FTP server",
                                                 domain=[('ftp_type', '=', 'receiver')],
                                                 help="Used for, identifying from which place the file "
                                                      "should be downloaded")
    production_sender_ftp_connection_id = fields.Many2one(comodel_name='ftp.server.ept',
                                                          string=" Production Sender FTP server",
                                                          domain=[('ftp_type', '=', 'sender')],
                                                          help="Used for, identifying in which "
                                                               "place the file "
                                                               "should be uploaded")
    production_receiver_ftp_connection_id = fields.Many2one(comodel_name='ftp.server.ept',
                                                            string="Production Receiver FTP server",
                                                            domain=[('ftp_type', '=', 'receiver')],
                                                            help="Used for, identifying from which "
                                                                 "place the file "
                                                                 "should be downloaded")

    def create_amazon_vendor_instance(self):
        """
            Create the amazon vendor instance.and check the validation for the vendor. If user
            wants to create the same name user second time so that raise the warning
        """
        vendor_exist = self.env['amazon.vendor.instance'].search(
            ['|', ('name', '=', self.name), ('supplier_id', '=', self.supplier)])
        if vendor_exist:
            raise UserError(_('This named Vendor already exist with same configuration...! \n'
                              'Make sure, The Vendor Name and Supplier Id must be Unique'
                              ' With Existing Instance Configurations'))

        vals = {
            'name': self.name,
            'avc_vendor_code': self.avc_vendor_code,
            'supplier_id': self.supplier,
            'country_id': self.country_id.id,
            'company_id': self.company_id.id,
            # 'account_type': self.account_type,
            'avc_amazon_qualifier': self.amazon_vendor_qualifier,
            'is_production_environment': self.is_production_environment,
            'sender_ftp_connection_id': self.sender_ftp_connection_id.id,
            'receiver_ftp_connection_id': self.receiver_ftp_connection_id.id,
            'production_sender_ftp_connection_id': self.production_sender_ftp_connection_id.id,
            'production_receiver_ftp_connection_id': self.production_receiver_ftp_connection_id.id
        }
        try:
            self.env['amazon.vendor.instance'].create(vals)
        except Exception as error:
            raise Warning(_(str(error)))
