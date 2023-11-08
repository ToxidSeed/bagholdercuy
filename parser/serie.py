from parser.base import BaseParser
from common.AppException import AppException
from datetime import date, timedelta
import json

class SimulacionVariacionParser:

    def parse_args_simular(self, args={}):
        cod_symbol = args.get("cod_symbol")
        if cod_symbol in [None,""]:
            raise AppException(msg="El cod_symbol es requerido")        
        
        fch_final = args.get("fch_final")
        if fch_final in [None,""]:
            raise AppException(msg="El fch_final es requerido")
        
        fch_final = date.fromisoformat(fch_final)
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
    

        
