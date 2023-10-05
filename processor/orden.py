from model.orden import OrdenModel
from model.StockSymbol import StockSymbol

from processor.posicion import PosicionProcessor, PosicionEliminador

from reader.symbol import SymbolReader
from reader.orden import OrdenReader
from reader.opcion import OpcionReader

from common.AppException import AppException
from config.negocio import TIPO_ACTIVO_OPT, TIPO_ORDEN_COMPRA, TIPO_ORDEN_VENTA
from settings import config
from common.Formatter import Formatter

import csv, os
from datetime import date, datetime
from sqlalchemy import delete

from app import db



class OrdenProcessor:

    def __init__(self):
        self.orden = None

    def ejecutar(self, nu_orden:OrdenModel):
        self.orden = nu_orden
        self.orden.cod_tipo_activo = self._get_tipo_activo(nu_orden)
        self.orden.num_orden = self.__get_sig_num_orden()
        
        self.__insertar(nu_orden)     
        self._gen_posiciones_x_orden(nu_orden) 

    def _get_tipo_activo(self, orden:OrdenModel):

        cod_tipo_activo = None
        if orden.cod_opcion != "" and orden.cod_opcion is not None:
            return TIPO_ACTIVO_OPT

        if orden.cod_symbol == "":
            raise AppException(msg="La orden no tiene un instrumento financiero")

        symbol = SymbolReader.get(orden.cod_symbol)
        
        if symbol is not None:
            if symbol.asset_type is None:
                raise AppException(msg="El symbol {} no tiene un tipo de activo asignado".format(symbol))
            else:
                return symbol.asset_type

        raise AppException(msg="No se ha encontrado el symbolo {}".format(symbol))

    def __insertar(self, orden:OrdenModel):
        db.session.add(
            orden
        )

        db.session.flush()
        return orden

    def _gen_posiciones_x_orden(self, orden:OrdenModel):
        PosicionProcessor().procesar_orden(orden)
    
    def __get_sig_num_orden(self):        

        num_orden = OrdenReader.get_max_num_orden(self.orden.usuario_id, self.orden.fch_orden, self.orden.cod_symbol, self.orden.cod_opcion)
        
        if num_orden is None:
            num_orden = 1
        else:
            num_orden += 1
        
        return num_orden        
                        
