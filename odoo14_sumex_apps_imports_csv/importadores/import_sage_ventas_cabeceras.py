# -*- coding: utf-8 -*-

"""
	ESTE IMPORTADOR USA CAMPOS EXTENDIDOS EN EL MODULO 'sumex_apps_sage_inherits'
"""

from odoo import models


class sumex_apps_imports_csv_import_sage_ventas_cabeceras(models.AbstractModel):

	_description = "modulo importador"

	_import_fields = [

		# Campos que participan en la importacion del modelo
		{'csv_column_name': 'RazonSocial', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_razonsocial'},
		{'csv_column_name': 'Nombre', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nombre'},
		{'csv_column_name': 'Municipio', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_municipio'},
		{'csv_column_name': 'CifEuropeo', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cifeuropeo'},
		{'csv_column_name': 'Nacion', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nacion'},
		{'csv_column_name': 'ColaMunicipio', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_colamunicipio'},
		{'csv_column_name': 'CodigoPostal', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigopostal'},
		{'csv_column_name': 'FechaPedido', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechapedido'},
		{'csv_column_name': 'FormadePago', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_formadepago'},
		{'csv_column_name': 'FechaNecesaria', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechanecesaria'},
		{'csv_column_name': 'FechaEntrega', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaentrega'},
		{'csv_column_name': 'FechaTope', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechatope'},
		{'csv_column_name': 'NumeroPedido', 'required_header_field': True, 'required_value': True, 'save_as_inherit_fieldname': '_sage_field_numeropedido'},

		# Campos que NO participan en la importacion del modelo, pero se incluyen a nivel informativo
		{'csv_column_name': 'NumeroLineas', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numerolineas'},
		{'csv_column_name': 'Domicilio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domicilio'},
		{'csv_column_name': 'SeriePedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_seriepedido'},
		{'csv_column_name': 'EjercicioPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejerciciopedido'},
		{'csv_column_name': 'CodigoCliente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocliente'},
		{'csv_column_name': 'CodigoCadena', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocadena'},
		{'csv_column_name': 'SiglaNacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_siglanacion'},
		{'csv_column_name': 'NumeroPlazos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numeroplazos'},
		{'csv_column_name': 'DiasPrimerPlazo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_diasprimerplazo'},
		{'csv_column_name': 'DiasEntrePlazos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_diasentreplazos'},
		{'csv_column_name': 'DiasFijos1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_diasfijos1'},
		{'csv_column_name': 'DiasFijos2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_diasfijos2'},
		{'csv_column_name': 'DiasFijos3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_diasfijos3'},
		{'csv_column_name': 'InicioNoPago', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_inicionopago'},
		{'csv_column_name': 'FinNoPago', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_finnopago'},
		{'csv_column_name': 'ControlarFestivos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_controlarfestivos'},
		{'csv_column_name': 'DiasRetroceso', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_diasretroceso'},
		{'csv_column_name': 'MesesComerciales', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mesescomerciales'},
		{'csv_column_name': 'CodigoContable', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocontable'},
		{'csv_column_name': 'CodigoDefinicion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodefinicion'},
		{'csv_column_name': 'RemesaHabitual', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_remesahabitual'},
		{'csv_column_name': 'CodigoBanco', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigobanco'},
		{'csv_column_name': 'CodigoAgencia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoagencia'},
		{'csv_column_name': 'DC', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_dc'},
		{'csv_column_name': 'CCC', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ccc'},
		{'csv_column_name': 'IBAN', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_iban'},
		{'csv_column_name': 'DomicilioEnvio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domicilioenvio'},
		{'csv_column_name': 'DomicilioFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domiciliofactura'},
		{'csv_column_name': 'DomicilioRecibo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domiciliorecibo'},
		{'csv_column_name': 'CodigoProyecto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoproyecto'},
		{'csv_column_name': 'CodigoSeccion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoseccion'},
		{'csv_column_name': 'CodigoDepartamento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodepartamento'},
		{'csv_column_name': 'CodigoTransportistaEnvios', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotransportistaenvios'},
		{'csv_column_name': 'TipoPortesEnvios', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipoportesenvios'},
		{'csv_column_name': 'CodigoRetencion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoretencion'},
		{'csv_column_name': 'CodigoTransaccion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotransaccion'},
		{'csv_column_name': 'CodigoZona', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigozona'},
		{'csv_column_name': 'CodigoCanal', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocanal'},
		{'csv_column_name': 'CodigoRuta_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoruta'},
		{'csv_column_name': 'CodigoTerritorio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoterritorio'},
		{'csv_column_name': 'CodigoTipoEfecto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipoefecto'},
		{'csv_column_name': 'CodigoExportacion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoexportacion'},
		{'csv_column_name': 'CondicionExportacion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_condicionexportacion'},
		{'csv_column_name': 'TarifaPrecio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tarifaprecio'},
		{'csv_column_name': 'TarifaDescuento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tarifadescuento'},
		{'csv_column_name': 'GrupoIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_grupoiva'},
		{'csv_column_name': 'IndicadorIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_indicadoriva'},
		{'csv_column_name': 'IvaIncluido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ivaincluido'},
		{'csv_column_name': 'ServirCompleto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_servircompleto'},
		{'csv_column_name': 'ReservarStock_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_reservarstock'},
		{'csv_column_name': 'Estado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_estado'},
		{'csv_column_name': 'StatusAnalitica', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_statusanalitica'},
		{'csv_column_name': 'StatusAprobado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_statusaprobado'},
		{'csv_column_name': 'StatusListado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_statuslistado'},
		{'csv_column_name': 'StatusEstadis', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_statusestadis'},
		{'csv_column_name': 'Descuento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuento'},
		{'csv_column_name': 'ProntoPago', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_prontopago'},
		{'csv_column_name': 'Financiacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_financiacion'},
		{'csv_column_name': 'Retencion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_retencion'},
		{'csv_column_name': 'Rappel', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_rappel'},
		{'csv_column_name': 'CodigoComisionista', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista'},
		{'csv_column_name': 'CodigoComisionista2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista2'},
		{'csv_column_name': 'CodigoComisionista3_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista3'},
		{'csv_column_name': 'CodigoComisionista4_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista4'},
		{'csv_column_name': 'CodigoJefeVenta_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigojefeventa'},
		{'csv_column_name': 'CodigoJefeZona_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigojefezona'},
		{'csv_column_name': 'Comision', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision'},
		{'csv_column_name': 'Comision2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision2'},
		{'csv_column_name': 'Comision3_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision3'},
		{'csv_column_name': 'Comision4_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision4'},
		{'csv_column_name': 'ComisionSobreVenta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comisionsobreventa_percent'},
		{'csv_column_name': 'ComisionSobreZona', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comisionsobrezona_percent'},
		{'csv_column_name': 'PeriodicidadFacturas', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_periodicidadfacturas'},
		{'csv_column_name': 'MascaraPedido_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mascarapedido'},
		{'csv_column_name': 'AgruparAlbaranes', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_agruparalbaranes'},
		{'csv_column_name': 'AlbaranValorado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_albaranvalorado'},
		{'csv_column_name': 'CopiasAlbaran', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_copiasalbaran'},
		{'csv_column_name': 'CopiasFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_copiasfactura'},
		{'csv_column_name': 'CopiasPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_copiaspedido'},
		{'csv_column_name': 'ObservacionesCliente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_observacionescliente'},
		{'csv_column_name': 'ObservacionesPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_observacionespedido'},
		{'csv_column_name': 'ObservacionesAlbaran', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_observacionesalbaran'},
		{'csv_column_name': 'ObservacionesFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_observacionesfactura'},
		{'csv_column_name': 'SuPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_supedido'},
		{'csv_column_name': 'PesoBruto_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesobruto'},
		{'csv_column_name': 'PesoNeto_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pesoneto'},
		{'csv_column_name': 'Volumen_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_volumen'},
		{'csv_column_name': 'EnEuros_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_eneuros'},
		{'csv_column_name': 'CodigoDivisa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodivisa'},
		{'csv_column_name': 'CodigoIdioma_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoidioma'},
		{'csv_column_name': 'MantenerCambio_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mantenercambio'},
		{'csv_column_name': 'FactorCambio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_factorcambio'},
		{'csv_column_name': 'ImporteCambio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importecambio'},
		{'csv_column_name': 'ImporteCambioViejo_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importecambioviejo'},
		{'csv_column_name': 'ImporteCoste', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importecoste'},
		{'csv_column_name': 'ImporteBruto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importebruto'},
		{'csv_column_name': 'ImporteBrutoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importebrutodivisa'},
		{'csv_column_name': 'ImporteBrutoPendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importebrutopendiente'},
		{'csv_column_name': 'ImporteDescuentoLineas', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedescuentolineas'},
		{'csv_column_name': 'ImporteDtoLineasDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedtolineasdivisa'},
		{'csv_column_name': 'ImporteNetoLineas', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importenetolineas'},
		{'csv_column_name': 'ImporteNetoLineasDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importenetolineasdivisa'},
		{'csv_column_name': 'ImporteNetoLineasPendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importenetolineaspendiente'},
		{'csv_column_name': 'ImporteDescuento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedescuento'},
		{'csv_column_name': 'ImporteDescuentoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importedescuentodivisa'},
		{'csv_column_name': 'ImporteParcial', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeparcial'},
		{'csv_column_name': 'ImporteParcialDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeparcialdivisa'},
		{'csv_column_name': 'ImporteParcialPendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeparcialpendiente'},
		{'csv_column_name': 'ImporteProntoPago', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeprontopago'},
		{'csv_column_name': 'ImporteProntoPagoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeprontopagodivisa'},
		{'csv_column_name': 'BaseImponible', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_baseimponible'},
		{'csv_column_name': 'BaseImponibleDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_baseimponibledivisa'},
		{'csv_column_name': 'BaseImponiblePendiente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_baseimponiblependiente'},
		{'csv_column_name': 'TotalCuotaIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_totalcuotaiva'},
		{'csv_column_name': 'TotalCuotaIvaDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_totalcuotaivadivisa'},
		{'csv_column_name': 'TotalCuotaRecargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_totalcuotarecargo'},
		{'csv_column_name': 'TotalCuotaRecargoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_totalcuotarecargodivisa'},
		{'csv_column_name': 'TotalIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_totaliva'},
		{'csv_column_name': 'TotalIvaDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_totalivadivisa'},
		{'csv_column_name': 'ImporteFinanciacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importefinanciacion'},
		{'csv_column_name': 'ImporteFinanciacionDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importefinanciaciondivisa'},
		{'csv_column_name': 'ImporteLiquido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeliquido'},
		{'csv_column_name': 'ImporteLiquidoDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeliquidodivisa'},
		{'csv_column_name': 'ImporteRappel', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importerappel'},
		{'csv_column_name': 'ImporteRappelDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importerappeldivisa'},
		{'csv_column_name': 'EjercicioFacturaOriginal', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejerciciofacturaoriginal'},
		{'csv_column_name': 'SerieFacturaOriginal', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_seriefacturaoriginal'},
		{'csv_column_name': 'NumeroFacturaOriginal', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numerofacturaoriginal'},
		{'csv_column_name': 'EjercicioOferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejerciciooferta'},
		{'csv_column_name': 'SerieOferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_serieoferta'},
		{'csv_column_name': 'NumeroOferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numerooferta'},
		{'csv_column_name': 'CodigoTipoOperacionLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipooperacionlc'},
		{'csv_column_name': 'CodigoTipoOperacionOrigenLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipooperacionorigenlc'},
		{'csv_column_name': 'CodigoDivisionLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodivisionlc'},
		{'csv_column_name': 'CodigoAmbitoClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoambitoclientelc'},
		{'csv_column_name': 'CodigoClaseClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoclaseclientelc'},
		{'csv_column_name': 'CodigoSubclaseClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubclaseclientelc'},
		{'csv_column_name': 'CodigoTipoClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipoclientelc'},
		{'csv_column_name': 'CodigoGrupoClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigogrupoclientelc'},
		{'csv_column_name': 'CodigoActividadLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoactividadlc'},
		{'csv_column_name': 'CodigoSubactividadLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubactividadlc'},
		{'csv_column_name': 'ComercialAsignadoLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comercialasignadolc'},
		{'csv_column_name': 'FacturarCompletoLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_facturarcompletolc'},
		{'csv_column_name': 'IdFacturarCompletoLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_idfacturarcompletolc'},
		{'csv_column_name': 'IdFacturacionConjuntaLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_idfacturacionconjuntalc'},
		{'csv_column_name': 'IdDelegacionCentralLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_iddelegacioncentrallc'},
		{'csv_column_name': 'CodigoCampanaLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocampanalc'},
		{'csv_column_name': 'ReferenciaEdi_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_referenciaedi'},
		{'csv_column_name': 'CodigoMotivoAbonoLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigomotivoabonolc'},
		{'csv_column_name': 'EjercicioAlbaranOriginalLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejercicioalbaranoriginallc'},
		{'csv_column_name': 'SerieAlbaranOriginalLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_seriealbaranoriginallc'},
		{'csv_column_name': 'NumeroAlbaranOriginalLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numeroalbaranoriginallc'},
		{'csv_column_name': 'GenerarFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_generarfactura'},
		{'csv_column_name': 'ImporteACuentaP_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeacuentap'},
		{'csv_column_name': 'ImporteACuentaPDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeacuentapdivisa'},
		{'csv_column_name': 'ImporteConsumidoP', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeconsumidop'},
		{'csv_column_name': 'ImporteConsumidoPDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeconsumidopdivisa'},
		{'csv_column_name': 'EjercicioAlbaranDevolucionP', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejercicioalbarandevolucionp'},
		{'csv_column_name': 'SerieAlbaranDevolucionP', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_seriealbarandevolucionp'},
		{'csv_column_name': 'NumeroAlbaranDevolucionP', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numeroalbarandevolucionp'},
		{'csv_column_name': 'ImportePendientePAC', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importependientepac'},
		{'csv_column_name': 'ImportePendientePACDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importependientepacdivisa'},
		{'csv_column_name': 'ImporteFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importefactura'},
		{'csv_column_name': 'ImporteFacturaDivisa_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importefacturadivisa'},
		{'csv_column_name': 'PorMargenBeneficio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pormargenbeneficio'},
		{'csv_column_name': 'MargenBeneficio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_margenbeneficio'},
		{'csv_column_name': 'EjercicioExpediente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ejercicioexpediente'},
		{'csv_column_name': 'SerieExpediente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_serieexpediente'},
		{'csv_column_name': 'NumeroExpediente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numeroexpediente'},
		{'csv_column_name': 'OrigenDespacho', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_origendespacho'},
		{'csv_column_name': 'ImporteProvisiones', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeprovisiones'},
		{'csv_column_name': 'ImporteProvisionesNF', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeprovisionesnf'},
		{'csv_column_name': 'ImporteSuplidos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importesuplidos'},
		{'csv_column_name': 'ImporteProvisionesDivisa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeprovisionesdivisa'},
		{'csv_column_name': 'ImporteProvisionesNFDivisa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importeprovisionesnfdivisa'},
		{'csv_column_name': 'ImporteSuplidosDivisa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_importesuplidosdivisa'},
		{'csv_column_name': 'CodigoContableANT_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocontableant'},
		{'csv_column_name': 'RemesaHabitualANT_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_remesahabitualant'},
		{'csv_column_name': 'AnaLote', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_analote'},
		{'csv_column_name': 'AnaCapitulo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_anacapitulo'},
		{'csv_column_name': 'NoFacturable', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nofacturable'},
		{'csv_column_name': 'ObservacionesWeb', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_observacionesweb'},
		{'csv_column_name': 'SuPedidoWeb', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_supedidoweb'},
		{'csv_column_name': 'VarFechaTraspaso', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_varfechatraspaso'},
		{'csv_column_name': 'VarTraspasado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_vartraspasado'},
		{'csv_column_name': 'IdPedidoCli', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_idpedidocli'},
		{'csv_column_name': 'ReferenciaMandato', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_referenciamandato'},
		{'csv_column_name': 'Comentarios', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comentarios'},
		{'csv_column_name': 'SuContrato', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sucontrato'},
		{'csv_column_name': 'S_AplicarBaremosT', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_s_aplicarbaremost'},
		{'csv_column_name': 'S_UsuarioCrea', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_s_usuariocrea'},
		{'csv_column_name': 'S_NombreUsuario', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_s_nombreusuario'},
		{'csv_column_name': 'SUMEX_PedidoAServir', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_pedidoaservir'},
		{'csv_column_name': 'CP_EDIEMISOR', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_ediemisor'},
		{'csv_column_name': 'CP_EDIVENDEDOR', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_edivendedor'},
		{'csv_column_name': 'CP_EDICOMPRADOR', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_edicomprador'},
		{'csv_column_name': 'CP_EDI', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_edi'},
		{'csv_column_name': 'CP_FECHAENTINI', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_fechaentini'},
		{'csv_column_name': 'CP_FECHAENTFIN', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_fechaentfin'},
		{'csv_column_name': 'CP_LIBREVAR1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_librevar1'},
		{'csv_column_name': 'CP_LIBREVAR2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_librevar2'},
		{'csv_column_name': 'CP_PRECIOTRANSPORTE', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cp_preciotransporte'},
		{'csv_column_name': 'SUMEX_CodigoRecargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_codigorecargo'},
		{'csv_column_name': 'SUMEX_ImporteRecargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_importerecargo'},
		{'csv_column_name': 'SUMEX_PorRecargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_porrecargo'},
		{'csv_column_name': 'PagoInmediato', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_pagoinmediato'},
		{'csv_column_name': 'StatusWF', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_statuswf'}
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

		nombre_partner = file_csv_content_row['nombre']
		nombre_partner_company = file_csv_content_row['razonsocial']
		ciudad = self._get_ciudad(file_csv_content_row, 'municipio')
		cif = self._get_cif(file_csv_content_row, 'cifeuropeo')
		country = self._get_country(file_csv_content_row['nacion'])
		state = self._get_state(country, file_csv_content_row['colamunicipio'])
		cp = self._get_cp(file_csv_content_row, 'codigopostal')
		msg_warning = "En esta fila la columna '%s' no contiene un valor válido, se omitirá el valor de este campo. (valor='%s')"
		warnings = []

		if not nombre_partner and not nombre_partner_company:
			return {'error': "Nombre y RazonSocial no pueden ser nulos ambos"}

		if not country:
			real_value = file_csv_content_row['nacion']
			warnings.append(msg_warning % ('nacion', real_value))

		if not state:
			real_value = file_csv_content_row['colamunicipio']
			warnings.append(msg_warning % ('colamunicipio', real_value))

		if not ciudad:
			real_value = file_csv_content_row['municipio']
			warnings.append(msg_warning % ('municipio', real_value))

		if not cp:
			real_value = file_csv_content_row['codigopostal']
			warnings.append(msg_warning % ('codigopostal', real_value))

		if not cif:
			real_value = file_csv_content_row['cifeuropeo']
			warnings.append(msg_warning % ('cifeuropeo', real_value))

		if warnings:
			return {'warning': ("; ").join(warnings)}

		return True

	def import_row(self, file_csv_content_row_num, company_id, file_csv_header, file_csv_content_row):

		"""
			Este método "import_row" es ejecutado en un bucle del objeto importador(sumex_apps_imports_csv)
			El formulario dispone de un botón de test, ese botón ejecuta este método "validate_row" sin realizar la importación, y el log recoge los resultados
			El retorno se asumirá como correcto al no ser que se retorne {'error':}
		"""

		nombre_partner = file_csv_content_row['nombre'].title()
		nombre_partner_company = file_csv_content_row['razonsocial'].title()
		if nombre_partner_company:
			nombre_partner = nombre_partner_company
		ciudad = self._get_ciudad(file_csv_content_row, 'municipio')
		vat = self._get_cif(file_csv_content_row, 'cifeuropeo')
		country = self._get_country(file_csv_content_row['nacion'])
		state = self._get_state(country, file_csv_content_row['colamunicipio'])
		cp = self._get_cp(file_csv_content_row, 'codigopostal')

		partner = self.env['sumex_apps_imports_csv_library'].sudo().get_or_create_partner(
			is_company = False,
			company_id = company_id,
			nombre = nombre_partner,
			parent_id = False,
			vat = vat,
			country_name = country,
			state_name = state,
			ciudad = ciudad,
			domicilio = '',
			cp = cp,
			telefono = '',
			mobile = '',
			email = ''
		)
		if isinstance(partner, dict) and 'error' in partner:
			return partner

		order = self._get_order(company_id, file_csv_content_row)
		if isinstance(order, dict) and 'error' in order:
			return order

		if not order:
			order = self._create_order(company_id, file_csv_content_row, partner.id)
		if isinstance(order, dict) and 'error' in order:
			return order

		dict_other_fields = {}
		result = self.env['sumex_apps_imports_csv_library'].update_extendedd_fields(order, self._import_fields, file_csv_content_row, dict_other_fields)
		if isinstance(result, dict) and 'error' in result:
			return result

		"""
		Inserciones adicionales
		"""
		list_values = {}
		changes = 0

		# forma de pago
		payment_term_name = file_csv_content_row['formadepago']
		if payment_term_name:
			payment_term = self.env['sumex_apps_imports_csv_library'].sudo().get_or_create_payment_term(payment_term_name)
			list_values['payment_term_id'] = payment_term.id
			changes += 1

		# fecha de creacion
		fecha_pedido = self._get_fecha_pedido(file_csv_content_row)
		if fecha_pedido:
			list_values['date_order'] = fecha_pedido
			changes += 1

		if changes:
			try:
				order.write(list_values)
				order._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}

		return True

	def _get_fecha_pedido(self, file_csv_content_row):
		for fecha_campo in ['fechanecesaria', 'fechaentrega', 'fechatope']:
			fecha_pedido = file_csv_content_row[fecha_campo]
			if fecha_pedido:
				fecha_pedido = self.env['sumex_apps_imports_csv_library'].get_sql_fecha(fecha_pedido)
				if fecha_pedido:
					return fecha_pedido

	def _get_order(self, company_id, file_csv_content_row):

		order_model = self.env['sale.order'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		sage_numero_pedido = file_csv_content_row['numeropedido']
		if not company_id:
			company_id = self.env.user.company_id.id
		try:
			order = order_model.search([
				('_sage_field_numeropedido', '=', sage_numero_pedido), 
				('company_id', '=', company_id)
			], limit = 1)
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		return order

	def _create_order(self, company_id, file_csv_content_row, partner_id):

		order_model = self.env['sale.order'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		if not company_id:
			company_id = self.env.user.company_id.id
		try:
			order = order_model.create({
				'company_id': company_id,
				'partner_id': partner_id,
				# pricelist_id
			})
			order_model._cr.commit()
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		return order

	def _get_country(self, country_name):

		return self.env['sumex_apps_imports_csv_library'].sudo().get_country(country_name)

	def _get_state(self, country, state_name):

		return self.env['sumex_apps_imports_csv_library'].sudo().get_state(country, state_name)

	def _get_cp(self, file_csv_content_row, fieldname):

		return self.env['sumex_apps_imports_csv_import_sage_clientes'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True).get_cp(file_csv_content_row, fieldname)

	def _get_ciudad(self, file_csv_content_row, fieldname):

		return self.env['sumex_apps_imports_csv_import_sage_clientes'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True).get_ciudad(file_csv_content_row, fieldname)

	def _get_cif(self, file_csv_content_row, fieldname):

		return self.env['sumex_apps_imports_csv_import_sage_clientes'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True).get_cif(file_csv_content_row, fieldname)

