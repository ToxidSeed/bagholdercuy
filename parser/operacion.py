from common.AppException import AppException
from reader.transaccion import TransaccionReader
from datetime import date, timedelta, datetime
from domain.semana import CodigoSemana
from domain.mes import CodigoMes
from domain.anyo import Anyo

from parser.base import BaseParser

class OperacionParser:
    def parse_args_get_rentabilidad_diaria(args={}):
        num_dias_profundidad_default = 31
        num_dias_profundidad_max = 365
        td_default = timedelta(days=31)
        td_max = timedelta(days=365)

        id_cuenta = args.get("id_cuenta")
        if id_cuenta in [None,""]:
            raise AppException(msg="no se ha indicado el identificador de la cuenta")
        
        id_cuenta = int(id_cuenta)
        args["id_cuenta"] = id_cuenta

        fch_hasta = BaseParser.parse_date(args.get("fch_hasta")) 
        if fch_hasta is None:
            fch_hasta = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)

        if fch_hasta is None:
            fch_hasta = date.today()        
        args["fch_hasta"] = fch_hasta

        fch_desde = BaseParser.parse_date(args.get("fch_desde"))
        if fch_desde is None:
            fch_desde = fch_hasta - td_default
        args["fch_desde"] = fch_desde        
        return args

    def parse_args_get_rentabilidad_mensual(args={}):
        
        #id_cuenta            
        id_cuenta = args.get("id_cuenta")
        id_cuenta = BaseParser.parse_id_cuenta(id_cuenta)
        if id_cuenta is None:
            raise AppException(msg="No se ha indicado el identificador de la cuenta")
        args["id_cuenta"] = id_cuenta

        #cod_mes_hasta
        cod_mes_hasta =  CodigoMes(args.get("cod_mes_hasta"))
        if cod_mes_hasta.value is None:

            fch_ultdia_rentabilidad = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)
            cod_mes_hasta = CodigoMes(fch_ultdia_rentabilidad)

            if cod_mes_hasta.value is None:

                cod_mes_hasta = CodigoMes(value=date.today())

        args["cod_mes_hasta"] = cod_mes_hasta.value

        #cod_mes_desde
        cod_mes_desde = CodigoMes(args.get("cod_mes_desde"))
        if cod_mes_desde.value is None:
            cod_mes_desde = cod_mes_hasta.restar(12)
            
        args["cod_mes_desde"] = cod_mes_desde.value

        #flg_ascendente 
        flg_ascendente = BaseParser.parse_boolean(args.get("flg_ascendente"))
        args["flg_ascendente"] = flg_ascendente

        return args

    def parse_args_get_rentabilidad_anual(args={}):
        num_max_anyos = 5

        #id_cuenta
        id_cuenta = args.get("id_cuenta")
        id_cuenta = BaseParser.parse_int(id_cuenta)
        if id_cuenta is None:
            raise AppException(msg="No se ha indicado id_cuenta")
        
        #anyo hasta
        num_anyo_hasta = Anyo(args.get("num_anyo_hasta"))
        if num_anyo_hasta.value is None:
            fch_ult_rentabilidad = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)            
            anyo_hasta = date.today().year() if fch_ult_rentabilidad is None else fch_ult_rentabilidad.year
            num_anyo_hasta = Anyo(anyo_hasta)
        
        args["num_anyo_hasta"] = num_anyo_hasta.value

        #anyo desde
        num_anyo_desde = Anyo(args.get("num_anyo_desde"))
        args["num_anyo_desde"] = num_anyo_desde.value

        if num_anyo_desde.value is None:
            args["num_anyo_desde"] = num_anyo_hasta.value - num_max_anyos

        #orden
        orden_resultados = BaseParser.parse_orden_resultados(args.get("orden_resultados"))
        args["orden_resultados"] = orden_resultados

        return args
    
    def parse_args_get_rentabilidad_semanal(args={}):        

        id_cuenta = args.get("id_cuenta")
        id_cuenta = BaseParser.parse_int(id_cuenta)
        if id_cuenta is None:
            raise AppException(msg="No se ha indicado id_cuenta")
        
        cod_semana_hasta = CodigoSemana(args.get("cod_semana_hasta"))

        if cod_semana_hasta.value is None:
            fch_ult_rentabilidad = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)
            cod_semana_hasta = CodigoSemana(value=fch_ult_rentabilidad)

            if cod_semana_hasta.value is None:
                cod_semana_hasta = CodigoSemana(value=date.today())

        args["cod_semana_hasta"] = cod_semana_hasta.value

        cod_semana_desde = CodigoSemana(args.get("cod_semana_desde"))
        if cod_semana_desde.value is None:
            cod_semana_desde = cod_semana_hasta.restar(num_semanas=52)

        args["cod_semana_desde"] = cod_semana_desde.value

        flg_ascendente = BaseParser.parse_boolean(args.get("flg_ascendente"))        
        args["flg_ascendente"] = flg_ascendente

        return args
