""" Inherit the existing functionality of attachment and add its new functionality """
import base64
import logging
from datetime import datetime
from odoo import models

_logger = logging.getLogger("Amazon Vendor Central Ept")


class IRAttachment(models.Model):
    """
        Inherit the existing functionality of attachment and add its new functionality
    """
    _inherit = "ir.attachment"

    def create_file_attachment(self, segment_data, filename, res_model=''):
        """
            Used for create the attachment
            :param segment_data: Segment Data
            :param filename: filename
            :param res_model: Resource Model, Type: String
            :@author: Dipak Gogiya, 02/12/2020
            :return: ir_attachment()
        """
        result = base64.b64encode(segment_data.encode())
        attachment = self.create({
            'name': filename,
            'datas': result,
            'res_model': res_model,
            'type': 'binary'
        })
        return attachment

    def create_attachment_and_upload_file_to_ftp(self, acknowledgment_data, ftp_server_id, instance,
                                                 file_prefix, directory_id, common_log_book=False,
                                                 raise_warning=False):
        """
            Usage: Used for create the attachment and uploading the file to the FTP
            and return the new attachment
            :param acknowledgment_data: Acknowledgment Data
            :param ftp_server_id: ftp.server.ept()
            :param instance: amazon.vendor.instance()
            :return: attachment
        """
        upload_file_name = '%s_%s_%s_%s_%s_%s_%s_%s.%s' % (
            file_prefix, instance.supplier_id,
            datetime.now().day, datetime.now().month,
            datetime.now().year, datetime.now().hour,
            datetime.now().minute, datetime.now().second, instance.avc_vendor_code)
        _logger.info("Uploaded File Name : {}".format(upload_file_name))

        res_model = 'amazon.sale.requisition.ept'
        # Attachment Create Process
        attachment = self.create_file_attachment(acknowledgment_data, upload_file_name,
                                                 res_model=res_model)

        _logger.info(
            "File Name which is uploading to the amazon vendor central, File Name : {}".format(upload_file_name))
        # Upload the file to the FTP
        status = instance.upload_file_to_ftp(acknowledgment_data, ftp_server_id, directory_id, upload_file_name,
                                              common_log_book, raise_warning=raise_warning)

        return attachment, status
