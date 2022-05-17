# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import pymssql
import odoorpc
import logging


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    statusfacturado = fields.Char('StatusFacturado')
    ejercicioalbaran = fields.Char('EjercicioAlbaran')
    seriealbaran = fields.Char('SerieAlbaran')

    def account_move_cron_job_custom_indaws_new(self):

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
