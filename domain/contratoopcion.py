from common.AppException import AppException
from datetime import date, datetime

class ContratoOpcion:
    def __init__(self, value):
        self.__imp_ejercicio = None
        self.__cod_tipo_opcion = None
        self.__fch_expiracion = None
        self.__cod_symbol_subyacente = None
        self.__value = self.parse(value)        

    def parse(self, valor):
        if valor in [None,""]:
            return None
        
        self.__imp_ejercicio = self.__extraer_ejercicio(valor=valor)
        self.__cod_tipo_opcion = self.__extraer_cod_tipo_opcion(valor=valor)
        self.__fch_expiracion  = self.__extraer_fch_expiracion(valor=valor)
        self.__cod_symbol_subyacente = self.__extraer_cod_symbol_subyacente(valor=valor)

        return valor
            
    def __extraer_ejercicio(self, valor):
        str_ejercicio = valor[-8:]
        return float(int(str_ejercicio))/1000
    
    def __extraer_cod_tipo_opcion(self, valor):
        cod_tipo_opcion = valor[-9:-8]
        if cod_tipo_opcion not in ["P","C"]:
            raise AppException(msg=f"No se encuentra el tipo de opcion en el codigo {valor}, valor encontrado {cod_tipo_opcion}")
        
        return cod_tipo_opcion

    def __extraer_fch_expiracion(self, valor):
        return datetime.strptime(valor[-17:-9],"%Y%m%d").date()
    
    def __extraer_cod_symbol_subyacente(self, valor):
        return valor[:-17]
                
    @property
    def imp_ejercicio(self):
        return self.__imp_ejercicio
    
    @property
    def cod_tipo_opcion(self):
        return self.__cod_tipo_opcion
    
    @property
    def fch_expiracion(self):
        return self.__fch_expiracion
    
    @property
    def cod_symbol_subyacente(self):
        return self.__cod_symbol_subyacente
    
    @property
    def value(self):
        return self.__value