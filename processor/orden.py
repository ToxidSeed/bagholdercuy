from model.orden import OrdenModel
from model.StockSymbol import StockSymbol
from model.posicion import PosicionModel
from model.operacion import OperacionModel

from processor.transaccion import TransaccionProcessor
from processor.operacion import OperacionProcessor
from processor.posicion import PosicionProcessor

from reader.symbol import SymbolReader
from reader.orden import OrdenReader
from reader.opcion import OpcionReader
from reader.posicion import PosicionReader
from reader.operacion import OperacionReader

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
        #PosicionProcessor().procesar_orden(orden)
        pass
    
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
        self.numeracion_operaciones = {}
        self.posiciones_afectadas = {}
        self.flg_procesar_ordenes = True           

    def procesar(self, fichero, id_cuenta):           
        self.id_cuenta = int(id_cuenta)
        #self.fichero = fichero
        fch_actual = date.today().strftime("%Y%m%d")

        tmp_dir = config.get("rutas","tmp_dir")        

        fichero_nombre = "{0}-{1}.csv".format(id_cuenta, fch_actual)
        self.fichero = os.path.join(tmp_dir, fichero_nombre)
        fichero.save(self.fichero)

        #
        self.__procesar_fichero()

    def __procesar_fichero(self):        
        with open(self.fichero) as csv_fichero:
            csv_reader = csv.reader(csv_fichero, delimiter=",")
            self.__procesar_lineas_fichero(csv_reader)

            #guardamos los cambios en las posiciones 
            self.__guardar_cambios_en_posiciones()

    def __guardar_cambios_en_posiciones(self):
        for posicion, operacion in self.posiciones_afectadas.values():            
            PosicionProcessor().cambiar_posicion(posicion=posicion, operacion=operacion)

    def __procesar_lineas_fichero(self, csv_reader):                        
        for rownum, record in enumerate(csv_reader, start=1):     
            try:                           
                if rownum == 1:
                    continue
                
                self.__procesar_linea(record=record)
            except Exception as e:
                raise AppException(msg=f"Error procesando la linea {rownum}: {str(e)}")

    def __procesar_linea(self, record):            
        #creamos la orden 
        pre_orden = self.__parse_record_a_orden(record=record)

        #generamos las ordenes en bd
        operacion = self.__generar_operacion(orden=pre_orden) 

        #las pre_ordenes generadas las guardamos en base de datos
        db.session.add(pre_orden)                   
        
    def __generar_operacion(self, orden:OrdenModel):
        processor = OperacionProcessor()

        #obtenemos la posicion afectada por la orden
        posicion_tmp, operacion = self.__get_cambio_temporal_posicion(orden=orden)

        #obtenemos la numeracion de la operacion
        num_orden_operacion = self.__get_siguiente_num_orden_operacion(id_cuenta=orden.id_cuenta, fch_operacion=orden.fch_orden)

        #le indicamos a la operacion, la posicion  y la operacion previa
        operacion = processor.procesar_orden(orden=orden, posicion=posicion_tmp, operacion=operacion, num_orden_operacion=num_orden_operacion)
        db.session.flush()

        #Indicamos el cambio en la posicion temporal
        self.__guardar_cambio_temporal_posicion(posicion=posicion_tmp, operacion=operacion)

        return operacion
    
    def __guardar_cambio_temporal_posicion(self, posicion:PosicionModel, operacion:OperacionModel):        
        
        if posicion is None:
            nueva_posicion = PosicionModel(
                id_cuenta = operacion.id_cuenta,
                id_symbol = operacion.id_symbol,
                id_contrato_opcion = operacion.id_contrato_opcion,
                cantidad = 0,
                imp_promedio = 0,
                imp_maximo = 0,
                imp_minimo = 0,
                fch_registro = date.today(),
                fch_ultima_actualizacion = date.today()
            )

            posicion = nueva_posicion

        id_temporal = self.__id_temporal_posicion(operacion.id_cuenta, operacion.id_symbol, operacion.id_contrato_opcion)

        #anadimos a la memoria
        self.posiciones_afectadas[id_temporal] = (posicion, operacion)        
    
    def __get_cambio_temporal_posicion(self, orden:OrdenModel):
        #obtener desde cache
        id_temporal_posicion = self.__id_temporal_posicion(orden.id_cuenta, orden.id_symbol, orden.id_contrato_opcion)
        cambio_posicion = self.posiciones_afectadas.get(id_temporal_posicion)
        if cambio_posicion is not None:
            return cambio_posicion
        
        posicion = PosicionReader.get_x_instrumento(orden.id_cuenta, orden.id_symbol, orden.id_contrato_opcion)
        #guardamos en 'cache'
        if posicion is not None:
            self.posiciones_afectadas[id_temporal_posicion] = (posicion, None)
            return (posicion, None)

        return (None, None)
    
    def __get_siguiente_num_orden_operacion(self, id_cuenta, fch_operacion):
        id_numeracion = f"{id_cuenta}-{fch_operacion.isoformat()}"
        num_orden_operacion = self.numeracion_operaciones.get(id_numeracion)
        if num_orden_operacion is not None:
            return num_orden_operacion + 1
        
        #si no esta en la memoria buscar el maximo en la base de datos
        num_orden_operacion = OperacionReader.get_max_num_orden(id_cuenta=id_cuenta, fch_operacion=fch_operacion)
        if num_orden_operacion is not None:
            return num_orden_operacion + 1
        
        return 1


    def __id_temporal_posicion(self, id_cuenta, id_symbol, id_contrato_opcion=None):
        return "-".join(map(str,[id_cuenta, id_symbol, id_contrato_opcion]))

    def __parse_record_a_orden(self, record):
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
    
