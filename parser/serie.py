from parser.base import BaseParser
from common.AppException import AppException
from datetime import date, timedelta
import json


class SerieControllerParser(BaseParser):
    def parse_args_get_series_diarias(self, args=None):
        self.params.set_params(args=args)
        param_cod_symbol = self.params.parse(nombre_param="cod_symbol", requerido=True)
        param_fch_desde = self.params.parse(nombre_param="fch_desde", requerido=True, datatype=date)
        param_fch_hasta = self.params.parse(nombre_param="fch_hasta", requerido=True, datatype=date)
        return {
            "cod_symbol":param_cod_symbol.valor,
            "fch_desde": param_fch_desde.valor,
            "fch_hasta": param_fch_hasta.valor
        }

    def parse_args_get_estadisticas(self, args=None):
        self.params.set_params(args=args)
        param_cod_symbol = self.params.parse(nombre_param="cod_symbol", requerido=True)
        return {
            "cod_symbol": param_cod_symbol.valor
        }


class ReparadorSeriesParser(BaseParser):
    def parse_args_reparar(self, args=None):
        self.params.set_params(args=args)
        param_cod_symbol = self.params.parse(nombre_param="cod_symbol", requerido=True)

        return {
            "cod_symbol": param_cod_symbol.valor
        }

class SerieManagerLoaderParser:
    def parse_args_actualizar_serie(self, args={}):
        parser = BaseParser(args=args)
        cod_symbol = parser.get("cod_symbol", requerido=True)
        args["cod_symbol"] = cod_symbol

        return args

class SimulacionVariacionParser(BaseParser):

    def parse_args_simular(self, args={}):
        self.params.set_params(args=args)

        cod_symbol = args.get("cod_symbol")
        if cod_symbol in [None,""]:
            raise AppException(msg="El cod_symbol es requerido")        

        param_fch_final = self.params.parse(nombre_param="fch_final", datatype=date, requerido=True)
        fch_final = param_fch_final.valor
        args["fch_final"] = fch_final

        lista_dias_profundidad_param = args.get("lista_dias_profundidad")
        if lista_dias_profundidad_param in [None,""]:
            raise AppException(msg="lista_dias_profundidad es requerido")
        
        lista_dias_profundidad = json.loads(lista_dias_profundidad_param)        
        
        fechas_iniciales = {}

        for dias_profundidad in lista_dias_profundidad:
            td = timedelta(days=dias_profundidad)
            fch_inicial = fch_final - td
            fechas_iniciales[fch_inicial.isoformat()] = (fch_inicial, dias_profundidad)
        
        args["fechas_iniciales"] = fechas_iniciales
        return args
    

        
