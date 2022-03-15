# -*- coding: utf-8 -*-

"""
	ESTE IMPORTADOR USA CAMPOS EXTENDIDOS EN EL MODULO 'sumex_apps_sage_inherits'
"""

from odoo import models


class sumex_apps_imports_csv_import_sage_ventas_lineas(models.AbstractModel):

	_description = "modulo importador"

	_import_fields = [

		# Campos que participan en la importacion del modelo
		{'csv_column_name': 'NumeroPedido', 'required_header_field': True, 'required_value': True, 'save_as_inherit_fieldname': '_sage_field_numeropedido'},
		{'csv_column_name': 'CodigoArticulo', 'required_header_field': True, 'required_value': True, 'save_as_inherit_fieldname': '_sage_field_codigoarticulo'},
		{'csv_column_name': 'DescripcionArticulo', 'required_header_field': True, 'required_value': True, 'save_as_inherit_fieldname': '_sage_field_descripcionarticulo'},
		{'csv_column_name': 'ImporteCoste', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importecoste'},
		{'csv_column_name': 'ImporteBruto', 'required_header_field': True, 'required_value': True, 'save_as_inherit_fieldname': '_sage_field_importebruto'},
		{'csv_column_name': 'UnidadesServidas', 'required_header_field': True, 'required_value': True, 'save_as_inherit_fieldname': '_sage_field_unidadeservidas'},

		# Campos que NO participan en la importacion del modelo, pero se incluyen a nivel informativo
		{'csv_column_name': 'CodigoEmpresa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoempresa'},
		{'csv_column_name': 'EjercicioPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejerciciopedido'},
		{'csv_column_name': 'SeriePedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_seriepedido'},
		{'csv_column_name': 'Orden', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_orden'},
		{'csv_column_name': 'LineasPosicion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_lineasposicion'},
		{'csv_column_name': 'LineasPosicionCompuesto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_lineasposicioncompuesto'},
		{'csv_column_name': 'LineasPosicionRegalo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_lineasposicionregalo'},
		{'csv_column_name': 'FechaRegistro', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fecharegistro'},
		{'csv_column_name': 'FechaPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechapedido'},
		{'csv_column_name': 'CodigoAlmacen', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoalmacen'},
		{'csv_column_name': 'CodigoAlmacenAnterior', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoalmacenanterior'},
		{'csv_column_name': 'AlmacenContrapartida', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_almacencontrapartida'},
		{'csv_column_name': 'Partida', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_partida'},
		{'csv_column_name': 'UnidadMedida1_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadmedida1'},
		{'csv_column_name': 'UnidadMedida2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadmedida2'},
		{'csv_column_name': 'FactorConversion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_factorconversion'},
		{'csv_column_name': 'CodigoFamilia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigofamilia'},
		{'csv_column_name': 'CodigoSubfamilia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubfamilia'},
		{'csv_column_name': 'Descripcion2Articulo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_descripcion2articulo'},
		{'csv_column_name': 'DescripcionLinea', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_descripcionlinea'},
		{'csv_column_name': 'CodigodelCliente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodelcliente'},
		{'csv_column_name': 'CodigoProveedor', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoproveedor'},
		{'csv_column_name': 'CodigoDefinicion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodefinicion'},
		{'csv_column_name': 'CodigoTransaccion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotransaccion'},
		{'csv_column_name': 'CodigoArancelario', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoarancelario'},
		{'csv_column_name': 'CodigoProyecto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoproyecto'},
		{'csv_column_name': 'CodigoSeccion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoseccion'},
		{'csv_column_name': 'CodigoDepartamento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodepartamento'},
		{'csv_column_name': 'FechaCaduca', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechacaduca'},
		{'csv_column_name': 'FechaNecesaria', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechanecesaria'},
		{'csv_column_name': 'FechaEntrega', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaentrega'},
		{'csv_column_name': 'FechaTope', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechatope'},
		{'csv_column_name': 'Ubicacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ubicacion'},
		{'csv_column_name': 'SuPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_supedido'},
		{'csv_column_name': 'ReservarStock_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_reservarstock'},
		{'csv_column_name': 'AcumulaEstadistica_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_acumulaestadistica'},
		{'csv_column_name': 'BloqueoRebaje_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_bloqueorebaje'},
		{'csv_column_name': 'Estado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_estado'},
		{'csv_column_name': 'EstadoAnterior', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_estadoanterior'},
		{'csv_column_name': 'StatusEstadis', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_statusestadis'},
		{'csv_column_name': 'StatusPedidoPro', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_statuspedidopro'},
		{'csv_column_name': 'CompletadaFabricacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_completadafabricacion'},
		{'csv_column_name': 'Formula', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_formula'},
		{'csv_column_name': 'FormulaLote', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_formulalote'},
		{'csv_column_name': 'Lote_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_lote'},
		{'csv_column_name': 'Componente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_componente'},
		{'csv_column_name': 'CodigoColor_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocolor'},
		{'csv_column_name': 'GrupoTalla_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_grupotalla'},
		{'csv_column_name': 'CodigoTalla01_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotalla01'},
		{'csv_column_name': 'IvaIncluido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ivaincluido'},
		{'csv_column_name': 'GrupoIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_grupoiva'},
		{'csv_column_name': 'CodigoIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoiva'},
		{'csv_column_name': '%Iva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_iva'},
		{'csv_column_name': '%Recargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_recargo'},
		{'csv_column_name': '%BaseCorreccion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_basecorreccion'},
		{'csv_column_name': 'EjercicioPedidoPro', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejerciciopedidopro'},
		{'csv_column_name': 'SeriePedidoPro', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_seriepedidopro'},
		{'csv_column_name': 'NumeroPedidoPro', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numeropedidopro'},
		{'csv_column_name': 'PesoBrutoUnitario_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesobrutounitario'},
		{'csv_column_name': 'PesoBruto_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesobruto'},
		{'csv_column_name': 'PesoNetoUnitario_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesonetounitario'},
		{'csv_column_name': 'PesoNeto_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesoneto'},
		{'csv_column_name': 'VolumenUnitario_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_volumenunitario'},
		{'csv_column_name': 'Volumen_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_volumen'},
		{'csv_column_name': 'CodigoAgrupacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoagrupacion'},
		{'csv_column_name': 'AgrupacionesPedidas', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_agrupacionespedidas'},
		{'csv_column_name': 'AgrupacionesPendientes', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_agrupacionespendientes'},
		{'csv_column_name': 'AgrupacionesaServir', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_agrupacionesaservir'},
		{'csv_column_name': 'UnidadesAgrupacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadesagrupacion'},
		{'csv_column_name': 'UnidadesPendientesFabricar', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadespendientesfabricar'},
		{'csv_column_name': 'UnidadesEnFabricacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadesenfabricacion'},
		{'csv_column_name': 'UnidadesAFabricar', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadesafabricar'},
		{'csv_column_name': 'UnidadesPedidas', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadespedidas'},
		{'csv_column_name': 'UnidadesPendientes', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadespendientes'},
		{'csv_column_name': 'UnidadesPendAnterior', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadespendanterior'},
		{'csv_column_name': 'UnidadesaServir', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadesaservir'},
		{'csv_column_name': 'Unidades2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidades2'},
		{'csv_column_name': 'Unidades2aServir_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidades2aservir'},
		{'csv_column_name': 'UnidadesRegalo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_unidadesregalo'},
		{'csv_column_name': 'Precio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_precio'},
		{'csv_column_name': 'PrecioCoste', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_preciocoste'},
		{'csv_column_name': '%Descuento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuento'},
		{'csv_column_name': '%Descuento2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuento2'},
		{'csv_column_name': '%Descuento3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuento3'},
		{'csv_column_name': 'CodigoComisionista', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista'},
		{'csv_column_name': 'CodigoComisionista2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista2'},
		{'csv_column_name': 'CodigoComisionista3_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista3'},
		{'csv_column_name': 'CodigoComisionista4_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista4'},
		{'csv_column_name': 'CodigoJefeVenta_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigojefeventa'},
		{'csv_column_name': 'CodigoJefeZona_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigojefezona'},
		{'csv_column_name': '%Comision', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision'},
		{'csv_column_name': '%Comision2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision2'},
		{'csv_column_name': '%Comision3_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision3'},
		{'csv_column_name': '%Comision4_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision4'},
		{'csv_column_name': 'ComisionSobreVenta%_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comisionsobreventapercent'},
		{'csv_column_name': 'ComisionSobreZona%_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comisionsobrezonapercent'},
		{'csv_column_name': 'ImporteBrutoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importebrutodivisa'},
		{'csv_column_name': 'ImporteBrutoPendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importebrutopendiente'},
		{'csv_column_name': 'ImporteDescuento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedescuento'},
		{'csv_column_name': 'ImporteDescuentoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedescuentodivisa'},
		{'csv_column_name': 'ImporteDescuentoPendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedescuentopendiente'},
		{'csv_column_name': 'ImporteNeto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeneto'},
		{'csv_column_name': 'ImporteNetoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importenetodivisa'},
		{'csv_column_name': 'ImporteNetoPendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importenetopendiente'},
		{'csv_column_name': 'ImporteDescuentoCliente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedescuentocliente'},
		{'csv_column_name': 'ImporteDtoClienteDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedtoclientedivisa'},
		{'csv_column_name': 'ImporteParcial', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeparcial'},
		{'csv_column_name': 'ImporteParcialDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeparcialdivisa'},
		{'csv_column_name': 'ImporteParcialPendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeparcialpendiente'},
		{'csv_column_name': 'ImporteProntoPago', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeprontopago'},
		{'csv_column_name': 'ImporteProntoPagoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeprontopagodivisa'},
		{'csv_column_name': 'BaseImponible', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_baseimponible'},
		{'csv_column_name': 'BaseImponibleDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_baseimponibledivisa'},
		{'csv_column_name': 'BaseImponiblePendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_baseimponiblependiente'},
		{'csv_column_name': 'BaseIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_baseiva'},
		{'csv_column_name': 'BaseIvaDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_baseivadivisa'},
		{'csv_column_name': 'CuotaIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cuotaiva'},
		{'csv_column_name': 'CuotaIvaDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cuotaivadivisa'},
		{'csv_column_name': 'CuotaRecargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cuotarecargo'},
		{'csv_column_name': 'CuotaRecargoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cuotarecargodivisa'},
		{'csv_column_name': 'TotalIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_totaliva'},
		{'csv_column_name': 'TotalIvaDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_totalivadivisa'},
		{'csv_column_name': 'ImporteLiquido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeliquido'},
		{'csv_column_name': 'ImporteLiquidoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeliquidodivisa'},
		{'csv_column_name': 'ImporteRappel', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importerappel'},
		{'csv_column_name': 'ImporteRappelDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importerappeldivisa'},
		{'csv_column_name': 'EjercicioOferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejerciciooferta'},
		{'csv_column_name': 'SerieOferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_serieoferta'},
		{'csv_column_name': 'NumeroOferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numerooferta'},
		{'csv_column_name': 'TipoArticulo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipoarticulo'},
		{'csv_column_name': 'LineaPosAbonoLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_lineaposabonolc'},
		{'csv_column_name': 'GestionCompras', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_gestioncompras'},
		{'csv_column_name': 'NumeroSerieLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numeroserielc'},
		{'csv_column_name': 'FactorPrecioVenta_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_factorprecioventa'},
		{'csv_column_name': 'TipoUnidadCalculo_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipounidadcalculo'},
		{'csv_column_name': 'Largo_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_largo'},
		{'csv_column_name': 'Alto_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_alto'},
		{'csv_column_name': 'Ancho_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ancho'},
		{'csv_column_name': 'Dimension_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_dimension'},
		{'csv_column_name': 'CodigoDun14', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodun14'},
		{'csv_column_name': 'PorMargenBeneficio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pormargenbeneficio'},
		{'csv_column_name': 'MargenBeneficio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_margenbeneficio'},
		{'csv_column_name': 'EdiSellerNumber', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_edisellernumber'},
		{'csv_column_name': 'EdiBatchNumber', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_edibatchnumber'},
		{'csv_column_name': 'EdiISBN', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ediisbn'},
		{'csv_column_name': 'EdiSerialNumber', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ediserialnumber'},
		{'csv_column_name': 'EdiEtiquetaEAN', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_edietiquetaean'},
		{'csv_column_name': 'EjercicioExpediente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejercicioexpediente'},
		{'csv_column_name': 'SerieExpediente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_serieexpediente'},
		{'csv_column_name': 'NumeroExpediente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numeroexpediente'},
		{'csv_column_name': 'Suplido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_suplido'},
		{'csv_column_name': 'AnaLote', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_analote'},
		{'csv_column_name': 'AnaCapitulo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_anacapitulo'},
		{'csv_column_name': 'PrecioTotal', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_preciototal'},
		{'csv_column_name': 'TarifaPrecioLin', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tarifapreciolin'},
		{'csv_column_name': 'SuContrato', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sucontrato'},
		{'csv_column_name': 'ArticuloEquivalente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_articuloequivalente'},
		{'csv_column_name': 'CausaExencion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_causaexencion'},
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

		order = self.env['sumex_apps_imports_csv_import_sage_ventas_cabeceras'].sudo()._get_order(company_id, file_csv_content_row)
		if isinstance(order, dict) and 'error' in order:
			return order
		if not order:
			# El pedido tiene que existir para poder insertar sus lineas
			return {'error': "El pedido '%s' no existe, es necesario para vincular las lineas de pedido" % (file_csv_content_row['numeropedido'])}

		return True

	def import_row(self, file_csv_content_row_num, company_id, file_csv_header, file_csv_content_row):

		"""
			Este método "import_row" es ejecutado en un bucle del objeto importador(sumex_apps_imports_csv)
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			El retorno se asumirá como correcto al no ser que se retorne {'error':}
		"""

		precio_venta = 0
		try:
			precio_venta = float(file_csv_content_row['importecoste'])
		except:
			pass
		precio_compra = 0
		try:
			precio_compra = float(file_csv_content_row['importebruto'])
		except:
			pass

		product_referencia = file_csv_content_row['codigoarticulo']
		product_name = file_csv_content_row['descripcionarticulo'].title()

		product_template = self.env['sumex_apps_imports_csv_library'].sudo().get_or_create_product_template(
			company_id = company_id,
			product_referencia = product_referencia,
			product_name = product_name,
			descripcion = '',
			precio_venta = precio_venta,
			precio_compra = precio_compra
		)
		if isinstance(product_template, dict) and 'error' in product_template:
			return product_template

		order = self.env['sumex_apps_imports_csv_import_sage_ventas_cabeceras'].sudo()._get_order(company_id, file_csv_content_row)
		if isinstance(order, dict) and 'error' in order:
			return order
		if not order:
			# El pedido tiene que existir para poder insertar sus lineas
			return {'error': "El pedido '%s' no existe, es necesario para vincular las lineas de pedido" % (file_csv_content_row['numeropedido'])}

		line_price = file_csv_content_row['importebruto']
		line_qty = file_csv_content_row['unidadesservidas']
		self._get_or_create_order_line(company_id, file_csv_content_row, product_template, order.id, line_price, line_qty)

		return True

	def _get_exception_msg(self, name, e):

		import sys
		exc_type, exc_obj, exc_tb = sys.exc_info()
		exception_line_num = exc_tb.tb_lineno
		msg = "'%s' (line=%s) msg = %s" % (__name__, exception_line_num, str(e))
		return msg

	def _get_or_create_order_line(self, company_id, file_csv_content_row, product_template, order_id, line_price, line_qty):

		product_template_id = product_template.id
		product_template_name = product_template.name
		product_id = product_template.product_variant_id.id

		if not company_id:
			company_id = self.env.user.company_id.id
		model = self.env['sale.order.line'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		try:
			row = model.search([
				('name', '=', product_template_name),
				('order_id', '=', order_id),
				('product_template_id', '=', product_template_id),
				('company_id', '=', company_id),
				('price_unit', '=', line_price),
				('product_uom_qty', '=', line_qty)
			])
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		
		if row:
			return

		try:
			model.create({
				'name': product_template_name,
				'order_id':  order_id,
				'product_template_id': product_template_id,
				'product_id': product_id,
				'company_id': company_id,
				'price_unit': line_price,
				'product_uom_qty': line_qty,
				'customer_lead': 0
			})
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}

		return True
