""" This file is inherit the existing functionality of ftp server and add its new functionality"""
from odoo import models, fields, _
from odoo.exceptions import UserError


class FtpServerEpt(models.Model):
    """
        Inherit the existing functionality and add its new functionality
    """
    _inherit = "ftp.server.ept"

    ftp_type = fields.Selection([('sender', 'Sender FTP'), ('receiver', 'Receiver FTP')],
                                string="FTP Type")
    po_file_import_prefix = fields.Char('PO Import File Prefix')
    po_ack_file_export_prefix = fields.Char('PO Ack Export File Prefix')
    inventory_file_export_prefix = fields.Char('Inventory File Prefix')
    invoice_file_export_prefix = fields.Char('Invoice File Prefix')
    asn_file_export_prefix = fields.Char('Shipment Notice File Prefix')
    sales_report_file_export_prefix = fields.Char('Sales report File Prefix')
    default_upload_dir_id = fields.Many2one('ftp.directory.ept', string='Default Upload Path')
    default_receive_dir_id = fields.Many2one('ftp.directory.ept', string='Default Download Path')

    def get_ftp_server(self, instance, is_sender_ftp_server=False, is_cron=False):
        """
            Used for find the ftp server based om instance.
            :param instance: amazon.vendor.instance()
            :param is_sender_ftp_server: Boolean
            :param is_cron: Boolean
            :return: ftp.server.ept()
        """
        if instance.is_production_environment:
            if is_sender_ftp_server:
                ftp_server = instance.production_sender_ftp_connection_id
                if ftp_server:
                    message = self.check_ftp_server_type(ftp_server, is_cron, is_sender_ftp_server)
                    if message:
                        return message

                field_string = instance._fields['production_sender_ftp_connection_id'] \
                               and instance._fields[
                                   'production_sender_ftp_connection_id'].string
            else:
                ftp_server = instance.production_receiver_ftp_connection_id
                if ftp_server:
                    message = self.check_ftp_server_type(ftp_server, is_cron)
                    if message:
                        return message

                field_string = instance._fields['production_receiver_ftp_connection_id'] \
                               and instance._fields[
                                   'production_receiver_ftp_connection_id'].string
            if not ftp_server:
                message = "Please Select the Production Receiver FTP server. \n " \
                          "- Goto : Configuration -> Instances -> {} -> {}". \
                    format(instance.display_name, field_string)
                if is_cron:
                    return message
                raise UserError(_(message))
        else:
            if is_sender_ftp_server:
                ftp_server = instance.sender_ftp_connection_id
                if ftp_server:
                    message = self.check_ftp_server_type(ftp_server, is_cron, is_sender_ftp_server)
                    if message:
                        return message

                field_string = instance._fields['sender_ftp_connection_id'] \
                               and instance._fields \
                                   ['sender_ftp_connection_id'].string
            else:
                ftp_server = instance.receiver_ftp_connection_id
                if ftp_server:
                    message = self.check_ftp_server_type(ftp_server, is_cron)
                    if message:
                        return message

                field_string = instance._fields['receiver_ftp_connection_id'] \
                               and instance._fields \
                                   ['receiver_ftp_connection_id'].string
            if not ftp_server:
                message = "Please Select the Test Receiver FTP server. \n " \
                          "- Goto : Configuration -> Instances -> {} -> {} ". \
                    format(instance.display_name, field_string)
                if is_cron:
                    return message
                raise UserError(_(message))
        return ftp_server

    def check_ftp_server_type(self, ftp_server, is_cron, is_sender_server=False):
        """
            :param ftp_server: ftp.server.ept()
            :param is_cron: Boolean
            :param is_sender_server: Boolean
            :return:
        """
        message = ''
        if is_sender_server:
            if not ftp_server.ftp_type == 'sender':
                message = "Please select the ftp type is ['Sender FTP'] of " \
                          "FTP Server {}!".format(ftp_server.display_name)
                if is_cron:
                    return message
                raise UserError(_(message))
            if not ftp_server.default_upload_dir_id:
                field_string = ftp_server._fields['default_upload_dir_id'] \
                               and ftp_server._fields[
                                   'default_upload_dir_id'].string
                message = "Please Select the {}. \n " \
                          "-   For Select the Directory \n " \
                          "-   Goto : Configuration -> SFTP -> {} -> {}". \
                    format(field_string, ftp_server.display_name, field_string)
                if is_cron:
                    return message
                raise UserError(_(message))
        else:
            if not ftp_server.ftp_type == 'receiver':
                message = "Please select the ftp type is ['Receiver FTP']" \
                          " of FTP Server {}!".format(ftp_server.display_name)
                if is_cron:
                    return message
                raise UserError(_(message))
            if not ftp_server.default_receive_dir_id:
                field_string = ftp_server._fields['default_receive_dir_id'] \
                               and ftp_server._fields[
                                   'default_receive_dir_id'].string
                message = "Please Select the {}. \n " \
                          "-   For Select the Directory \n " \
                          "-   Goto : Configuration -> SFTP -> {} -> {}". \
                    format(field_string, ftp_server.display_name, field_string)
                if is_cron:
                    return message
                raise UserError(_(message))
        return message
