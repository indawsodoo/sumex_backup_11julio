#!/usr/bin/python3
import logging
# import paramiko
import ftplib
from odoo import models, fields, api, _
from .sftp_interface import sftp_interface
from .api import TPWFTPInterface
from odoo.exceptions import Warning, ValidationError, UserError



_logger = logging.getLogger("=== FTP Connector ===")


class FtpServerEpt(models.Model):
    _name = "ftp.server.ept"
    _description = "Ftp Server Details"

    name = fields.Char("Server name", required=True)
    ftp_host = fields.Char("Host", required=True)
    ftp_username = fields.Char("User Name", required=True)
    ftp_password = fields.Char("Password")
    ftp_port = fields.Char("Port", required=True)
    is_passive_mode = fields.Boolean("Passive Mode", default=True)
    directory_ids = fields.One2many("ftp.directory.ept", 'ftp_server_id', string="Directory list")
    conn_type = fields.Selection([('ftp', 'FTP'), ('sftp', 'SFTP')], string="Connection Type",
                                 default='sftp', )
    server_type = fields.Selection([('production', 'Production'), ('sandbox', 'Sandbox')],
                                   string="Server Connection Type", default='sandbox')
    key_filename = fields.Char("SSH Key path")
    is_production_environment = fields.Boolean()
    is_sftp_passphrase_password = fields.Boolean()

    _sql_constraints = [
        ('ftp_unique_ept', 'UNIQUE (name,ftp_host,ftp_username,ftp_password,ftp_port)',
         'The Server must be unique!'), ]

    def toggle_prod_environment_value(self):
        """
        This will switch environment between production and pre-production.
        @return : True
        @author: Keyur Kanani
        """
        self.ensure_one()
        self.is_production_environment = not self.is_production_environment
        if self.is_production_environment:
            self.server_type = 'production'
        else:
            self.server_type = 'sandbox'

    @api.onchange('conn_type')
    def onchange_conn_type(self):
        if self.conn_type == 'ftp':
            self.ftp_port = 21
        if self.conn_type == 'sftp':
            self.ftp_port = 22

    def do_test(self):
        """
        author: bhavesh jadav 27/4/2019
        func: this method use for test connection only of FTP and SFTP
        :return:
        """
        conn_type = self.conn_type
        ftp_host = self.ftp_host
        ftp_port = int(self.ftp_port)
        ftp_username = self.ftp_username
        ftp_password = self.ftp_password
        key_filename = self.key_filename
        if conn_type == "ftp":
            try:
                with TPWFTPInterface(host=ftp_host, user=ftp_username, passwd=ftp_password,
                                     port=ftp_port, from_tpw_dir=False, to_tpw_dir=False):
                    title = _("FTP Connection Test Succeeded!")
                    message = _("Everything seems properly set up!")
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': title,
                            'message': message,
                            'sticky': False,
                        }
                    }
            except Exception as e:
                raise UserError(_("Connection Test Failed! Here is what we got instead:\n %s") % (e))
        elif conn_type == "sftp":
            try:
                with sftp_interface(host=ftp_host, user=ftp_username, passwd=ftp_password, key_filename=key_filename,
                                    port=ftp_port, upload_dir=False):
                    title = _("SFTP Connection Test Succeeded!")
                    message = _("Everything seems properly set up!")
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': title,
                            'message': message,
                            'sticky': False,
                        }
                    }
            except Exception as e:
                raise UserError(_("Connection Test Failed! Here is what we got instead:\n %s") % (e))
        else:
            raise Warning("Please set proper connection type.")

    def do_test_connection(self):
        """
        author: bhavesh jadav 15/4/2019
        func: this method use for test connection of FTP and SFTP
        :return:NULL
        """
        global sending, receive, archive
        conn_type = self.conn_type
        ftp_host = self.ftp_host
        ftp_port = int(self.ftp_port)
        ftp_username = self.ftp_username
        ftp_password = self.ftp_password
        key_filename = self.key_filename
        if conn_type == "ftp":
            try:
                if not self.directory_ids:
                    raise Warning("Please add FTP directories")
                for directory in self.directory_ids:
                    sending = TPWFTPInterface(
                        host=ftp_host,
                        user=ftp_username,
                        passwd=ftp_password,
                        from_tpw_dir=directory.path,
                        to_tpw_dir=directory.path,
                        port=ftp_port
                    )

                    receive = TPWFTPInterface(
                        host=ftp_host,
                        user=ftp_username,
                        passwd=ftp_password,
                        to_tpw_dir=directory.path,
                        from_tpw_dir=directory.path,
                        port=ftp_port
                    )

                    archive = TPWFTPInterface(
                        host=ftp_host,
                        user=ftp_username,
                        passwd=ftp_password,
                        archive_dir=directory.path,
                        to_tpw_dir=directory.path,
                        from_tpw_dir=directory.path,
                        port=ftp_port
                    )

                if sending or receive or archive:
                    raise Warning("Working properly")
                else:
                    raise Warning("Not working")
            except Exception as e:
                raise Warning("%s" % e)
        elif conn_type == "sftp":
            try:
                if not self.directory_ids:
                    raise Warning("Please add FTP directories")
                for directory in self.directory_ids:
                    sending = sftp_interface(
                        host=ftp_host,
                        user=ftp_username,
                        passwd=ftp_password,
                        key_filename=key_filename,
                        port=int(ftp_port),
                        upload_dir=str(directory.path)
                    )
                    receive = sftp_interface(
                        host=ftp_host,
                        user=ftp_username,
                        passwd=ftp_password,
                        key_filename=key_filename,
                        port=ftp_port,
                        download_dir=str(directory.path)
                    )
                    archive = sftp_interface(
                        host=ftp_host,
                        user=ftp_username,
                        passwd=ftp_password,
                        key_filename=key_filename,
                        port=ftp_port,
                        archive_dir=str(directory.path)
                    )
                if sending or receive or archive:
                    raise Warning("Working properly")
                else:
                    raise Warning("Oops.. Not working")
            except Exception as e:
                raise Warning("%s" % e)

    def add_directory(self):
        """
        This method set all directory list in FTP instance.
        :return: Set directory list in FTP instance
        """
        if self.do_test():
            directory_list = []
            if self.conn_type == 'ftp':
                ftp = ftplib.FTP(self.ftp_host, self.ftp_username, self.ftp_password)
                directory_list = self._get_ftp_directory_list(ftp, directory_list)
                if directory_list:
                    self.env['ftp.directory.ept'].create(directory_list)
            elif self.conn_type == 'sftp':
                with sftp_interface(host=self.ftp_host, user=self.ftp_username, passwd=self.ftp_password,
                                    key_filename=self.key_filename,
                                    port=self.ftp_port, upload_dir=False) as ssh:
                    directory_list = self._get_sftp_directory_list(ssh.sftp_client, directory_list)
                    if directory_list:
                        self.env['ftp.directory.ept'].create(directory_list)
        return True

    def _get_sftp_directory_list(self, sftp_client, directory_list, **kwargs):
        """
            Usage: This method is prepare the find all the directories with
            nested directory and return it.
            :param sftp_client: Paramiko SFTP Client Object
            :param directory_list: It contain Directory Information, Type: List
            :param kwargs: Keyword Arguments, Type: Dict
            @Author: Dipak Gogiya
            @Task: 175413 - FTP connector: Get child directories
            :return: directory_list -> List.
        """
        root_path = kwargs.get('root_path', '') or ''
        for dir in sftp_client.listdir(root_path):
            if dir.__contains__('.'):
                continue
            try:
                # normalize_path = sftp_client.normalize(dir) if not kwargs.get('normalize_path', '') else kwargs.get('normalize_path', '') + '/' + dir
                normalize_path = root_path + '/' + dir if not root_path.endswith('/') else root_path + dir
                lstatout = str(sftp_client.lstat(normalize_path)).split()[0]
            except Exception as exception:
                _logger.info(f"Exception Occur While preparing the Directory List, Exception: {exception}")
                continue
            if 'd' in lstatout:
                directory_list.append({
                    'ftp_server_id': self.id,
                    'name': normalize_path,
                    'path': normalize_path
                })
                self._get_sftp_directory_list(sftp_client, directory_list, root_path=normalize_path)

        return directory_list

    def _get_ftp_directory_list(self, ftp, directory_list, **kwargs):
        """

        :param FTP: FTP Client Object
        :param directory_list: It contain Directory Information, Type: List
        :param kwargs: Keyword Arguments, Type: Dict
        @Author: Dipak Gogiya
        @Task: 175413 - FTP connector: Get child directories
        :return: directory_list -> List
        """
        root_path = kwargs.get('root_path') or ''
        for dir in ftp.nlst(root_path):
            if not dir.__contains__('.'):
                directory_list.append({
                    'ftp_server_id': self.id,
                    'name': dir,
                    'path': "/" + dir
                })
                self._get_ftp_directory_list(ftp, directory_list, root_path=dir)

        return directory_list


class FtpDirectoryEpt(models.Model):
    _name = "ftp.directory.ept"
    _description = "Ftp Directories Ddetails"

    ftp_server_id = fields.Many2one("ftp.server.ept", string="Ftp Server")
    name = fields.Char("Name", required=True)
    path = fields.Char("Path", required=True)

    _sql_constraints = [('directory_unique', 'UNIQUE (name,ftp_server_id)', 'The Directory must be unique!'), ]
