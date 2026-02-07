from parser.base import BaseParser
from datetime import date
from common.AppException import AppException


class OpcionesContratoParser(BaseParser):
    def __init__(self, args=None):
        super().__init__(args=args)

    def parse_args_get_options_chain(self, args=None):
        self.params.set_params(args=args)

        param_cod_symbol = self.params.parse(nombre_param="cod_symbol", requerido=True)
        param_fch_expiracion = self.params.parse(nombre_param="fch_expiracion", datatype=date, vacio_es_nulo=True)
        param_imp_ejercicio = self.params.parse(nombre_param="imp_ejercicio", datatype=float, vacio_es_nulo=True)

        params = {
            "cod_symbol": param_cod_symbol.valor,
            "fch_expiracion": param_fch_expiracion.valor,
            "imp_ejercicio": param_imp_ejercicio.valor
        }

        return params

    def parse_args_get_contratos(self, args=None):
        self.params.set_params(args=args)

        param_id_contrato_opcion = self.params.parse(nombre_param="id_contrato_opcion", datatype=int, vacio_es_nulo=True)
        param_cod_symbol = self.params.parse(nombre_param="cod_symbol", vacio_es_nulo=True)
        param_sentidos = self.params.parse(nombre_param="sentidos")
        param_imp_ejercicio = self.params.parse(nombre_param="imp_ejercicio", datatype=float)
        param_fch_expiracion = self.params.parse(nombre_param="fch_expiracion", datatype=date)

        if len(list(param_sentidos.valor)) > 0:
            if "call" not in param_sentidos.valor and "put" not in param_sentidos.valor:
                raise AppException(msg="No se ha indicado un tipo de opcion valido")

        params = {
            "id_contrato_opcion": param_id_contrato_opcion.valor,
            "cod_symbol": param_cod_symbol.valor,
            "sentidos": param_sentidos.valor,
            "fch_expiracion": param_fch_expiracion.valor,
            "imp_ejercicio": param_imp_ejercicio.valor
        }

        return params


class SymbolLoaderParser(BaseParser):
    def __init__(self, args=None):
        super().__init__(args=args)

    def parse_args_load(self, args=None):
        self.params.set_params(args=args)
        param_cod_symbol = self.params.parse("cod_symbol", requerido=True)
        param_fch_expiracion = self.params.parse("fch_expiracion", requerido=True, datatype=date)
        params = {
            "cod_symbol": param_cod_symbol.valor,
            "fch_expiracion": param_fch_expiracion.valor
        }
        return params



