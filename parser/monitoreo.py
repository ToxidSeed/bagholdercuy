from parser.base import BaseParser
from model.monitoreo import MonitoreoModel
from common.AppException import AppException


class MonitoreoParser:
    def parse_args_get_lista_seguimiento(self, args={}):
        parser = BaseParser(args=args)

        requeridos = {
            "id_cuenta": parser.get("id_cuenta", requerido=True, datatype=int)
        }

        opcionales = {}
        if "id_symbol" in args and args.get("id_symbol") is not None:
            opcionales["id_symbol"] = parser.get("id_symbol", datatype=int)
        if "id_contrato_opcion" in args and args.get("id_contrato_opcion") is not None:
            opcionales["id_contrato_opcion"] = parser.get("id_contrato_opcion", datatype=int)
        if "id_symbol_type" in args and args.get("id_symbol_type") is not None:
            opcionales["id_symbol_type"] = parser.get("id_symbol_type", datatype=int)

        return requeridos, opcionales

    def parse_args_registrar(self, args={}):
        parser = BaseParser(args=args)

        monitoreo = MonitoreoModel()
        monitoreo.id_cuenta = parser.get("id_cuenta", requerido=True, datatype=int)

        id_symbol = parser.get("id_symbol", requerido=False, datatype=int)
        id_symbol_subyacente = parser.get("id_symbol_subyacente", requerido=False, datatype=int)
        id_contrato_opcion = parser.get("id_contrato_opcion", requerido=False, datatype=int)
        id_symbol_type = parser.get("id_symbol_type", requerido=False, datatype=int)

        cod_symbol = parser.get("cod_symbol", requerido=False, datatype=str)
        tipo_opcion = parser.get("tipo_opcion", requerido=False, datatype=str)
        fch_vencimiento = args.get("fch_vencimiento")
        imp_strike = (
            parser.get("imp_strike", requerido=False, datatype=float)
            if ("imp_strike" in args and args.get("imp_strike") is not None)
            else None
        )
        tam_contrato = (
            parser.get("tam_contrato", requerido=False, datatype=int)
            if ("tam_contrato" in args and args.get("tam_contrato") is not None)
            else 100
        )
        cod_moneda = parser.get("cod_moneda", requerido=False, datatype=str)
        descripcion = parser.get("descripcion", requerido=False, datatype=str)

        # Si no se envió id_contrato_opcion pero sí se enviaron datos de un contrato de opción
        if id_contrato_opcion is None and (
            id_symbol_type == 2
            or (tipo_opcion and str(tipo_opcion).upper() in ("CALL", "PUT"))
            or (cod_symbol and (tipo_opcion or fch_vencimiento or imp_strike))
        ):
            subyacente_id = id_symbol_subyacente or id_symbol
            monitoreo.contrato_opcion_data = {
                "id_symbol_subyacente": subyacente_id,
                "id_symbol": subyacente_id,
                "cod_symbol": cod_symbol,
                "tipo_opcion": tipo_opcion,
                "fch_vencimiento": fch_vencimiento,
                "imp_strike": imp_strike,
                "tam_contrato": tam_contrato or 100,
                "cod_moneda": cod_moneda or "USD",
                "descripcion": descripcion,
            }
            monitoreo.id_symbol_type = 2
            monitoreo.id_symbol = None
        else:
            if id_symbol is None and id_contrato_opcion is None:
                raise AppException(msg="Debe enviar 'id_symbol' o 'id_contrato_opcion'")

            monitoreo.id_symbol = id_symbol
            monitoreo.id_contrato_opcion = id_contrato_opcion
            monitoreo.id_symbol_type = id_symbol_type

        return monitoreo

