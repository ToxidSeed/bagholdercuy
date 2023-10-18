from common.AppException import AppException
from reader.transaccion import TransaccionReader
from datetime import date, timedelta, datetime
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
        td_max = timedelta(days=365)

        id_cuenta = args.get("id_cuenta")
        id_cuenta = BaseParser.parse_id_cuenta(id_cuenta)
        if id_cuenta is None:
            raise AppException(msg="No se ha indicado el identificador de la cuenta")
        args["id_cuenta"] = id_cuenta

        cod_mes_hasta = args.get("cod_mes_hasta")
        if cod_mes_hasta in [None,""]:
            fch_ultdia_rentabilidad = TransaccionReader.get_ultdia_con_rentabilidad(id_cuenta=id_cuenta)
            fch_hasta = fch_ultdia_rentabilidad if fch_ultdia_rentabilidad is not None else date.today()
            cod_mes_hasta = BaseParser.parse_int(fch_hasta.strftime("%Y%m"))
        else:
            cod_mes_hasta = cod_mes_hasta.replace("/")
            cod_mes_hasta = BaseParser.parse_int(cod_mes_hasta)
        args["cod_mes_hasta"] = cod_mes_hasta

        cod_mes_desde = args.get("cod_mes_desde")
        if cod_mes_desde in [None,""]:
            fch_hasta = datetime.strptime(str(cod_mes_hasta),"%Y%m").date()
            fch_desde = fch_hasta - td_max
            cod_mes_desde = BaseParser.parse_int(fch_desde.strftime("%Y%m"))
        else:
            cod_mes_desde = cod_mes_desde.replace("/")
            cod_mes_desde = BaseParser.parse_int(cod_mes_desde)
        args["cod_mes_desde"] = cod_mes_desde

        return args


        