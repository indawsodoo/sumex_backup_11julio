from odoo import models, fields, api


class sumex_apps_imports_csv_instructions_wizard(models.Model):

    _name = 'sumex_apps_imports_csv_instructions_wizard'
    _description = 'Wizard para instrucciones del importador csv'

    csv_instructions = fields.Html(string="Instrucciones")

    import_name = fields.Selection(  # hacer field related
        string = 'Tipo',
        selection = lambda self: self.env['sumex_apps_imports_csv'].import_names
    )

    @api.onchange('import_name')
    def _update_csv_instructions(self):

        self.csv_instructions = "(selecciona Tipo para visualizar)"

        obj = False
        found = False
        try:
            obj = self.env[self.import_name].sudo()
            found = True
        except:
            obj = False
            found = False

        if found:
            print("obj=")
            print(obj)
            self.csv_instructions = """""" \
                """<i>La primera fila del fichero CSV tiene que ser obligatoriamente una cabecera.</i><br>""" \
                """<i>La cabecera del csv ha de tener los nombres exactos descritos, aunque no sea en el mismo orden (siendo las negritas campo obligatorio)</i><br>"""
            for item in obj.fieldnames:
                print(item)
                fieldname = item[0]
                fieldname_required = item[1]
                if fieldname_required:
                    self.csv_instructions += """&nbsp;&nbsp;&nbsp;- <b>%s</b><br>""" % fieldname
                else:
                    self.csv_instructions += """&nbsp;&nbsp;&nbsp;- %s<br>""" % fieldname
