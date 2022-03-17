""" This file manage the operations of import products, import amazon purchase orders, etc."""
import base64
import csv
import os
import logging
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import Warning

_logger = logging.getLogger("Amazon Vendor Central")


class AmazonVendorImportExport(models.TransientModel):
    """
    This model is used for import and export functionality.
    """
    _name = 'amazon.vendor.import.export.ept'
    _description = "Amazon Vendor Import Export EPT"

    def _get_current_company_instances(self):
        """
            Usage: Return the domain which will display the current company instances
            :return: Domain
        """
        return [('company_id', '=', self.env.company.id)]

    vendor_operations = fields.Selection([('import_products', 'Import Products'),
                                          ('import_purchase_order', 'Import Purchase Orders'),
                                          ('export_inventory_and_stock_report', 'Export Inventory and Cost Report')],
                                         string="Operations")
    instance_id = fields.Many2one('amazon.vendor.instance', string="Amazon Vendor",
                                  help='Amazon vendor central instance',
                                  domain=_get_current_company_instances)
    file = fields.Binary(string='Choose File', help='Import Product CSV File')
    file_name = fields.Char(string='Import File Name', help='Import File Name')
    delimiter = fields.Selection([('tab', 'Tab'), ('semicolon', 'Semicolon'), ('comma', 'Comma')],
                                 string="Separator", default='comma', required=True)

    @api.onchange('vendor_operations')
    def onchange_instance_id(self):
        company = self.env.company or self.env.user.company_id.id
        instances = self.env['amazon.vendor.instance'].search([('company_id', '=', company.id or False)])
        if instances and len(instances) == 1:
            self.instance_id = instances.id

    def execute(self):
        """
            import order from the directory
            :return: the action of product
        """
        if self.vendor_operations == 'import_products':
            self.import_csv_file()
        elif self.vendor_operations == 'import_purchase_order':
            self.env['amazon.sale.requisition.ept'].import_order_from_amazon(self.instance_id)
            return self.env['ir.actions.act_window']._for_xml_id(
                'amazon_vendor_central_ept.amazon_sale_requisition_view_action')
        elif self.vendor_operations == 'export_inventory_and_stock_report':
            self.instance_id.export_inventory_and_stock_report()
            return self.env['ir.actions.act_window']._for_xml_id(
                'amazon_vendor_central_ept.amazon_vendor_central_product_ept_view_action')
        return True

    def import_csv_file(self):
        """
            This method decode csv file data into dictionary format and call
            functions for create log.
            :return: action
            Added By: Keyur Kanani
        """
        _logger.info("Import Product Process Started...")
        if self.file and self.instance_id:
            if self._get_file_type(self.file_name):

                csv_file = StringIO(base64.b64decode(self.file).decode())
                file_write = open('/tmp/products.csv', 'w+')
                file_write.writelines(csv_file.getvalue())
                file_write.close()

                if self.delimiter == "tab":
                    reader = csv.DictReader(open('/tmp/products.csv', "rU"), delimiter="\t")
                elif self.delimiter == "semicolon":
                    reader = csv.DictReader(open('/tmp/products.csv', "rU"), delimiter=";")
                else:
                    reader = csv.DictReader(open('/tmp/products.csv', "rU"), delimiter=",")

                if reader and reader.fieldnames and len(reader.fieldnames) == 4:
                    self.process_csv_file(reader)
                else:
                    raise Warning(_(
                        "Either file is invalid or proper delimiter/separator is not specified "
                        "or not found required fields."))
            else:
                raise Warning(_(
                    "Either file format is not csv or proper delimiter/separator is not specified"))

        _logger.info("Import Product Process Ended...")
        return self.env['ir.actions.act_window']._for_xml_id(
            'amazon_vendor_central_ept.amazon_vendor_central_product_ept_view_action')

    def process_csv_file(self, reader):
        """
            Usage: Used for, process the csv file and create the amazon product and mapping with
            odoo product or update the existing amazon product.
            :param reader: csv reader object, which contain all the csv file data.
            :return: True
        """
        common_log_lines_obj = self.env['common.log.lines.ept']
        product_obj = self.env['product.product']
        avc_product_obj = self.env['amazon.vendor.central.product.ept']
        # pricelist_id = self.instance_id.pricelist_id

        # Create the Common Log Book.
        message = 'Import Amazon Vendor Product for vendor %s and filename is %s' % (
            self.instance_id.name, self.file_name)
        log = self.env['common.log.book.ept'].create_avc_common_log \
            ('amazon.vendor.central.product.ept', 'import', message)

        for line in reader:
            default_code = line.get('default_code', '')
            amazon_sku = line.get('amazon_sku', '')
            barcode = line.get('barcode', '')
            item_type = line.get('item_type', '')
            if not item_type or item_type not in ['EN', 'UP', 'SRV', 'BP', 'SA', 'IB']:
                product_code = default_code or amazon_sku or barcode or ''
                message = "Skip Create Product because, Either product type is not set or " \
                          "define product type is wrong, Product Code: [{}]".format(product_code)
                common_log_lines_obj.create_avc_log_lines(message, log, default_code=product_code)
                continue
            ## set default price 1
            # price = line.get('price', 0.0) or 1.0
            # if float(price) <= 0:
            #     raise Warning(_("Must have to set the price greater then 0."))

            odoo_product = product_obj.search_avc_odoo_product(default_code, barcode)
            if not odoo_product:
                message = 'Odoo Product not found %s' % (default_code if default_code else barcode)
                _logger.info(message)
                common_log_lines_obj.create_avc_log_lines(message, log, default_code=default_code)
            else:
                amazon_product = avc_product_obj.search_avc_amazon_product(amazon_sku,
                                                                           self.instance_id,
                                                                           item_type)
                if not amazon_product:
                    vals = {'amazon_vendor_instance_id': self.instance_id.id,
                            'product_id': odoo_product.id,
                            'amazon_sku': amazon_sku,
                            'barcode': barcode,
                            'product_type': item_type,
                            }
                    avc_product_obj.create(vals)
                else:
                    amazon_product.write({'product_id': odoo_product.id})

                # if pricelist_id:
                #     pricelist_id.set_product_price_ept(odoo_product.id, float(price))
                message = 'Amazon Vendor Product is Created with amazon SKU %s' % (amazon_sku)
                _logger.info(message)

        if not log.log_lines:
            log.unlink()

        return True

    def download_sample_attachment(self):
        """
            Download the Sample Attachment.
            :return: dictionary
            Added By: Mansi Ramani
        """
        attachment = self.env['ir.attachment'].search([('name', '=', 'import_product_sample.csv'), ('res_model', '=', 'amazon.vendor.import.export.ept')], limit=1)
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'new',
            'nodestroy': False,
        }

    @staticmethod
    def _get_file_type(file_name):
        """
            This method is used to find file type using os library if file type is not .csv
            then return False
            :param file_name:file name
            :return:Boolean
            Added By: Mansi Ramani
        """
        file_type = os.path.splitext(file_name)
        if len(file_type) == 2 and file_type[1] == '.csv':
            return True
        return False
