# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import pymssql
import odoorpc
import logging
import json


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    statusfacturado = fields.Char('StatusFacturado')
    ejercicioalbaran = fields.Char('EjercicioAlbaran')
    seriealbaran = fields.Char('SerieAlbaran')
    uid_number = fields.Char('UID')

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

        cursor = conn.cursor()
        columns = ['partner_id', 'invoice_date', 'invoice_payment_term_id', 'ref', 'name', 'StatusFacturado',
                   'EjercicioAlbaran', 'SerieAlbaran']
        result = []
        ir_config_parameter_fetch = self.env['ir.config_parameter'].get_param('Fetch_value')
        # cursor.execute(
        #     f'select count(*) from CabeceraAlbaranCliente where EjercicioAlbaran >= 2017;')
        # print('cursor()----', cursor)
        # for row in cursor.fetchall():
        #     print('row----------', row)
        res_partner_obj = self.env['res.partner']
        res_partner_payment_terms = self.env['account.payment.term']
        account_move_obj = self.env['account.move']
        for i in range(0, 60000, 1000):
            # print('i',i)

            cursor.execute(
                f'select CodigoCliente,FechaAlbaran,FormadePago,Numerofactura,NumeroAlbaran,StatusFacturado,EjercicioAlbaran ,SerieAlbaran from CabeceraAlbaranCliente where EjercicioAlbaran >= 2017 order by CodigoCliente offset {i} rows FETCH NEXT {ir_config_parameter_fetch} ROWS ONLY;')
            vals_list = []
            for row in cursor.fetchall():
                j = dict(zip(columns, row))
                product_pay_terms = res_partner_payment_terms.search([('name', '=', j['invoice_payment_term_id'])])
                partner_search = res_partner_obj.search([('ref', '=', j['partner_id'])])
                account_move_new = {
                    'partner_id': partner_search[0].id if j['partner_id'] else False,
                    'invoice_date': str(j['invoice_date']),
                    'invoice_payment_term_id': product_pay_terms[0].id if j['invoice_payment_term_id'] else False,
                    'ref': j['ref'],
                    'journal_id': 1,
                    'currency_id': 1,
                    'state': 'draft',
                    'move_type': 'out_invoice',
                    'statusfacturado': j['StatusFacturado'],
                    'name': j['name'],
                    'ejercicioalbaran': j['EjercicioAlbaran'],
                    'seriealbaran': j['SerieAlbaran']
                }
                vals_list.append(account_move_new)
            try:
                account_move_obj.create(vals_list)
            except Exception as e:
                print('Excepetion========', e)


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    quantity_2 = fields.Float(string='quantity 2')
    uid_number = fields.Char('UID')

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

    def account_move_line_cron_job_custom_stag_live_testing_sumex_1(self):
        server = '10.210.86.100'
        database = 'sage'
        username = 'consultasit'
        password = 'Ulises-2007'
        conn = pymssql.connect(server=server, user=username,
                               password=password, database=database)

        cursor = conn.cursor()
        columns = ['move_id', 'name', 'product_id', 'quantity', 'quantity2', 'price_unit', 'tax_ids', 'tax_ids_2',
                   'discount',
                   'discount2', 'discount3', 'EjercicioAlbaran', 'SerieAlbaran', 'unique_field', ]
        result = []
        res_partner_obj = self.env['res.partner']
        res_partner_payment_terms = self.env['account.payment.term']
        account_move_obj = self.env['account.move']
        account_move_line_obj = self.env['account.move.line']
        product_product_obj = self.env['product.product']
        account_tax_new = self.env['account.tax']
        account_account_new = self.env['account.account']
        ir_config_parameter_fetch = self.env['ir.config_parameter'].get_param('Fetch_value')
        account_tax_21 = account_tax_new.search([('name', '=', 'IVA 21% (Bienes)')])
        account_tax_0 = account_tax_new.search(
            [('name', '=', 'IVA 0% Prestación de servicios intracomunitario')])
        account_tax_5_2 = account_tax_new.search(
            [('name', '=', '5.2% Recargo Equivalencia Ventas')])
        account_id = account_account_new.search([('code', '=', '700000')])
        company_id = self.env['res.company'].browse(1)
        min_counter = int(company_id.move_line_count)
        not_found_account_move_ids = ''
        not_found_move_year = []
        for i in range(0, 600000, 1000):
            vals_list = []
            counter = 0
            for index, row in enumerate(cursor.fetchall()):
                j = dict(zip(columns, row))
                product_id_search = product_product_obj.search([('default_code', '=', j['product_id'])])
                account_move_id = account_move_obj.search(
                    [('name', '=', str(j['move_id'])), ('ejercicioalbaran', '=', j['EjercicioAlbaran'])], limit=1)
                global account_tax_1
                # partner_search = account_move_obj.search([('name', '=', j['move_id'])])
                if j['tax_ids'] == 21:
                    account_tax_1 = account_tax_21
                elif (j['tax_ids'] == 0):
                    account_tax_1 = account_tax_0
                elif (j['tax_ids_2'] == 5.2):
                    account_tax_1 = account_tax_5_2
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
                if account_move_id:
                    vals = {
                        'move_id': account_move_id.id if j['move_id'] else False,
                        'name': str(j['name']),
                        'product_id': product_id_search[0].id if j['product_id'] and product_id_search else False,
                        'quantity': float(j['quantity'].to_eng_string()),
                        'quantity_2': float(j['quantity2'].to_eng_string()),
                        'price_unit': float(j['price_unit'].to_eng_string()),
                        'tax_ids': [(6, 0, [account_tax_1[0].id])] if account_tax_1 else False,
                        'exclude_from_invoice_tab': 0,
                        'account_id': account_id[0].id if account_id else False,
                        'discount': n,
                        'discount2': p,
                        'discount3': q,
                    }
                    vals_list.append(vals)
                    counter = index + 1
                else:
                    if not list(filter(lambda x: x[0] == j['move_id'] and x[1] == j['EjercicioAlbaran'], not_found_move_year)):
                        not_found_move_year.append((j['move_id'], j['EjercicioAlbaran']))
                        not_found_account_move_ids += f'\n{str(j)}\n'
            company_id.move_line_count += counter
            try:
                move_lines = account_move_line_obj.create(vals_list)
                self._cr.commit()
                logging.info("<<<<<<<<<<<move_lines %s", len(move_lines))
            except Exception as e:
                logging.info('%s', e)
            with open('/tmp/not_found_moves.txt', 'a') as file:
                file.write(not_found_account_move_ids)
                file.close()

    def search_move(self, move_tuple):
        self._cr.execute(f"""
            SELECT id from account_move where name='{str(move_tuple[0])}' and ejercicioalbaran='{str(move_tuple[1])}';
        """)
        return False if self._cr.fetchall() else True

    def fetch_missing_account_moves(self):
        server = '10.210.86.100'
        database = 'sage'
        username = 'consultasit'
        password = 'Ulises-2007'
        conn = pymssql.connect(server=server, user=username,
                               password=password, database=database)

        cursor = conn.cursor()
        move_columns = ['uid_number','partner_id', 'invoice_date', 'invoice_payment_term_id', 'ref', 'name', 'StatusFacturado',
                   'EjercicioAlbaran', 'SerieAlbaran']
        move_line_columns = ['uid_number', 'move_id', 'name', 'product_id', 'quantity', 'quantity2', 'price_unit', 'tax_ids', 'tax_ids_2',
                   'discount',
                   'discount2', 'discount3', 'EjercicioAlbaran', 'SerieAlbaran', 'unique_field', ]
        import re
        move_ids = []
        regex = r"\{(.*?)\}"
        with open("/tmp/not_found_moves.txt") as txt_file:
            a = txt_file.read()
            txt_file.close()

        matches = re.finditer(regex, a, re.MULTILINE | re.DOTALL)
        for matchNum, match in enumerate(matches):
            for groupNum in range(0, len(match.groups())):
                move_ids.append(int(match.group(1).split(':')[1].split(',')[0].strip()))

        move_ids = tuple(set(move_ids))
        # cursor.execute(
        #     f'select  NumeroAlbaran,EjercicioAlbaran ,SerieAlbaran from CabeceraAlbaranCliente where NumeroAlbaran in {move_ids} and EjercicioAlbaran >= 2017;')
        # fetched_move_ids = cursor.fetchall()
        # fetched_move_ids = list(filter(self.search_move, fetched_move_ids))
        # print(">>>>>>>>>>>>>fetched_move_ids", fetched_move_ids)
        res_partner_obj = self.env['res.partner']
        res_partner_payment_terms = self.env['account.payment.term']
        account_move_obj = self.env['account.move']
        ir_config_parameter_fetch = self.env['ir.config_parameter'].get_param('Fetch_value')
        product_product_obj = self.env['product.product']
        account_tax_new = self.env['account.tax']
        account_account_new = self.env['account.account']
        ir_config_parameter_fetch = self.env['ir.config_parameter'].get_param('Fetch_value')
        account_tax_21 = account_tax_new.search([('name', '=', 'IVA 21% (Bienes)')])
        account_tax_0 = account_tax_new.search(
            [('name', '=', 'IVA 0% Prestación de servicios intracomunitario')])
        account_tax_5_2 = account_tax_new.search(
            [('name', '=', '5.2% Recargo Equivalencia Ventas')])
        account_id = account_account_new.search([('code', '=', '700000')])
        company_id = self.env['res.company'].browse(1)
        for i in range(0, 60000, 1000):
            cursor.execute(
                f'select IdAlbaranCli,CodigoCliente,FechaAlbaran,FormadePago,Numerofactura,NumeroAlbaran,StatusFacturado,EjercicioAlbaran ,SerieAlbaran from CabeceraAlbaranCliente where EjercicioAlbaran >= 2017 order by CodigoCliente offset {i} rows FETCH NEXT {ir_config_parameter_fetch} ROWS ONLY;')

            move_vals_list = []
            for row in cursor.fetchall():
                j = dict(zip(move_columns, row))
                cursor.execute(
                    f'select  lineasPosicion,NumeroAlbaran,DescripcionArticulo,CodigoArticulo,Unidades,UnidadesServidas,Precio,[%Iva],[%Recargo],[%Descuento],[%Descuento2],[%Descuento3],EjercicioAlbaran ,SerieAlbaran ,lineasPosicion  from LineasAlbaranCliente where EjercicioAlbaran >= 2017 and NumeroAlbaran={j["name"]} and EjercicioAlbaran={j["EjercicioAlbaran"]} order by EjercicioAlbaran,NumeroAlbaran  offset {i} rows FETCH NEXT {ir_config_parameter_fetch} ROWS ONLY;')
                move_line_list = []
                for line_row in cursor.fetchall():
                    move_line = dict(zip(move_line_columns, line_row))
                    product_id_search = product_product_obj.search([('default_code', '=', move_line['product_id'])])
                    global account_tax_1
                    # partner_search = account_move_obj.search([('name', '=', j['move_id'])])
                    if move_line['tax_ids'] == 21:
                        account_tax_1 = account_tax_21
                    elif (move_line['tax_ids'] == 0):
                        account_tax_1 = account_tax_0
                    elif (move_line['tax_ids_2'] == 5.2):
                        account_tax_1 = account_tax_5_2
                    global n, p, q
                    if str(move_line['discount'].to_eng_string())[0] == '0':
                        n = 0
                    else:
                        n = float(move_line['discount'].to_eng_string())

                    if str(move_line['discount2'].to_eng_string())[0] == '0':
                        p = 0
                    else:
                        p = float(move_line['discount2'].to_eng_string())

                    if str(move_line['discount3'].to_eng_string())[0] == '0':
                        q = 0
                    else:
                        q = float(move_line['discount3'].to_eng_string())
                    vals = {
                        # 'move_id': account_move_id.id if j['move_id'] else False,
                        'name': str(move_line['name']),
                        'product_id': product_id_search[0].id if move_line['product_id'] and product_id_search else False,
                        'quantity': float(move_line['quantity'].to_eng_string()),
                        'quantity_2': float(move_line['quantity2'].to_eng_string()),
                        'price_unit': float(move_line['price_unit'].to_eng_string()),
                        'tax_ids': [(6, 0, [account_tax_1[0].id])] if account_tax_1 else False,
                        'exclude_from_invoice_tab': 0,
                        'account_id': account_id[0].id if account_id else False,
                        'discount': n,
                        'discount2': p,
                        'discount3': q,
                        'uid_number': move_line['uid_number'],
                    }
                    move_line_list.append(vals)
                product_pay_terms = res_partner_payment_terms.search([('name', '=', j['invoice_payment_term_id'])])
                partner_search = res_partner_obj.search([('ref', '=', j['partner_id'])])
                account_move_new = {
                    'partner_id': partner_search[0].id if j['partner_id'] and partner_search else False,
                    'invoice_date': str(j['invoice_date']),
                    'invoice_payment_term_id': product_pay_terms[0].id if j['invoice_payment_term_id'] and product_pay_terms else False,
                    'ref': j['ref'],
                    'journal_id': 1,
                    'currency_id': 1,
                    'state': 'draft',
                    'move_type': 'out_invoice',
                    'statusfacturado': j['StatusFacturado'],
                    'name': j['name'],
                    'ejercicioalbaran': j['EjercicioAlbaran'],
                    'seriealbaran': j['SerieAlbaran'],
                    'invoice_line_ids' : [(0, 0, ml) for ml in move_line_list],
                    'uid_number': j['uid_number'],
                }
                move_vals_list.append(account_move_new)
            try:
                moves = account_move_obj.create(move_vals_list)
                print("{>>>>>>>>>>>>moves", moves, len(moves))
            except Exception as e:
                print('Excepetion========', e)
