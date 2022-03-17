""" This file is inherit the existing functionality of common log lines and
added its new functionality """
from odoo import models


class CommonLogLinesEpt(models.Model):
    """
        Inherit the existing functionality and added its new functionality
    """
    _inherit = "common.log.lines.ept"
    _rec_name = "message"

    def create_avc_log_lines(self, message, common_log_book, default_code='', odoo_product=False, **kwargs):
        """
            Usage:  This method is used for create the common log lines based on method parameters
            and attach with common log book.
            :param message:
            :param common_log_book: common.log.book.ept()
            :param default_code: product default code (Internal Reference), Type: Char
            :param odoo_product: product.product() or False.
            Added By: Dipak Gogiya
            :return:
        """
        log_val = {
            'default_code': default_code,
            'message': message,
            'log_book_id': common_log_book.id if common_log_book else False,
            'product_id': odoo_product,
            'order_ref': kwargs.get('order_ref', False)
        }
        self.create(log_val)
        return True
