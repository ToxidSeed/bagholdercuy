from model.orden import OrdenModel
from model.StockSymbol import StockSymbol

from processor.transaccion import TransaccionProcessor

from reader.symbol import SymbolReader
from reader.orden import OrdenReader
from reader.opcion import OpcionReader

from common.AppException import AppException
from config.negocio import TIPO_ACTIVO_OPT, TIPO_ACTIVO_OTROS, TIPO_ORDEN_COMPRA, TIPO_ORDEN_VENTA
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
        self.id_cuenta = None
        self.correlativos = {}
        self.flg_procesar_ordenes = True

    def procesar(self, fichero, id_cuenta):           
        self.id_cuenta = id_cuenta
        #self.fichero = fichero
        fch_actual = date.today().strftime("%Y%m%d")

        tmp_dir = config.get("rutas","tmp_dir")        

        fichero_nombre = "{0}-{1}.csv".format(id_cuenta, fch_actual)
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

                TransaccionProcessor().generar_desde_orden(orden=orden)                

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
        imp_accion = float(record[4])

        id_symbol = None
        id_contrato_opcion = None
        cod_tipo_activo = None
        num_orden = None

        instrumento, cod_tipo_activo = self.__get_instrumento(cod_instrumento=cod_instrumento)

        if cod_tipo_activo == TIPO_ACTIVO_OPT:
            subyacente, cod_tipo_activo_subyacente = self.__get_subyacente(cod_symbol=cod_subyacente)
            id_symbol = subyacente.id
            id_contrato_opcion = instrumento.id
        else:
            id_symbol = instrumento.id
       
        orden = OrdenModel(
            id_cuenta = self.id_cuenta,
            num_orden = self.__get_siguiente_num_orden(fch_orden),
            cod_tipo_orden = self.__get_tipo_orden(ctd_orden=ctd_orden),
            id_symbol = id_symbol,
            id_contrato_opcion = id_contrato_opcion,       
            cod_tipo_activo = cod_tipo_activo,
            cantidad = abs(ctd_orden),
            imp_accion = imp_accion,
            fch_registro = date.today(),
            fch_orden = fch_orden
        )    

        db.session.add(orden)  
        db.session.flush()  
        return orden

    def __get_instrumento(self, cod_instrumento):
        if cod_instrumento in self.symbols:
            return self.symbols[cod_instrumento]

        symbol = SymbolReader.get(cod_symbol=cod_instrumento)
        contrato_opcion = None

        if symbol is not None:            
            self.symbols[symbol.symbol] = (symbol, TIPO_ACTIVO_OTROS)
            return (symbol, TIPO_ACTIVO_OTROS)

        cod_opcion = self.__format_cod_opcion(cod_instrumento)
        contrato_opcion = OpcionReader.get(cod_contrato_opcion=cod_opcion)
        if contrato_opcion is not None:
            self.symbols[contrato_opcion.symbol] = (contrato_opcion, TIPO_ACTIVO_OPT)
            return (contrato_opcion, TIPO_ACTIVO_OPT)
        else:
            raise AppException(msg=f"No se ha encontrado el instrumento {cod_instrumento}")

    def __get_subyacente(self, cod_symbol):
        if cod_symbol in self.symbols:
            return self.symbols[cod_symbol]

        symbol = SymbolReader.get(cod_symbol=cod_symbol)

        if symbol is not None:
            return (symbol, TIPO_ACTIVO_OTROS)
        else:
            raise AppException(msg=f"No se ha encontrado el subyacente {cod_symbol}")

    def __get_tipo_orden(self, ctd_orden=0):
        if ctd_orden == 0:
            raise AppException(msg="El importe de la orden no puede ser 0")
        
        if ctd_orden > 0:
            return TIPO_ORDEN_COMPRA
        else:
            return TIPO_ORDEN_VENTA
        

    def __format_cod_opcion(self, cod_opcion):
        cod_opcion = cod_opcion.replace(" ","")
        cod_subyacente = cod_opcion[:-15]
        fch_exp_yymmdd = cod_opcion[-15:-9]
        resto = cod_opcion[-9:] 
        cod_opcion_nuevo = "{0}20{1}{2}".format(cod_subyacente, fch_exp_yymmdd, resto)
        return cod_opcion_nuevo    

    def __get_siguiente_num_orden(self, fch_orden):        

        cod_correlativo = fch_orden.strftime("%Y%m%d")

        if cod_correlativo in self.correlativos:
            return int(self.correlativos[cod_correlativo]) + 1
                       
        num_orden = OrdenReader.get_max_num_orden(self.id_cuenta, fch_orden)
        num_orden += 1                        
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

    


    

    

        
    