class OperacionesMultiplesCreator:
    def __init__(self):
        self.operaciones_numeracion = {}
        self.posiciones = {}

    def crear(self, ordenes=[]):
        for orden in ordenes:
            num_orden_operacion = self.__get_siguiente_num_orden_operacion(id_cuenta=orden.id_cuenta, fch_operacion=orden.fch_orden)                        
            posicion, ctd_posicion_tmp, id_operacion_tmp = self.__get_posicion(orden=orden)
            operacion = OperacionProcessor().procesar_orden(orden=orden, num_orden_operacion=num_orden_operacion, ctd_posicion=ctd_posicion_tmp)

            #enviamos los cambios a base de datos
            db.session.flush()

            #Aactualizando datos
            orden.id_operacion = operacion.id_operacion
                            
    
    def __id_temporal(self, id_cuenta, id_symbol, id_contrato_opcion=None):
        return "-".join([id_cuenta, id_symbol, id_contrato_opcion])

    def __get_posicion(self, orden:OrdenModel):   
        id_temporal = self.__id_temporal(id_cuenta=orden.id_cuenta, id_symbol=orden.id_symbol, id_contrato_opcion=orden.id_contrato_opcion)
        if id_temporal in self.posiciones:
            return self.posiciones[id_temporal]
        
        #        
        posicion = PosicionReader.get_x_instrumento(id_cuenta=orden.id_cuenta, id_symbol=orden.id_symbol, id_contrato_opcion=orden.id_contrato_opcion)
        if posicion is not None:
            self.posiciones[id_temporal] = (posicion, posicion.cantidad, posicion.id_operacion)
            return self.posiciones[id_temporal]

        posicion = orden.a_posicion
        self.posiciones[id_temporal] = (posicion, posicion.cantidad, posicion.id_operacion)
        return self.posiciones[id_temporal]
    
    def __modificar_posicion_temporal(self, posicion:PosicionModel, operacion):
        id_temporal = self.__id_temporal(id_cuenta=posicion.id_cuenta, id_symbol=posicion.id_symbol, id_contrato_opcion=posicion.id_contrato_operacion)

    def __get_siguiente_num_orden_operacion(self, id_cuenta, fch_operacion):
        id_numeracion = f"{fch_operacion.isoformat()}-{id_cuenta}"
        if id_numeracion not in self.operaciones_numeracion:
            num_operacion = OperacionProcessor().get_siguiente_num_orden(id_cuenta, fch_operacion)
            self.operaciones_numeracion[id_numeracion] = num_operacion
        else:
            self.operaciones_numeracion[id_numeracion] += 1
        
        return self.operaciones_numeracion[id_numeracion]        

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

    


    

    

        
    

