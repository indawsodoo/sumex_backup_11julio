# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import pymssql
import odoorpc
import logging

global unique_move_line_list
unique_move_line_list = []


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    statusfacturado = fields.Char('StatusFacturado')
    ejercicioalbaran = fields.Char('EjercicioAlbaran')
    seriealbaran = fields.Char('SerieAlbaran')

    def account_move_cron_job_custom_indaws_livess(self):

        server = '10.210.86.100'
        database = 'sage'
        username = 'consultasit'
        password = 'Ulises-2007'
        conn = pymssql.connect(server=server, user=username,
                               password=password, database=database)

        new_v_14_db = odoorpc.ODOO('38.242.209.30', port=8069)
        new_v_14_db.login('14_sumex', 'hola@indaws.com', 'holaindaws123!!!')

        cursor = conn.cursor()
        columns = ['partner_id', 'invoice_date', 'invoice_payment_term_id', 'ref', 'name', 'StatusFacturado',
                   'EjercicioAlbaran', 'SerieAlbaran']
        result = []
        ir_config_parameter_fetch = new_v_14_db.env['ir.config_parameter'].get_param('Fetch_value')
        for i in range(0, 60000, 1000):
            # print('i',i)
            cursor.execute(
                f'select CodigoCliente,FechaAlbaran,FormadePago,Numerofactura,NumeroAlbaran,StatusFacturado,EjercicioAlbaran ,SerieAlbaran from CabeceraAlbaranCliente where EjercicioAlbaran >= 2017 order by CodigoCliente offset {i} rows FETCH NEXT {ir_config_parameter_fetch} ROWS ONLY;')

            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))

            res_partner_obj = new_v_14_db.env['res.partner']
            res_partner_payment_terms = new_v_14_db.env['account.payment.term']
            account_move_obj = new_v_14_db.env['account.move']
        for j in result:
            try:
                product_pay_terms = res_partner_payment_terms.search([('name', '=', j['invoice_payment_term_id'])])
                partner_search = res_partner_obj.search([('ref', '=', j['partner_id'])])
                account_move_new = account_move_obj.create({
                    'partner_id': partner_search[0] if j['partner_id'] else False,
                    'invoice_date': str(j['invoice_date']),
                    'invoice_payment_term_id': product_pay_terms[0] if j['invoice_payment_term_id'] else False,
                    'ref': j['ref'],
                    'journal_id': 1,
                    'currency_id': 1,
                    'state': 'draft',
                    'move_type': 'out_invoice',
                    'statusfacturado': j['StatusFacturado'],
                    'name': j['name'],
                    'ejercicioalbaran': j['EjercicioAlbaran'],
                    'seriealbaran': j['SerieAlbaran']
                })
            except Exception as e:
                print(e)

    def account_move_cron_job_custom_indaws_stagess(self):

        server = '10.210.86.100'
        database = 'sage'
        username = 'consultasit'
        password = 'Ulises-2007'
        conn = pymssql.connect(server=server, user=username,
                               password=password, database=database)

        new_v_14_db = odoorpc.ODOO('38.242.209.30', port=8069)
        new_v_14_db.login('14_sumex_news', 'hola@indaws.com', 'holaindaws123!!!')

        cursor = conn.cursor()
        columns = ['partner_id', 'invoice_date', 'invoice_payment_term_id', 'ref', 'name', 'StatusFacturado',
                   'EjercicioAlbaran', 'SerieAlbaran']
        result = []
        ir_config_parameter_fetch = new_v_14_db.env['ir.config_parameter'].get_param('Fetch_value')
        for i in range(0, 60000, 1000):
            # print('i',i)
            cursor.execute(
                f'select CodigoCliente,FechaAlbaran,FormadePago,Numerofactura,NumeroAlbaran,StatusFacturado,EjercicioAlbaran ,SerieAlbaran from CabeceraAlbaranCliente where EjercicioAlbaran >= 2017 order by CodigoCliente offset {i} rows FETCH NEXT {ir_config_parameter_fetch} ROWS ONLY;')

            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))

            res_partner_obj = new_v_14_db.env['res.partner']
            res_partner_payment_terms = new_v_14_db.env['account.payment.term']
            account_move_obj = new_v_14_db.env['account.move']
        for j in result:
            try:
                product_pay_terms = res_partner_payment_terms.search([('name', '=', j['invoice_payment_term_id'])])
                partner_search = res_partner_obj.search([('ref', '=', j['partner_id'])])
                account_move_new = account_move_obj.create({
                    'partner_id': partner_search[0] if j['partner_id'] else False,
                    'invoice_date': str(j['invoice_date']),
                    'invoice_payment_term_id': product_pay_terms[0] if j['invoice_payment_term_id'] else False,
                    'ref': j['ref'],
                    'journal_id': 1,
                    'currency_id': 1,
                    'state': 'draft',
                    'move_type': 'out_invoice',
                    'statusfacturado': j['StatusFacturado'],
                    'name': j['name'],
                    'ejercicioalbaran': j['EjercicioAlbaran'],
                    'seriealbaran': j['SerieAlbaran']
                })
            except Exception as e:
                print(e)


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    quantity_2 = fields.Float(string='quantity 2')

    def account_move_line_cron_job_custom(self):
        server = '10.210.86.100'
        database = 'sage'
        username = 'consultasit'
        password = 'Ulises-2007'
        conn = pymssql.connect(server=server, user=username,
                               password=password, database=database)

        new_v_14_db = odoorpc.ODOO('38.242.209.30', port=8069)
        new_v_14_db.login('14_sumex', 'hola@indaws.com', 'holaindaws123!!!')

        cursor = conn.cursor()
        columns = ['move_id', 'name', 'product_id', 'quantity', 'quantity2', 'price_unit', 'tax_ids', 'tax_ids_2',
                   'discount',
                   'discount2', 'discount3', 'EjercicioAlbaran', 'SerieAlbaran']
        result = []
        ir_config_parameter_fetch = new_v_14_db.env['ir.config_parameter'].get_param('Fetch_value')

        for i in range(0, 700000, 1000):
            cursor.execute(
                f'select  NumeroAlbaran,DescripcionArticulo,CodigoArticulo,Unidades,UnidadesServidas,Precio,[%Iva],[%Recargo],[%Descuento],[%Descuento2],[%Descuento3],EjercicioAlbaran ,SerieAlbaran from LineasAlbaranCliente where EjercicioAlbaran >= 2017  order by NumeroAlbaran offset {i} rows FETCH NEXT {ir_config_parameter_fetch} ROWS ONLY;')

            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))
            res_partner_obj = new_v_14_db.env['res.partner']
            res_partner_payment_terms = new_v_14_db.env['account.payment.term']
            account_move_obj = new_v_14_db.env['account.move']
            account_move_line_obj = new_v_14_db.env['account.move.line']
            product_product_obj = new_v_14_db.env['product.product']
            account_tax_new = new_v_14_db.env['account.tax']
            account_account_new = new_v_14_db.env['account.account']
        for j in result:
            try:
                product_id_search = product_product_obj.search([('default_code', '=', j['product_id'])])
                account_move_id = account_move_obj.search(
                    [('name', '=', j['move_id']), ('ejercicioalbaran', '=', j['EjercicioAlbaran']),
                     ('seriealbaran', '=', j['SerieAlbaran'])])
                print('account move id ==', account_move_id)
                account_id = account_account_new.search([('code', '=', '700000')])
                global account_tax_1
                partner_search = account_move_obj.search([('name', '=', j['move_id'])])
                if j['tax_ids'] == 21:
                    account_tax_1 = account_tax_new.search([('name', '=', 'IVA 21% (Bienes)')])
                elif (j['tax_ids'] == 0):
                    account_tax_1 = account_tax_new.search(
                        [('name', '=', 'IVA 0% Prestación de servicios intracomunitario')])
                elif (j['tax_ids_2'] == 5.2):
                    account_tax_1 = account_tax_new.search(
                        [('name', '=', '5.2% Recargo Equivalencia Ventas')])
                global n, p, q
                if str(j['discount'].to_eng_string())[0] == '0':
                    n = 0
                else:
                    n = float(j['discount'].to_eng_string())

                if str(j['discount2'].to_eng_string())[0] == '0':
                    p = 0
                else:
                    p = float(j['discount2'].to_eng_string())

                if str(j['discount3'].to_eng_string())[0] == '0':
                    q = 0
                else:
                    q = float(j['discount3'].to_eng_string())

                vals = {
                    'move_id': account_move_id[0] if j['move_id'] else False,
                    'name': j['name'],
                    'product_id': product_id_search[0] if j['product_id'] else False,
                    'quantity': float(j['quantity'].to_eng_string()),
                    'quantity_2': float(j['quantity2'].to_eng_string()),
                    'price_unit': float(j['price_unit'].to_eng_string()),
                    'tax_ids': [(6, 0, [account_tax_1[0]])],
                    'exclude_from_invoice_tab': 0,
                    'account_id': account_id[0],
                    'discount': n,
                    'discount2': p,
                    'discount3': q,

                }
                browse_rec = account_move_obj.browse(account_move_id[0])
                account_move_new = browse_rec.invoice_line_ids = [(0, 0, vals)]
            except Exception as e:
                print(e)

    def account_move_line_cron_job_custom_stag_live(self):


        server = '10.210.86.100'
        database = 'sage'
        username = 'consultasit'
        password = 'Ulises-2007'
        conn = pymssql.connect(server=server, user=username,
                               password=password, database=database)

        new_v_14_db = odoorpc.ODOO('38.242.209.30', port=8069)
        new_v_14_db.login('14_sumex', 'hola@indaws.com', 'holaindaws123!!!')

        cursor = conn.cursor()
        columns = ['move_id', 'name', 'product_id', 'quantity', 'quantity2', 'price_unit', 'tax_ids', 'tax_ids_2',
                   'discount',
                   'discount2', 'discount3', 'EjercicioAlbaran', 'SerieAlbaran', 'unique_field', ]
        result = []
        ir_config_parameter_fetch = new_v_14_db.env['ir.config_parameter'].get_param('Fetch_value')
        for i in range(0, 600000, 1000):
            logging.info('unique_move_line_list-----------%s', unique_move_line_list)
            if unique_move_line_list:
                unique_move_line_list_1=tuple(unique_move_line_list)
                cursor.execute(
                    f'select  NumeroAlbaran,DescripcionArticulo,CodigoArticulo,Unidades,UnidadesServidas,Precio,[%Iva],[%Recargo],[%Descuento],[%Descuento2],[%Descuento3],EjercicioAlbaran ,SerieAlbaran ,lineasPosicion  from LineasAlbaranCliente where EjercicioAlbaran >= 2017 and lineasPosicion not in {unique_move_line_list_1} order by NumeroAlbaran offset {i} rows FETCH NEXT {ir_config_parameter_fetch} ROWS ONLY;')
            else:
                print('>>> false')
                cursor.execute(
                    f'select  NumeroAlbaran,DescripcionArticulo,CodigoArticulo,Unidades,UnidadesServidas,Precio,[%Iva],[%Recargo],[%Descuento],[%Descuento2],[%Descuento3],EjercicioAlbaran ,SerieAlbaran ,lineasPosicion  from LineasAlbaranCliente where EjercicioAlbaran >= 2017  order by NumeroAlbaran offset {i} rows FETCH NEXT {ir_config_parameter_fetch} ROWS ONLY;')
            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))

            res_partner_obj = new_v_14_db.env['res.partner']
            res_partner_payment_terms = new_v_14_db.env['account.payment.term']
            account_move_obj = new_v_14_db.env['account.move']
            account_move_line_obj = new_v_14_db.env['account.move.line']
            product_product_obj = new_v_14_db.env['product.product']
            account_tax_new = new_v_14_db.env['account.tax']
            account_account_new = new_v_14_db.env['account.account']
        for j in result:
            try:
                product_id_search = product_product_obj.search([('default_code', '=', j['product_id'])])
                account_move_id = account_move_obj.search(
                    [('name', '=', j['move_id']), ('ejercicioalbaran', '=', j['EjercicioAlbaran']),
                     ('seriealbaran', '=', j['SerieAlbaran'])])
                print('account move id ==', account_move_id)
                account_id = account_account_new.search([('code', '=', '700000')])
                global account_tax_1
                partner_search = account_move_obj.search([('name', '=', j['move_id'])])
                if j['tax_ids'] == 21:
                    account_tax_1 = account_tax_new.search([('name', '=', 'IVA 21% (Bienes)')])
                elif (j['tax_ids'] == 0):
                    account_tax_1 = account_tax_new.search(
                        [('name', '=', 'IVA 0% Prestación de servicios intracomunitario')])
                elif (j['tax_ids_2'] == 5.2):
                    account_tax_1 = account_tax_new.search(
                        [('name', '=', '5.2% Recargo Equivalencia Ventas')])
                global n, p, q
                if str(j['discount'].to_eng_string())[0] == '0':
                    n = 0
                else:
                    n = float(j['discount'].to_eng_string())

                if str(j['discount2'].to_eng_string())[0] == '0':
                    p = 0
                else:
                    p = float(j['discount2'].to_eng_string())

                if str(j['discount3'].to_eng_string())[0] == '0':
                    q = 0
                else:
                    q = float(j['discount3'].to_eng_string())
                vals = {
                    'move_id': account_move_id[0] if j['move_id'] else False,
                    'name': j['name'],
                    'product_id': product_id_search[0] if j['product_id'] else False,
                    'quantity': float(j['quantity'].to_eng_string()),
                    'quantity_2': float(j['quantity2'].to_eng_string()),
                    'price_unit': float(j['price_unit'].to_eng_string()),
                    'tax_ids': [(6, 0, [account_tax_1[0]])],
                    'exclude_from_invoice_tab': 0,
                    'account_id': account_id[0],
                    'discount': n,
                    'discount2': p,
                    'discount3': q,

                }
                logging.info('>>>>> vals %s', vals)
                unique_move_line_list.append(str(j['unique_field']))
                logging.info('>>>>> unique_move_line_list neww %s', unique_move_line_list)
                browse_rec = account_move_obj.browse(account_move_id[0])
                account_move_new = browse_rec.invoice_line_ids = [(0, 0, vals)]
            except Exception as e:
                logging.info('%s', e)
