from model.OptionContract import OptionContractModel
from reader.opcion import OpcionReader
from reader.symbol import SymbolReader

import csv
from datetime import date, datetime

from app import db
from settings import config

from common.AppException import AppException

class OpcionProcessor:
    def guardar(self, opcion:OptionContractModel):
        self.__validar_symbol(opcion.symbol)
        db.session.add(opcion)

    def __validar_symbol(self, cod_symbol):
        symbol = OpcionReader.get(cod_symbol)
        if symbol is not None:
            raise AppException(msg="El symbol {0} ya existe".format(cod_symbol))

    def __validar_subyacente(self, cod_subyacente):
        subyacente = SymbolReader.get(cod_subyacente)
        if subyacente is None:
            raise AppException(msg="El subyacente {0} no existe".format(cod_subyacente))

class OpcionLoader:
    def __init__(self):
        self.fichero = None
        self.cod_moneda = None
        self.ctd_multiplicador = None
        self.formato_cod_opcion = None
        self.flg_excluir_errores = True        

    def procesar(self):
        self.__procesar_fichero()

    def __procesar_fichero(self):
        with open(self.fichero) as csv_file:
            csv_reader = csv.reader(csv_file)
            for rownum, record in enumerate(csv_reader, start=1):
                if rownum == 1:
                    continue

                try:                    
                    self.__crear_opcion(record)
                except Exception as e:
                    if self.flg_excluir_errores:
                        pass
                    else:
                        raise AppException(msg="Error en la linea {0}".format(rownum)).from_exception(e)

    def __crear_opcion(self, record):
        cod_opcion_in = record[0]
        opcion = OptionContractModel()
        opcion.currency = self.cod_moneda
        opcion.contract_size = self.ctd_multiplicador           
                
        cod_opcion, cod_subyacente, fch_exp, sentido, imp_ejercicio = self.__descomponer_cod_opcion(cod_opcion_in)        
        
        opcion.underlying = cod_subyacente
        opcion.expiration_date = fch_exp
        opcion.strike = imp_ejercicio
        opcion.side = sentido
        opcion.symbol = cod_opcion
        opcion.fch_audit = datetime.now()
        opcion.moneda_id = self.cod_moneda
        opcion.register_date = datetime.now().date()

        db.session.add(opcion)        
        
    
    def __descomponer_cod_opcion(self, cod_opcion):
        if self.formato_cod_opcion == config.get("formato.cod_opcion","fmt_interactive_brokers"):
            return self.__descom_cod_opcion_ibk(cod_opcion)
    
    def __descom_cod_opcion_ibk(self, cod_opcion_in):

        if len(cod_opcion_in) <= int(config.get("formato.cod_opcion","min_longitud")):
            raise AppException(msg="El formato de la opcion {0} que se quire descomponer no es correcto".format(cod_opcion_in))

        fch_exp =  datetime.strptime(cod_opcion_in[-15:-9], "%y%m%d").date()
        cod_tipo_sentido = cod_opcion_in[-9:-8]
        cod_ejercicio = cod_opcion_in[-8:]

        if cod_tipo_sentido not in ["C","P"]:
            raise AppException(msg="El tipo de sentido extraido de la opcion {0} no es correcto".format(cod_tipo_sentido))

        sentido = ""
        if cod_tipo_sentido == "C":
            sentido = "call"
        if cod_tipo_sentido == "P":
            sentido = "put"                

        imp_ejercicio = float(int(cod_ejercicio)/1000)
        cod_subyacente = cod_opcion_in[:-15].strip()
        cod_opcion = "{0}{1}{2}{3}".format(cod_subyacente, fch_exp.strftime("%Y%m%d"), cod_tipo_sentido, cod_ejercicio)

        if len(cod_opcion) <= int(config.get("formato.cod_opcion","min_longitud")):
            raise AppException(msg="El formato de la opcion {0} que se quire descomponer no es correcto".format(cod_opcion_in))

        self.__validar_existencia_opcion(cod_opcion)

        return (cod_opcion, cod_subyacente, fch_exp, sentido, imp_ejercicio)

    def __validar_existencia_opcion(self, cod_opcion):
        opcion = OpcionReader.get(cod_opcion)

        if opcion is not None:            
            raise AppException(msg="El codigo de opcion {0} ya existe".format(cod_opcion))
            

        
