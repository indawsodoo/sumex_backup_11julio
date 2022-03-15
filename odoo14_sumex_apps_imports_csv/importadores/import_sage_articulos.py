# -*- coding: utf-8 -*-

"""
	ESTE IMPORTADOR USA CAMPOS EXTENDIDOS EN EL MODULO 'sumex_apps_sage_inherits'
"""

from odoo import models


class sumex_apps_imports_csv_import_sage_articulos(models.AbstractModel):

	_description = "modulo importador"

	_import_fields = [

		# Campos que participan en la importacion del modelo
		{'csv_column_name': 'codigoarticulo', 'required_header_field': True, 'required_value': True, 'save_as_inherit_fieldname': '_sage_field_codigoarticulo'},
		{'csv_column_name': 'descripcionarticulo', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_descripcionarticulo'},
		{'csv_column_name': 'precioventa', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioventa'},
		{'csv_column_name': 'preciocompra', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_preciocompra'},
		{'csv_column_name': 'comentarioarticulo', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comentarioarticulo'},
		{'csv_column_name': 'marcaproducto', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_marcaproducto'},

		# Campos que NO participan en la importacion del modelo, pero se incluyen a nivel informativo
		{'csv_column_name': 'codigoempresa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoempresa'},
		{'csv_column_name': 'descripcion2articulo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_descripcion2articulo'},
		{'csv_column_name': 'descripcionlinea', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_descripcionlinea'},
		{'csv_column_name': 'codigoalternativo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoalternativo'},
		{'csv_column_name': 'codigoalternativo2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoalternativo2'},
		{'csv_column_name': 'codigoarticulooferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoarticulooferta'},
		{'csv_column_name': 'codigoarancelario', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoarancelario'},
		{'csv_column_name': 'codigoproveedor', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoproveedor'},
		{'csv_column_name': 'referenciaedi_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_referenciaedi_'},
		{'csv_column_name': 'publicarinternet', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_publicarinternet'},
		{'csv_column_name': 'tipoarticulo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipoarticulo'},
		{'csv_column_name': 'utilizado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_utilizado'},
		{'csv_column_name': 'fechaalta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaalta'},
		{'csv_column_name': 'fechainiciooferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechainiciooferta'},
		{'csv_column_name': 'fechafinaloferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechafinaloferta'},
		{'csv_column_name': 'temporada', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_temporada'},
		{'csv_column_name': 'tipoenvase_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipoenvase_'},
		{'csv_column_name': 'unidadmedida2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadmedida2_'},
		{'csv_column_name': 'unidadmedidaalternativa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadmedidaalternativa_'},
		{'csv_column_name': 'factorconversion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_factorconversion_'},
		{'csv_column_name': 'codigofamilia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigofamilia'},
		{'csv_column_name': 'codigosubfamilia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubfamilia'},
		{'csv_column_name': 'codigodivisa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodivisa'},
		{'csv_column_name': 'codigoproyecto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoproyecto'},
		{'csv_column_name': 'codigoseccion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoseccion'},
		{'csv_column_name': 'codigodepartamento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodepartamento'},
		{'csv_column_name': 'codigodefinicion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodefinicion_'},
		{'csv_column_name': 'valoracionstock', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_valoracionstock'},
		{'csv_column_name': 'tratamientopartidas', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tratamientopartidas'},
		{'csv_column_name': 'contadorpartida', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_contadorpartida'},
		{'csv_column_name': 'colores_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_colores_'},
		{'csv_column_name': 'grupotalla_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_grupotalla_'},
		{'csv_column_name': 'acumulaestadistica_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_acumulaestadistica_'},
		{'csv_column_name': 'generacompraautomatica_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_generacompraautomatica_'},
		{'csv_column_name': 'ivaincluido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ivaincluido'},
		{'csv_column_name': 'bloqueocompra', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_bloqueocompra'},
		{'csv_column_name': 'bloqueopedidocompra', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_bloqueopedidocompra'},
		{'csv_column_name': 'bloqueoalbaranventa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_bloqueoalbaranventa'},
		{'csv_column_name': 'bloqueopedidoventa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_bloqueopedidoventa'},
		{'csv_column_name': 'unidadesminimasoferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadesminimasoferta'},
		{'csv_column_name': 'unidadesregalooferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadesregalooferta'},
		{'csv_column_name': 'stockminimo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_stockminimo'},
		{'csv_column_name': 'stockmaximo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_stockmaximo'},
		{'csv_column_name': 'puntopedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_puntopedido'},
		{'csv_column_name': 'lotepedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_lotepedido'},
		{'csv_column_name': 'grupoiva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_grupoiva'},
		{'csv_column_name': 'grupoivacompras', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_grupoivacompras'},
		{'csv_column_name': '%Margen', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_margen'},
		{'csv_column_name': 'costefabricacionunitario', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_costefabricacionunitario'},
		{'csv_column_name': 'preciocosteestandar', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_preciocosteestandar'},
		{'csv_column_name': 'precioventaconiva1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioventaconiva1'},
		{'csv_column_name': 'precioventaconiva2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioventaconiva2'},
		{'csv_column_name': 'precioventaconiva3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioventaconiva3'},
		{'csv_column_name': 'precioventasiniva1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioventasiniva1'},
		{'csv_column_name': 'precioventasiniva2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioventasiniva2'},
		{'csv_column_name': 'precioventasiniva3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioventasiniva3'},
		{'csv_column_name': 'precioofertaconiva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioofertaconiva'},
		{'csv_column_name': 'precioofertasiniva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioofertasiniva'},
		{'csv_column_name': '%Descuento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuento'},
		{'csv_column_name': '%Descuento2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuento2'},
		{'csv_column_name': '%Descuento3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuento3'},
		{'csv_column_name': '%DescuentoCompras', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuentocompras'},
		{'csv_column_name': '%DescuentoCompras2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuentocompras2'},
		{'csv_column_name': '%DescuentoCompras3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuentocompras3'},
		{'csv_column_name': 'descuentooferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_descuentooferta'},
		{'csv_column_name': 'aplicardescuentos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_aplicardescuentos'},
		{'csv_column_name': 'codigocomisionista', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista'},
		{'csv_column_name': 'codigocomisionista2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista2_'},
		{'csv_column_name': 'codigocomisionista3_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista3_'},
		{'csv_column_name': 'codigocomisionista4_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista4_'},
		{'csv_column_name': '%Comision', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision'},
		{'csv_column_name': '%Comision2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision2_'},
		{'csv_column_name': '%Comision3_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision3_'},
		{'csv_column_name': '%Comision4_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision4_'},
		{'csv_column_name': 'pesobrutounitario_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesobrutounitario_'},
		{'csv_column_name': 'pesonetounitario_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesonetounitario_'},
		{'csv_column_name': 'volumenunitario_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_volumenunitario_'},
		{'csv_column_name': 'formulalote', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_formulalote'},
		{'csv_column_name': 'lote_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_lote_'},
		{'csv_column_name': 'formula', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_formula'},
		{'csv_column_name': 'lotefabricacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_lotefabricacion'},
		{'csv_column_name': 'nivelcompuesto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nivelcompuesto'},
		{'csv_column_name': 'tipodemanda', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipodemanda'},
		{'csv_column_name': 'generarplanprod', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_generarplanprod'},
		{'csv_column_name': 'usarstockseg', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_usarstockseg'},
		{'csv_column_name': '%StockSeguridad', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_stockseguridad'},
		{'csv_column_name': 'demandamediadiaria', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_demandamediadiaria'},
		{'csv_column_name': 'factorcrecimiento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_factorcrecimiento'},
		{'csv_column_name': 'periodospromediar', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_periodospromediar'},
		{'csv_column_name': 'tasaproducciondiaria', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tasaproducciondiaria'},
		{'csv_column_name': 'tiempomedioreposicion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tiempomedioreposicion'},
		{'csv_column_name': 'numdecimalesunidades', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numdecimalesunidades'},
		{'csv_column_name': 'periodovida', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_periodovida'},
		{'csv_column_name': 'tipoabc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipoabc'},
		{'csv_column_name': 'codigocategorialc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocategorialc'},
		{'csv_column_name': 'codigosubcategorialc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubcategorialc'},
		{'csv_column_name': 'codigoclasearticulolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoclasearticulolc'},
		{'csv_column_name': 'codigotipoarticulolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipoarticulolc'},
		{'csv_column_name': 'codigosubtipoarticulolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubtipoarticulolc'},
		{'csv_column_name': 'codigogrupoarticulolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigogrupoarticulolc'},
		{'csv_column_name': 'codigosubgrupoarticulolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubgrupoarticulolc'},
		{'csv_column_name': 'codigomodolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigomodolc'},
		{'csv_column_name': 'codigofabricantelc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigofabricantelc'},
		{'csv_column_name': 'codigofamiliafabricantelc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigofamiliafabricantelc'},
		{'csv_column_name': 'codigoconjuntolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoconjuntolc'},
		{'csv_column_name': 'codigosubconjuntolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubconjuntolc'},
		{'csv_column_name': 'maximosinretencionlc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_maximosinretencionlc'},
		{'csv_column_name': 'tratanumerosserielc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tratanumerosserielc'},
		{'csv_column_name': 'sonhoraslc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sonhoraslc'},
		{'csv_column_name': 'articulonocodificadolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_articulonocodificadolc'},
		{'csv_column_name': 'preciocosteeditablelc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_preciocosteeditablelc'},
		{'csv_column_name': 'codigotipoperiodicidadpreciolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipoperiodicidadpreciolc'},
		{'csv_column_name': 'liquidablelc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_liquidablelc'},
		{'csv_column_name': 'codigotipocoberturalc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipocoberturalc'},
		{'csv_column_name': 'obsoletolc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_obsoletolc'},
		{'csv_column_name': 'codigoareacompetencialc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoareacompetencialc'},
		{'csv_column_name': 'imagenext', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_imagenext'},
		{'csv_column_name': 'gestioncompras', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_gestioncompras'},
		{'csv_column_name': 'unidadmedidacompras_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadmedidacompras_'},
		{'csv_column_name': 'unidadmedidaventas_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadmedidaventas_'},
		{'csv_column_name': 'unidadmedidafabricacion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadmedidafabricacion_'},
		{'csv_column_name': 'codigoserie', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoserie'},
		{'csv_column_name': 'unidadmedidaserie', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadmedidaserie'},
		{'csv_column_name': 'factorpreciocompra_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_factorpreciocompra_'},
		{'csv_column_name': 'factorprecioventa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_factorprecioventa_'},
		{'csv_column_name': 'tipounidadcalculo_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipounidadcalculo_'},
		{'csv_column_name': 'medida', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_medida'},
		{'csv_column_name': 'tipoarticulopresupuesto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipoarticulopresupuesto'},
		{'csv_column_name': 'tipocodificado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipocodificado'},
		{'csv_column_name': 'codigoperiodicidadprecio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoperiodicidadprecio'},
		{'csv_column_name': 'cobrardevoluciontardia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cobrardevoluciontardia'},
		{'csv_column_name': 'cobrarentregaadelantada', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cobrarentregaadelantada'},
		{'csv_column_name': 'devolverdevolucionadelantada', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_devolverdevolucionadelantada'},
		{'csv_column_name': 'devolverentregatardia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_devolverentregatardia'},
		{'csv_column_name': 'codigoarticulofacturacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoarticulofacturacion'},
		{'csv_column_name': 'precioperiodoretraso', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioperiodoretraso'},
		{'csv_column_name': 'preciounidadperdida', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_preciounidadperdida'},
		{'csv_column_name': 'partirperiodos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_partirperiodos'},
		{'csv_column_name': 'tipoarticuloalquiler', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipoarticuloalquiler'},
		{'csv_column_name': 'notraspasarsfa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_notraspasarsfa'},
		{'csv_column_name': 'codigocontaje', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocontaje'},
		{'csv_column_name': 'precioportramos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precioportramos'},
		{'csv_column_name': 'suplido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_suplido'},
		{'csv_column_name': 'codigonacionorigen', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigonacionorigen'},
		{'csv_column_name': 'tipocodigobarrassr', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipocodigobarrassr'},
		{'csv_column_name': 'pesablesr', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesablesr'},
		{'csv_column_name': 'imagentactilsr', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_imagentactilsr'},
		{'csv_column_name': 'taraunitaria_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_taraunitaria_'},
		{'csv_column_name': 'preciomodificablesr', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_preciomodificablesr'},
		{'csv_column_name': 'noagruparsr', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_noagruparsr'},
		{'csv_column_name': 'enviarasr', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_enviarasr'},
		{'csv_column_name': 'impresionresguardosr', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_impresionresguardosr'},
		{'csv_column_name': 'periodogarantiasr', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_periodogarantiasr'},
		{'csv_column_name': 'novedadesweb', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_novedadesweb'},
		{'csv_column_name': 'idarticulo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_idarticulo'},
		{'csv_column_name': 'publicargcrm', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_publicargcrm'},
		{'csv_column_name': 'mesesgarantiaventa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mesesgarantiaventa'},
		{'csv_column_name': 'mesesgarantiacompra', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mesesgarantiacompra'},
		{'csv_column_name': 'mesesgarantiareparacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mesesgarantiareparacion'},
		{'csv_column_name': 'fechamodificacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechamodificacion'},
		{'csv_column_name': 'fecharecepcionsumex', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fecharecepcionsumex'},
		{'csv_column_name': 'factors', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_factors'},
		{'csv_column_name': 'estaencatalogo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_estaencatalogo'},
		{'csv_column_name': 'codigoalternativo3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoalternativo3'},
		{'csv_column_name': 'largo_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_largo_'},
		{'csv_column_name': 'ancho_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ancho_'},
		{'csv_column_name': 'alto_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_alto_'},
		{'csv_column_name': 'fabricadoen', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fabricadoen'},
		{'csv_column_name': 's_codigofiscalproducto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_s_codigofiscalproducto'},
		{'csv_column_name': 'moq', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_moq'},
		{'csv_column_name': 'udcajaouter', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_udcajaouter'},
		{'csv_column_name': 'udcajainner', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_udcajainner'},
		{'csv_column_name': 'largoouter', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_largoouter'},
		{'csv_column_name': 'largoinner', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_largoinner'},
		{'csv_column_name': 'anchoouter', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_anchoouter'},
		{'csv_column_name': 'anchoinner', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_anchoinner'},
		{'csv_column_name': 'altoouter', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_altoouter'},
		{'csv_column_name': 'altoinner', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_altoinner'},
		{'csv_column_name': 'gwouter', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_gwouter'},
		{'csv_column_name': 'gwinner', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_gwinner'},
		{'csv_column_name': 'nwouter', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nwouter'},
		{'csv_column_name': 'nwinner', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nwinner'},
		{'csv_column_name': 'volumenouter', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_volumenouter'},
		{'csv_column_name': 'volumeninner', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_volumeninner'},
		{'csv_column_name': 'codigotembalaje', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotembalaje'},
		{'csv_column_name': 'estaentarifa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_estaentarifa'},
		{'csv_column_name': 'articuloequivalente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_articuloequivalente'},
		{'csv_column_name': 'fechaprevistasumex', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaprevistasumex'},
	]

	def get_import_fields(self):

		return self._import_fields

	def hook_pre_process(self, company_id, file_csv_header, file_csv_content):

		pass

	def hook_post_process(self, company_id, file_csv_header, file_csv_content_row_dict, file_csv_content):

		pass

	def validate_row(self, file_csv_content_row_num, company_id, file_csv_content_row):

		"""
			El importador ya realiza automaticamente las validaciones de 'required_header_field' y 'required_value'file_csv_content_row
			Aquí podemos validar el formato de valores y otras cuestiones

			Este método "validate_row" es ejecutado en un bucle antes de realizar la importación
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			Se puede retornar {'error':''} {'warning':''} o {'info':''} o simplemente nada.
		"""

		warnings = []

		# descripcionarticulo
		if not file_csv_content_row['descripcionarticulo']:
			warnings.append("La columna 'descripcion artículo' no contiene valor, se reemplazará por un valor aleatorio")

		if warnings:
			return {'warning': ("; ").join(warnings)}

		return True

	def import_row(self, file_csv_content_row_num, company_id, file_csv_header, file_csv_content_row):

		"""
			Este método "import_row" es ejecutado en un bucle del objeto importador(sumex_apps_imports_csv)
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			El retorno se asumirá como correcto al no ser que se retorne {'error':}
		"""

		product_referencia = file_csv_content_row['codigoarticulo']
		product_name = file_csv_content_row['descripcionarticulo']
		if product_name:
			product_name = product_name.title()
		else:
			product_name = "no-name %s" % product_referencia
		precio_venta = 0
		try:
			precio_venta = float(file_csv_content_row['precioventa'])
		except:
			pass
		precio_compra = 0
		try:
			precio_compra = float(file_csv_content_row['preciocompra'])
		except:
			pass
		descripcion = file_csv_content_row['comentarioarticulo']

		product_template = self.env['sumex_apps_imports_csv_library'].sudo().get_or_create_product_template(
			company_id = company_id,
			product_referencia = product_referencia,
			product_name = product_name,
			descripcion = descripcion,
			precio_venta = precio_venta,
			precio_compra = precio_compra
		)
		if isinstance(product_template, dict) and 'error' in product_template:
			return product_template

		# marca
		marca_nombre = file_csv_content_row['marcaproducto']
		result = self.env['sumex_apps_imports_csv_library'].sudo().get_or_create_marca(product_template, marca_nombre)
		if isinstance(result, dict) and 'error' in result:
			return result

		"""
		Inserciones adicionales
		"""
		list_values = {}
		changes = 0

		if file_csv_content_row['obsoletolc'] == "-1" or file_csv_content_row['obsoletolc'] == "1":
			list_values['purchase_ok'] = False
			list_values['sale_ok'] = False
			changes += 2
		else:
			list_values['purchase_ok'] = True
			list_values['sale_ok'] = True
			changes += 2

		if changes:
			try:
				product_template.write(list_values)
				product_template._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}

		dict_other_fields = {}
		result = self.env['sumex_apps_imports_csv_library'].update_extendedd_fields(product_template, self._import_fields, file_csv_content_row, dict_other_fields)
		if isinstance(result, dict) and 'error' in result:
			return result

		return True

