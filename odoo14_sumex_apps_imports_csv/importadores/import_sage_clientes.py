# -*- coding: utf-8 -*-

"""
	ESTE IMPORTADOR USA CAMPOS EXTENDIDOS EN EL MODULO 'sumex_apps_sage_inherits'
"""

from odoo import models


class sumex_apps_imports_csv_import_sage_clientes(models.AbstractModel):

	_description = "modulo importador"

	_import_fields = [

		# Campos que participan en la importacion del modelo
		{'csv_column_name': 'RazonSocial', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_razonsocial'},
		{'csv_column_name': 'Nombre', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nombre'},
		{'csv_column_name': 'CifEuropeo', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cifeuropeo'},
		{'csv_column_name': 'Municipio', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_municipio'},
		{'csv_column_name': 'CodigoPostal', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigopostal'},
		{'csv_column_name': 'Nacion', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nacion'},
		{'csv_column_name': 'ColaMunicipio', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_colamunicipio'},
		{'csv_column_name': 'Domicilio', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domicilio'},
		{'csv_column_name': 'Telefono', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_telefono'},
		{'csv_column_name': 'Telefono2', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_telefono2'},
		{'csv_column_name': 'Email1', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_email1'},
		{'csv_column_name': 'FechaAlta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaalta'},
		{'csv_column_name': 'FormadePago', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_formadepago'},
		{'csv_column_name': 'CodigoBanco', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigobanco'},
		{'csv_column_name': 'IBAN', 'required_header_field': True, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_iban'},

		# Campos que NO participan en la importacion del modelo, pero se incluyen a nivel informativo
		{'csv_column_name': 'CodigoMunicipio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigomunicipio'},
		{'csv_column_name': 'DomicilioEnvio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domicilioenvio'},
		{'csv_column_name': 'DomicilioFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domiciliofactura'},
		{'csv_column_name': 'DomicilioRecibo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domiciliorecibo'},
		{'csv_column_name': 'CodigoAgencia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoagencia'},
		{'csv_column_name': 'DC', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_dc'},
		{'csv_column_name': 'CCC', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_ccc'},
		{'csv_column_name': 'Provincia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_provincia'},
		{'csv_column_name': 'CodigoSigla', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosigla'},
		{'csv_column_name': 'Telefono3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_telefono3'},
		{'csv_column_name': 'CodigoProvincia', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoprovincia'},
		{'csv_column_name': 'CodigoNacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigonacion'},
		{'csv_column_name': 'SiglaNacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_siglanacion'},
		{'csv_column_name': 'IdDelegacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_iddelegacion'},
		{'csv_column_name': 'CodigoEmpresa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoempresa'},
		{'csv_column_name': 'CodigoCliente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocliente'},
		{'csv_column_name': 'CifDni', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cifdni'},
		{'csv_column_name': 'CodigoProveedor', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoproveedor'},
		{'csv_column_name': 'CodigoContable', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocontable'},
		{'csv_column_name': 'CodigoCadena_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocadena'},
		{'csv_column_name': 'CodigoCategoriaCliente_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocategoriacliente'},
		{'csv_column_name': 'CodigoDefinicion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodefinicion'},
		{'csv_column_name': 'ReferenciaEdi_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_referenciaedi'},
		{'csv_column_name': 'ActivarLogicNet', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_activarlogicnet'},
		{'csv_column_name': 'UsuarioLogicNet', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_usuariologicnet'},
		{'csv_column_name': 'ContraseñaLogicNet', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_contraseñalogicnet'},
		{'csv_column_name': 'CodigoExportacion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoexportacion'},
		{'csv_column_name': 'CondicionExportacion_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_condicionexportacion'},
		{'csv_column_name': 'CodigoDivisa', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodivisa'},
		{'csv_column_name': 'CodigoCondiciones', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocondiciones'},
		{'csv_column_name': 'CodigoIdioma_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoidioma'},
		{'csv_column_name': 'RazonSocial2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_razonsocial2'},
		{'csv_column_name': 'Domicilio2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domicilio2'},
		{'csv_column_name': 'Actividad', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_actividad'},
		{'csv_column_name': 'TipoCliente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipocliente'},
		{'csv_column_name': 'CodigoSector_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosector'},
		{'csv_column_name': 'Cargo1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cargo1'},
		{'csv_column_name': 'Nombre1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nombre1'},
		{'csv_column_name': 'Cargo2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cargo2'},
		{'csv_column_name': 'Nombre2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nombre2'},
		{'csv_column_name': 'Cargo3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cargo3'},
		{'csv_column_name': 'Nombre3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_nombre3'},
		{'csv_column_name': 'BloqueoPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_bloqueopedido'},
		{'csv_column_name': 'BloqueoAlbaran', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_bloqueoalbaran'},
		{'csv_column_name': 'CodigoCanal', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocanal'},
		{'csv_column_name': 'CodigoProyecto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoproyecto'},
		{'csv_column_name': 'CodigoSeccion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoseccion'},
		{'csv_column_name': 'CodigoDepartamento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodepartamento'},
		{'csv_column_name': 'TarifaPrecio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tarifaprecio'},
		{'csv_column_name': 'TarifaDescuento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tarifadescuento'},
		{'csv_column_name': 'MantenerCambio_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mantenercambio'},
		{'csv_column_name': 'IndicadorIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_indicadoriva'},
		{'csv_column_name': 'GrupoIva', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_grupoiva'},
		{'csv_column_name': '%Descuento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_descuento'},
		{'csv_column_name': '%ProntoPago', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_prontopago'},
		{'csv_column_name': '%Retencion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_retencion'},
		{'csv_column_name': '%Financiacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_financiacion'},
		{'csv_column_name': '%Rappel', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_rappel'},
		{'csv_column_name': 'CodigoComisionista', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista'},
		{'csv_column_name': 'CodigoComisionista2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista2'},
		{'csv_column_name': 'CodigoComisionista3_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista3'},
		{'csv_column_name': 'CodigoComisionista4_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocomisionista4'},
		{'csv_column_name': 'CodigoJefeZona_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigojefezona'},
		{'csv_column_name': '%Comision', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision'},
		{'csv_column_name': '%Comision2_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision2'},
		{'csv_column_name': '%Comision3_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision3'},
		{'csv_column_name': '%Comision4_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_percent_comision4'},
		{'csv_column_name': 'ComisionSobreZona%_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comisionsobrezona_percent'},
		{'csv_column_name': 'CodigoZona', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigozona'},
		{'csv_column_name': 'CodigoRuta_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoruta'},
		{'csv_column_name': 'CodigoTransportista', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotransportista'},
		{'csv_column_name': 'TipoPortes', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tipoportes'},
		{'csv_column_name': 'ObservacionesCliente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_observacionescliente'},
		{'csv_column_name': 'Comentarios', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comentarios'},
		{'csv_column_name': 'PeriodicidadFacturas', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_periodicidadfacturas'},
		{'csv_column_name': 'AgruparAlbaranes', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_agruparalbaranes'},
		{'csv_column_name': 'AgruparAbonos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_agruparabonos'},
		{'csv_column_name': 'AlbaranValorado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_albaranvalorado'},
		{'csv_column_name': 'ServirCompleto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_servircompleto'},
		{'csv_column_name': 'MascaraOferta_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mascaraoferta'},
		{'csv_column_name': 'MascaraPedido_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mascarapedido'},
		{'csv_column_name': 'MascaraAlbaran_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mascaraalbaran'},
		{'csv_column_name': 'MascaraFactura_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mascarafactura'},
		{'csv_column_name': 'MascaraRecibo_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_mascararecibo'},
		{'csv_column_name': 'SerieOferta_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_serieoferta'},
		{'csv_column_name': 'SeriePedido_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_seriepedido'},
		{'csv_column_name': 'SerieAlbaran_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_seriealbaran'},
		{'csv_column_name': 'CopiasAlbaran', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_copiasalbaran'},
		{'csv_column_name': 'CopiasFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_copiasfactura'},
		{'csv_column_name': 'CopiasOferta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_copiasoferta'},
		{'csv_column_name': 'CopiasPedido', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_copiaspedido'},
		{'csv_column_name': 'ViaPublica', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_viapublica'},
		{'csv_column_name': 'Numero1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numero1'},
		{'csv_column_name': 'Numero2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_numero2'},
		{'csv_column_name': 'Escalera', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_escalera'},
		{'csv_column_name': 'Piso', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_piso'},
		{'csv_column_name': 'Puerta', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_puerta'},
		{'csv_column_name': 'Letra', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_letra'},
		{'csv_column_name': 'Fax', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fax'},
		{'csv_column_name': 'Email2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_email2'},
		{'csv_column_name': 'BajaEmpresaLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_bajaempresalc'},
		{'csv_column_name': 'FechaBajaLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechabajalc'},
		{'csv_column_name': 'CodigoMotivoBajaClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigomotivobajaclientelc'},
		{'csv_column_name': 'ComercialAsignadoLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comercialasignadolc'},
		{'csv_column_name': 'CodigoTipoClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipoclientelc'},
		{'csv_column_name': 'FechaUltimaAccionLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaultimaaccionlc'},
		{'csv_column_name': 'PersonaClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_personaclientelc'},
		{'csv_column_name': 'CodigoActividadLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoactividadlc'},
		{'csv_column_name': 'CodigoSubActividadLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigosubactividadlc'},
		{'csv_column_name': 'CodigoCargo1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocargo1'},
		{'csv_column_name': 'CodigoCargo2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocargo2'},
		{'csv_column_name': 'CodigoCargo3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocargo3'},
		{'csv_column_name': 'CodigoDivisionLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigodivisionlc'},
		{'csv_column_name': 'CodigoAmbitoClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoambitoclientelc'},
		{'csv_column_name': 'CodigoClaseClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoclaseclientelc'},
		{'csv_column_name': 'CodigoGrupoClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigogrupoclientelc'},
		{'csv_column_name': 'IdDelegacionCentralLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_iddelegacioncentrallc'},
		{'csv_column_name': 'HorarioDomicilioLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_horariodomiciliolc'},
		{'csv_column_name': 'CodigoColectivoClienteLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocolectivoclientelc'},
		{'csv_column_name': 'CodigoTipoPrimerContactoLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotipoprimercontactolc'},
		{'csv_column_name': 'FechaProximaAccionLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaproximaaccionlc'},
		{'csv_column_name': 'AutorizacionLOPDLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_autorizacionlopdlc'},
		{'csv_column_name': 'FechaAutorizacionLOPDLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaautorizacionlopdlc'},
		{'csv_column_name': 'ExcluirPorLOPDLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_excluirporlopdlc'},
		{'csv_column_name': 'FechaExcluirPorLOPDLc', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechaexcluirporlopdlc'},
		{'csv_column_name': 'RiesgoMaximo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_riesgomaximo'},
		{'csv_column_name': 'ReferenciadelProveedor', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_referenciadelproveedor'},
		{'csv_column_name': 'DestinoEdi', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_destinoedi'},
		{'csv_column_name': 'CodigoNaturaleza', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigonaturaleza'},
		{'csv_column_name': 'CodigoTransporte', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigotransporte'},
		{'csv_column_name': 'CodigoPuerto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigopuerto'},
		{'csv_column_name': 'CodigoRegimenEstadistico', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoregimenestadistico'},
		{'csv_column_name': 'EnvioEFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_envioefactura'},
		{'csv_column_name': 'EmailEnvioEFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_emailenvioefactura'},
		{'csv_column_name': 'GuiaXMLEFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_guiaxmlefactura'},
		{'csv_column_name': 'DepartamentoEdi', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_departamentoedi'},
		{'csv_column_name': 'SabadosFestivos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sabadosfestivos'},
		{'csv_column_name': 'DomingosFestivos', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_domingosfestivos'},
		{'csv_column_name': 'FormatoEFactura', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_formatoefactura'},
		{'csv_column_name': 'NoTraspasarSFA', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_notraspasarsfa'},
		{'csv_column_name': 'CuentaProvision', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cuentaprovision'},
		{'csv_column_name': 'LiquidacionEnDespacho', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_liquidacionendespacho'},
		{'csv_column_name': 'CodigoContableANT_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigocontableant'},
		{'csv_column_name': 'CuentaProvisionANT_', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cuentaprovisionant'},
		{'csv_column_name': 'FormatoEnvio', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_formatoenvio'},
		{'csv_column_name': 'PuntosSR', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_puntossr'},
		{'csv_column_name': 'TarjetaSR', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_tarjetasr'},
		{'csv_column_name': 'FechaNacimiento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechanacimiento'},
		{'csv_column_name': 'PersonaAsignada', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_personaasignada'},
		{'csv_column_name': 'AsesorNominaLW', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_asesornominalw'},
		{'csv_column_name': 'EmpresaNominaLWin', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_empresanominalwin'},
		{'csv_column_name': 'CodigoEmpleado', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_codigoempleado'},
		{'csv_column_name': 'IdCliente', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_idcliente'},
		{'csv_column_name': 'PublicarGCRM', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_publicargcrm'},
		{'csv_column_name': 'ReferenciaMandato', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_referenciamandato'},
		{'csv_column_name': 'FechaModificacion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_fechamodificacion'},
		{'csv_column_name': 'sumex_referenciaedipagador', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_referenciaedipagador'},
		{'csv_column_name': 'Sumex_ClienteRiesgo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_clienteriesgo'},
		{'csv_column_name': 'Sumex_FechaAltaRiesgo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_fechaaltariesgo'},
		{'csv_column_name': 'Sumex_RiesgoFechaH1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_riesgofechah1'},
		{'csv_column_name': 'Sumex_RiesgoFechaH2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_riesgofechah2'},
		{'csv_column_name': 'Sumex_RiesgoFechaH3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_riesgofechah3'},
		{'csv_column_name': 'Sumex_RiesgoFechaH4', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_riesgofechah4'},
		{'csv_column_name': 'Sumex_RiesgoH1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_riesgoh1'},
		{'csv_column_name': 'Sumex_RiesgoH2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_riesgoh2'},
		{'csv_column_name': 'Sumex_RiesgoH3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_riesgoh3'},
		{'csv_column_name': 'Sumex_RiesgoH4', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_riesgoh4'},
		{'csv_column_name': 'SUMEX_ObservacionesRiesgo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_observacionesriesgo'},
		{'csv_column_name': 'S_AplicarBaremosT', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_s_aplicarbaremost'},
		{'csv_column_name': 'Social1', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_social1'},
		{'csv_column_name': 'Social2', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_social2'},
		{'csv_column_name': 'Social3', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_social3'},
		{'csv_column_name': 'Social4', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_social4'},
		{'csv_column_name': 'TelefonoAccion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_telefonoaccion'},
		{'csv_column_name': 'Telefono2Accion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_telefono2accion'},
		{'csv_column_name': 'Telefono3Accion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_telefono3accion'},
		{'csv_column_name': 'Social1Accion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_social1accion'},
		{'csv_column_name': 'Social2Accion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_social2accion'},
		{'csv_column_name': 'Social3Accion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_social3accion'},
		{'csv_column_name': 'Social4Accion', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_social4accion'},
		{'csv_column_name': 'SUMEX_CodigoRecargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_codigorecargo'},
		{'csv_column_name': 'SUMEX_ImporteRecargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_importerecargo'},
		{'csv_column_name': 'SUMEX_PorRecargo', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_sumex_porrecargo'},
		{'csv_column_name': 'CuentaGasto', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_cuentagasto'},
		{'csv_column_name': 'ComentarioAsiento', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_comentarioasiento'},
		{'csv_column_name': 'DIRe', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_dire'},
		{'csv_column_name': 'IdClientePago', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_idclientepago'},
		{'csv_column_name': 'StatusWF', 'required_header_field': False, 'required_value': False, 'save_as_inherit_fieldname': '_sage_field_statuswf'},
	]

	def get_import_fields(self):

		return self._import_fields

	def hook_pre_process(self, company_id, file_csv_header, file_csv_content):

		# model = self.env['product.template'].sudo()
		# rows=model.search([('_created_from_sumex_apps_imports_csv', '=', True)])
		# rows.write({'_created_from_sumex_apps_imports_csv_of_sage': True})

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
		ciudad = self.get_ciudad(file_csv_content_row, 'municipio')
		vat = self.get_cif(file_csv_content_row, 'cifeuropeo')
		if isinstance(vat, dict) and 'error' in vat:
			vat = ''
		country = self.env['sumex_apps_imports_csv_library'].sudo().get_country(file_csv_content_row['nacion'])
		state = self.env['sumex_apps_imports_csv_library'].sudo().get_state(country, file_csv_content_row['colamunicipio'])
		cp = self.get_cp(file_csv_content_row, 'codigopostal')
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

		if not vat:
			real_value = file_csv_content_row['cifeuropeo']
			warnings.append(msg_warning % ('cifeuropeo', real_value))

		codigobanco = file_csv_content_row['codigobanco']
		iban = file_csv_content_row['iban']
		if not codigobanco or not iban:
			return

		bank_list_item = self._get_bank_list_item(codigobanco)
		if not bank_list_item:
			warnings.append("No se ha encontrado un banco con el código '%s', se omitirá este campo" % codigobanco)

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

		# if "Blazquez Martin, Antonio" in nombre_partner:
		# 	a = 15  # 'Auto Repuestos Blazquez' # 11967

		# if "Blazquez Martin, Antonio" in nombre_partner_company:
		# 	a = 15   # 'Blazquez Martin, Antonio' # 11326			OK

		if nombre_partner_company and not nombre_partner:
			nombre_partner = nombre_partner_company
			nombre_partner_company = ''
		if nombre_partner_company == nombre_partner:
			nombre_partner = nombre_partner_company
			nombre_partner_company = ''
		vat = self.get_cif(file_csv_content_row, 'cifeuropeo')
		if isinstance(vat, dict) and 'error' in vat:
			vat = ''
		ciudad = self.get_ciudad(file_csv_content_row, 'municipio')
		cp = self.get_cp(file_csv_content_row, 'codigopostal')
		domicilio = self.get_domicilio(file_csv_content_row, "domicilio")
		telefono = self.get_telefono(file_csv_content_row, "telefono")
		mobile = self.get_telefono(file_csv_content_row, "telefono2")
		email = self.get_email(file_csv_content_row, "email1")
		country_name = file_csv_content_row['nacion']
		state_name = file_csv_content_row['colamunicipio']

		partner_company_id = False
		if nombre_partner_company:
			partner_company_row = self.env['sumex_apps_imports_csv_library'].sudo().get_or_create_partner(
				is_company = True,
				company_id = company_id,
				nombre = nombre_partner_company,
				parent_id = False,
				vat = vat,
				country_name = country_name,
				state_name = state_name,
				ciudad = ciudad,
				domicilio = domicilio,
				cp = cp,
				telefono = telefono,
				mobile = mobile,
				email = email
			)
			if isinstance(partner_company_row, dict) and 'error' in partner_company_row:
				return partner_company_id
			partner_company_id = partner_company_row.id

			"""
			Inserciones adicionales para el partner_company
			"""
			result = self.set_additional_values(partner_company_row, file_csv_content_row)
			if isinstance(result, dict) and 'error' in result:
				return result

		partner = self.env['sumex_apps_imports_csv_library'].sudo().get_or_create_partner(
			is_company = False,
			company_id = company_id,
			nombre = nombre_partner,
			parent_id = partner_company_id,
			vat = vat,
			country_name = country_name,
			state_name = state_name,
			ciudad = ciudad,
			domicilio = domicilio,
			cp = cp,
			telefono = telefono,
			mobile = mobile,
			email = email
		)
		if isinstance(partner, dict) and 'error' in partner:
			return partner

		dict_other_fields = {}
		result = self.env['sumex_apps_imports_csv_library'].update_extendedd_fields(partner, self._import_fields, file_csv_content_row, dict_other_fields)
		if isinstance(result, dict) and 'error' in result:
			return result

		"""
		Inserciones adicionales al partner
		"""
		result = self.set_additional_values(partner, file_csv_content_row)
		if isinstance(result, dict) and 'error' in result:
			return result

		return True

	def set_additional_values(self, partner, file_csv_content_row):

		list_values = {}
		changes = 0

		if file_csv_content_row['bajaempresalc'] == "-1" or file_csv_content_row['bajaempresalc'] == "1":
			list_values['active'] = False
			changes += 1
		else:
			list_values['active'] = True
			changes += 1

		# forma de alta
		fecha_alta = file_csv_content_row["fechaalta"]
		fecha_alta = self.env['sumex_apps_imports_csv_library'].get_sql_fecha(fecha_alta)
		if fecha_alta:
			list_values['date'] = fecha_alta
			changes += 1

		# forma de pago
		payment_term_name = file_csv_content_row['formadepago']
		if payment_term_name:
			payment_term = self.env['sumex_apps_imports_csv_library'].sudo().get_or_create_payment_term(payment_term_name)
			list_values['property_payment_term_id'] = payment_term.id
			changes += 1

		if changes:
			try:
				partner.write(list_values)
				partner._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
		return True

	def get_ciudad(self, file_csv_content_row, fieldname):

		return file_csv_content_row[fieldname]

	def get_cp(self, file_csv_content_row, fieldname):

		return file_csv_content_row[fieldname] if fieldname in file_csv_content_row and file_csv_content_row[fieldname] and len(file_csv_content_row[fieldname]) == 5 else ''

	def get_domicilio(self, file_csv_content_row, fieldname):

		return file_csv_content_row[fieldname]

	def get_telefono(self, file_csv_content_row, fieldname):

		value = file_csv_content_row[fieldname]
		value = value.replace("(", "").replace(")", "").replace(",", "")
		return value

	def get_email(self, file_csv_content_row, fieldname):

		return file_csv_content_row[fieldname]

	def get_cif(self, file_csv_content_row, fieldname):

		value = file_csv_content_row[fieldname]
		result = self.if_valid_nif(value)
		if isinstance(result, dict) and 'error' in result:
			return result
		if not result:
			return ''
		return value

	def if_valid_nif(self, vat):

		partner_obj = self.env['res.partner'].sudo()
		try:
			vat_country, vat_number = partner_obj._split_vat(vat)
			result = partner_obj.simple_vat_check(vat_country, vat_number)
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		return result

	def _get_bank_list_item(self, bank_code):

		bank_code = int(bank_code)
		list_bank_and_codes = self._get_bank_and_codes()
		for list_bank_and_code_item in list_bank_and_codes:
			list_bank_code = int(list_bank_and_code_item['code'])
			if bank_code == list_bank_code:
				return list_bank_and_code_item
		return False

	def _get_bank_id(self, bank_list_item):

		bank_name = bank_list_item['name']
		bank_name_sanitized = bank_name.replace("'", "\\'")
		bank_mask = "%" + bank_name_sanitized + "%"
		sql = "CREATE EXTENSION IF NOT EXISTS unaccent; SELECT id FROM res_bank WHERE unaccent(lower(name)) ilike unaccent(lower(E'%s')) LIMIT 1" % (bank_mask)
		try:
			self.env.cr.execute(sql)
			row = self.env.cr.fetchall()
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			return {'error': exception_msg}
		if row:
			return row[0][0]
		return False

	def _set_partner_account_bank(self, partner, file_csv_content_row):

		codigobanco = file_csv_content_row['codigobanco']
		iban = file_csv_content_row['iban']
		if not codigobanco or not iban:
			return

		bank_list_item = self._get_bank_list_item(codigobanco)
		if not bank_list_item:
			return

		bank_id = self._get_bank_id(bank_list_item)
		if not bank_id:
			bank_name = bank_list_item['name']
			bank_bic = bank_list_item['bic']
			model_bank = self.env['res.bank'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
			try:
				bank = model_bank.create({
					'name': bank_name,
					'bic': bank_bic
				})
				bank._cr.commit()
			except Exception as e:
				exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
				return {'error': exception_msg}
			bank_id = bank.id

		model_partner_bank = self.env['res.partner.bank'].sudo().with_context(from_import_csv=True, mail_create_nosubscribe=True, tracking_disable=True)
		vals = model_partner_bank.search([
			('acc_number', '=', iban),
		])
		if vals:
			return
		try:
			partner_bank = model_partner_bank.create({
				'bank_id': bank_id,
				'acc_number': iban,
				'partner_id': partner.id,
				'acc_type': 'bank'
			})
			partner_bank._cr.commit()
		except Exception as e:
			exception_msg = self.env['sumex_apps_imports_csv_library'].rollback_and_get_exception_msg(str(e))
			self._cr.rollback()
			return {'error': exception_msg}

	def _get_bank_and_codes(self):

		from .sage_bank_codes import get_bank_codes

		return get_bank_codes()
