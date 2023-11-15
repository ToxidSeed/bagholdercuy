from common.AppException import AppException

from datetime import datetime, date
class BaseParser:
    def __init__(self, args={}):
        self.args = args

    @staticmethod
    def parse_id_cuenta(id_cuenta):
        if id_cuenta in [None, ""]:
            return None

        return int(id_cuenta)

    @staticmethod
    def parse_date(fecha):
        if fecha in [None,""]:
            return None

        return date.fromisoformat(fecha)

    @staticmethod
    def parse_int(param):
        if param in [None,""]:
            return None

        return int(param)
    
    @staticmethod
    def parse_boolean(param):
        if param in [None, "", "false", "False", False, 0, "0"]:
            return False
        else:
            return True
    
    @staticmethod
    def parse_orden_resultados(param):
        if param in [None,""]:
            return None
        
        if param not in ["asc","desc"]:
            raise AppException(msg="orden_resultados solo puede ser asc o desc")
        
    def get(self, nombre_param, requerido=False, datatype=None, vacio_es_nulo=False):

        valor = self.args.get(nombre_param)
        if requerido is True:            
            if valor in [None,""]:
                raise AppException(msg=f"No se ha enviado {nombre_param}")                    
            
        valor = None if vacio_es_nulo is True and valor == '' else valor
        
        if datatype is not None:
            if datatype == int:
                return self.parse_int(valor)
            
            if datatype == float:
                return float(valor)
        
        return valor