class CargadorMultipleProcessor:
    def __init__(self):
        self.fichero = None
        self.symbols = {}
        self.usuario_id = None
        self.correlativos = {}
        self.flg_procesar_ordenes = True

    def procesar(self, fichero, usuario_id):           
        self.usuario_id = usuario_id
        #self.fichero = fichero
        fch_actual = date.today().strftime("%Y%m%d")

        tmp_dir = config.get("rutas","tmp_dir")        

        fichero_nombre = "{0}-{1}.csv".format(usuario_id, fch_actual)
        self.fichero = os.path.join(tmp_dir, fichero_nombre)
        fichero.save(self.fichero)        

        with open(self.fichero) as csv_fichero:
            csv_reader = csv.reader(csv_fichero, delimiter=",")
            for rownum, record in enumerate(csv_reader, start=1):                                
                if rownum == 1:
                    continue

                orden = self.__crear_orden(record)

                if not self.flg_procesar_ordenes:
                    continue

                #Genrear posiciones
                PosicionProcessor().procesar_orden(orden)
                try:
                    db.session.flush()
                except Exception as e:
                    raise AppException(msg="Error al procesar la orden {0}, exception: {1} ".format(str(record), str(e)))

    def __crear_orden(self, record):
        #symbol
        cod_instrumento = record[0]
        #UnderlyingSymbol
        cod_subyacente = record[1]        
        #TradeDate
        fch_orden = record[2]
        fch_orden = datetime.strptime(fch_orden,"%Y%m%d").date()
        #Quantity
        ctd_orden = int(record[3])
        #TradePrice
        imp_accion = record[4]                

        cod_symbol = None
        cod_opcion = None
        cod_tipo_activo = None
        num_orden = None

        if cod_subyacente == "":
            cod_symbol = cod_instrumento
            cod_tipo_activo = self.__get_tipo_activo(cod_symbol)
            num_orden = self.__get_num_orden(fch_orden, cod_symbol=cod_symbol)
        else:
            cod_opcion = self.__format_cod_opcion(cod_instrumento)
            self.__validar_opcion(cod_opcion=cod_opcion)
            cod_tipo_activo = TIPO_ACTIVO_OPT
            num_orden = self.__get_num_orden(fch_orden, cod_opcion=cod_opcion)

        cod_tipo_orden = TIPO_ORDEN_COMPRA if ctd_orden > 0 else TIPO_ORDEN_VENTA
        
        orden = OrdenModel(
            num_orden = num_orden,
            cod_tipo_orden = cod_tipo_orden,
            cod_symbol = cod_symbol,
            cod_opcion = cod_opcion,
            cod_tipo_activo = cod_tipo_activo,
            cantidad = abs(ctd_orden),
            imp_accion = imp_accion,
            usuario_id = self.usuario_id,
            fch_registro = date.today(),
            fch_orden = fch_orden
        )    

        db.session.add(orden)    
        return orden

    def __get_tipo_activo(self, cod_symbol):
        if cod_symbol in self.symbols:
            return self.symbols[cod_symbol].asset_type

        symbol = SymbolReader.get(cod_symbol)
        if symbol is None:
            raise AppException(msg="No se ha encontado el symbol {0}".format(cod_symbol))

        if symbol.symbol not in self.symbols:
            self.symbols[symbol.symbol] = symbol

        return symbol.asset_type

    def __format_cod_opcion(self, cod_opcion):
        cod_opcion = cod_opcion.replace(" ","")
        cod_subyacente = cod_opcion[:-15]
        fch_exp_yymmdd = cod_opcion[-15:-9]
        resto = cod_opcion[-9:] 
        cod_opcion_nuevo = "{0}20{1}{2}".format(cod_subyacente, fch_exp_yymmdd, resto)
        return cod_opcion_nuevo    

    def __validar_opcion(self, cod_opcion):
        opcion_reader = OpcionReader.get(cod_opcion)
        if opcion_reader is None:
            raise AppException(msg="No existe la opcion {0}".format(cod_opcion))

    def __get_num_orden(self, fch_orden, cod_symbol=None, cod_opcion=None):
        
        cod_correlativo = None
        cod_fch_orden = date.strftime(fch_orden, "%Y%m%d")

        if cod_symbol is not None:
            cod_correlativo = "{0}{1}".format(cod_symbol, cod_fch_orden)    

        if cod_opcion is not None:
            cod_correlativo = "{0}{1}".format(cod_opcion, cod_fch_orden)    

        if cod_correlativo in self.correlativos:
            return int(self.correlativos[cod_correlativo]) + 1
        

        num_orden = OrdenReader.get_max_num_orden(self.usuario_id, fch_orden, cod_symbol=cod_symbol, cod_opcion=cod_opcion)

        if num_orden is None:
            self.correlativos[cod_correlativo] = 1
            return 1
                
        num_orden = num_orden + 1        
        self.correlativos[cod_correlativo] = num_orden
        return num_orden

class ReprocesadorOrdenesProcessor:
    def __init__(self):
        self.usuario_id = None
        self.flg_opcion = None
        self.cod_symbol = None
        self.cod_opcion = None      
        self.flg_reprocesar_todo = False  
        self.ordenes = []

    def reprocesar(self):    
        if self.flg_reprocesar_todo == True:
            self.reprocesar_todo()
        else:
            self.reprocesar_x_instrumento()      
    
    def reprocesar_x_instrumento(self):
        if self.flg_opcion == True:
            opcion = OpcionReader.get(self.cod_opcion)
            if opcion is None:
                raise AppException(msg="No se ha encontrado una opcion con codigo {0}".format(self.cod_opcion))            
            else:
                #Eliminamos las posiciones por opcion
                PosicionEliminador.eliminar_x_opcion(self.usuario_id, self.cod_opcion)

                #obtenemos las ordenes para reprocesar
                self.ordenes = OrdenReader.get_ordenes(self.usuario_id, cod_opcion=self.cod_opcion)

        if self.flg_opcion == False:
            symbol = SymbolReader.get(self.cod_symbol)
            if symbol is None:
                raise AppException(msg="No se ha encontrado un symbol con codigo {0}".format(self.cod_symbol))
            else:
                #Eliminamos las posiciones para los otros activos
                PosicionEliminador.eliminar_x_otros_activos(self.usuario_id, self.cod_symbol)
                #
                self.ordenes = OrdenReader.get_ordenes(self.usuario_id, cod_symbol=self.cod_symbol)        

        self.__reprocesar_ordenes()            

    def reprocesar_todo(self):
        self.ordenes = OrdenReader.get_ordenes(self.usuario_id)
        self.__reprocesar_ordenes()            

    def __reprocesar_ordenes(self):
        if len(self.ordenes) == 0:
            raise AppException(msg="No se ha encontrado ordenes para reprocesar")

        for orden in self.ordenes:
            PosicionProcessor().procesar_orden(orden)        

    


    

    

        
    

