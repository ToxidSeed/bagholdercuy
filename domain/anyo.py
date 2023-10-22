from datetime import MINYEAR, MAXYEAR
from common.AppException import AppException

class Anyo:
    def __init__(self, value):
        self.value = self.parse(value)

    def parse(self, valor):
        if valor is None:
            return None
        
        if isinstance(valor, str):
            return self.parse_string(valor=valor)
        
        if isinstance(valor, int):
            self.__val_rango_anyo(valor=valor)
            return valor

    def parse_string(self, valor):        
        valor = int(valor)
        self.__val_rango_anyo(valor=valor)

    
    def __val_rango_anyo(self, valor):
        if valor < MINYEAR or valor > MAXYEAR:
            raise AppException(msg=f"El anyo deberia estar en el rango {MINYEAR}-{MAXYEAR}, valor: {valor}")                