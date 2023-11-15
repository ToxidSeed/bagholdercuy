from model.configuracionalerta import ConfiguracionAlertaModel
from parser.base import BaseParser
from common.AppException import AppException
from config.negocio import TIPO_VARIACION_EJERCICIO

from reader.symbol import SymbolReader
from reader.monitoreo import MonitoreoReader

class ConfiguracionAlertaParser:        
    
    def parse_args_registrar(self, args={}):
        parser = BaseParser(args=args)
        symbol_reader = SymbolReader()        
        
        flg_compras = BaseParser.parse_boolean(args.get("flg_compras"))
        flg_ventas = BaseParser.parse_boolean(args.get("flg_ventas"))

        if flg_compras is False or flg_ventas is False:
            raise AppException(msg="Debe seleccionar al menos una opcion para generar, compras o ventas")
        
        configuracion = ConfiguracionAlertaModel(
            flg_compras = flg_compras,
            flg_ventas = flg_ventas
        )        

        id_monitoreo = parser.get("id_monitoreo", datatype=int)
        configuracion.id_monitoreo = id_monitoreo

        id_cuenta = parser.get("id_cuenta", datatype=int)
        configuracion.id_cuenta = id_cuenta
    
        if id_monitoreo is None and id_cuenta is None:
            raise AppException(msg="Se debe enviar el identificador del monitoreo o el identificador de la cuenta")

        cod_symbol = parser.get("cod_symbol", requerido=True)    
        symbol = symbol_reader.get(cod_symbol=cod_symbol, not_found_error=True)
        configuracion.id_symbol = symbol.id
                        
        cod_tipo_variacion_titulo = parser.get("cod_tipo_variacion_titulo", requerido=True)        
        configuracion.cod_tipo_variacion_titulo = cod_tipo_variacion_titulo

        ctd_variacion_titulo = parser.get("ctd_variacion_titulo", requerido=True, datatype=int)        
        configuracion.ctd_variacion_titulo = ctd_variacion_titulo

        ctd_ciclos = parser.get("ctd_ciclos", requerido=True, datatype=int)
        configuracion.ctd_ciclos = ctd_ciclos
        
        imp_inicio_ciclos = parser.get("imp_inicio_ciclos", requerido=True, datatype=float)
        configuracion.imp_inicio_ciclos = imp_inicio_ciclos        

        #flg_opciones = args.get("flg_opciones")
        #         
        cod_tipo_variacion_ejercicio = parser.get("cod_tipo_variacion_ejercicio", requerido=True)
        configuracion.cod_tipo_variacion_ejercicio = cod_tipo_variacion_ejercicio

        if cod_tipo_variacion_ejercicio == TIPO_VARIACION_EJERCICIO.COD_IMPORTE_FIJO:

            imp_fijo_ejercicio_call = parser.get("imp_fijo_ejercicio_call", datatype=float)
            if imp_fijo_ejercicio_call is None:
                raise AppException(msg="Se ha seleccionado que el importe del ejercicio es fijo pero no se ha enviado imp_fijo_ejercicio_call")
                        
            imp_fijo_ejercicio_put = parser.get("imp_fijo_ejercicio_put", datatype=float)
            if imp_fijo_ejercicio_put is None:
                raise AppException(msg="Se ha seleccionado que el importe del ejercicio es fijo pero no se ha enviado imp_fijo_ejercicio_put")
            
            configuracion.imp_fijo_ejercicio_call = imp_fijo_ejercicio_call
            configuracion.imp_fijo_ejercicio_put = imp_fijo_ejercicio_put
            configuracion.imp_variacion_subyacente_call = None
            configuracion.imp_variacion_subyacente_put = None
        
        if cod_tipo_variacion_ejercicio == TIPO_VARIACION_EJERCICIO.COD_VARIACION_SUBYACENTE:            

            imp_variacion_subyacente_call = parser.get("imp_variacion_subyacente_call", datatype=float)
            if imp_variacion_subyacente_call is None:
                raise AppException(msg="Se ha seleccionado que el importe del ejercicio es variacion del subyacente pero no se ha enviado imp_variacion_subyacente_call")

            imp_variacion_subyacente_put = parser.get("imp_variacion_subyacente_put", datatype=float)
            if imp_variacion_subyacente_put is None:
                raise AppException(msg="Se ha seleccionado que el importe del ejercicio es variacion del subyacente pero no se ha enviado imp_variacion_subyacente_put")
            
            configuracion.imp_fijo_ejercicio_call = None
            configuracion.imp_fijo_ejercicio_put = None
            configuracion.imp_variacion_subyacente_call = imp_variacion_subyacente_call
            configuracion.imp_variacion_subyacente_put = imp_variacion_subyacente_put

        num_dias_expiracion_call = parser.get("num_dias_expiracion_call", requerido=True)        
        configuracion.num_dias_expiracion_call = num_dias_expiracion_call

        num_dias_expiracion_put = parser.get("num_dias_expiracion_put", requerido=True)
        configuracion.num_dias_expiracion_put = num_dias_expiracion_put

        return configuracion        

    def parse_args_get_configuracion_alerta(self, args={}):
        parser = BaseParser(args=args)
        id_monitoreo = parser.get("id_monitoreo",requerido=True, datatype=int)
        args["id_monitoreo"] = id_monitoreo
        return args