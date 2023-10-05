from app import app, db
from model.orden import OrdenModel

from datetime import datetime, date, time
from common.AppException import AppException
from common.Response import Response

from model.StockSymbol import StockSymbol
from model.posicion import PosicionModel

from processor.orden import OrdenProcessor, CargadorMultipleProcessor, ReprocesadorOrdenesProcessor

from reader.symbol import SymbolReader
from reader.orden import OrdenReader

from controller.base import Base

import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract

import json, csv
from config.general import CLIENT_DATE_FORMAT

class OrdenManager(Base):
    
    def ejecutar(self, args={}):
        try:
            procesador = OrdenProcessor()
            self.__validar_procesar(args)
            orden = self.__collect(args)            
            procesador.ejecutar(orden)
            db.session.commit()
            return Response(msg="la orden se procesó correctamente").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def __collect(self, args={}):        

        cod_opcion = args.get('cod_opcion')        
        cod_symbol = args.get('cod_symbol')

        cod_symbol = None if cod_opcion != "" and cod_opcion is not None else cod_symbol
        cod_opcion = None if cod_symbol != "" and cod_symbol is not None else cod_opcion
               
        orden = OrdenModel(
                cod_symbol = cod_symbol,       
                cod_opcion = cod_opcion,
                cod_tipo_orden = args["tipo_orden"],
                cantidad = int(args["cantidad"]),
                usuario_id = self.usuario.id,
                imp_accion = float(args["imp_accion"]),
                fch_orden = datetime.strptime(args["fch_orden"],CLIENT_DATE_FORMAT).date(),
                fch_registro = datetime.now().date()
            )        

        return orden

    def __validar_procesar(self, args={}):
        #validate symbol    
        errors = []
        if "cod_symbol" not in args and "cod_opcion" not in args:
            errors.append("No se ha enviado el instrumento financiero")                        
        
        tipo_orden = args["tipo_orden"]
        if tipo_orden not in ["B","S"]:
            errors.append("el valor del parámetro [tipo_orden] es invalido, valor enviado: {}".format(trade_type))

        if "cantidad" not in args:
            errors.append("No se ha enviado [cantidad] como parámetro del request")

        cantidad = args["cantidad"]
        cantidad = 0 if cantidad == "" else cantidad

        if float(cantidad) <= 0.00:
            errors.append("La cantidad de participaciones no puede ser menor o igual a 0")        

        if "fch_orden" not in args:
            errors.append("No se ha enviado [fch_orden] como parámetro del request")
        
        fch_orden = datetime.strptime(args.get("fch_orden"),CLIENT_DATE_FORMAT).date()        
        if fch_orden is None:
            errors.append("No se ha enviado una fecha de transacción correcta, valor enviado: {}".format(args["fch_orden"]))

        if "imp_accion" not in args:
            errors.append("No se ha enviado [imp_accion] como parámetro del request")
        
        imp_accion = args.get("imp_accion")
        imp_accion = 0 if imp_accion == "" else imp_accion
        if float(imp_accion) <= 0.00:
            errors.append("El precio de la orden no puede ser menor o igual a 0")

        args["imp_accion"] = float(imp_accion) 

        if len(errors) > 0:
            raise AppException(msg="Se han encontrado errores de validacion", errors=errors)


    def get_symbol(self, symbol=""):
        symbol = StockSymbol.query.filter(
            StockSymbol.symbol == symbol
        ).first()

        if symbol is None:
            raise AppException(msg="No se ha encontrado el symbolo {}".format(symbol))

        return symbol

class ReprocesadorManager(Base):
    def ejecutar(self, args={}):
        try:
            reprocesador = ReprocesadorOrdenesProcessor()            
            self.__collect_ejecutar(reprocesador, args=args)
            reprocesador.reprocesar()
            db.session.commit()
            return Response(msg="Se ha completado el reproceso de ordenes")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def __collect_ejecutar(self, reprocesador:ReprocesadorOrdenesProcessor, args={}):
        flg_opcion = args.get("flg_opcion")
        cod_symbol = args.get("cod_symbol")
        cod_opcion = args.get("cod_opcion")
        flg_reprocesar_todo = args.get("flg_reprocesar_todo")

        if flg_reprocesar_todo is None:
            raise AppException(msg="No se ha enviado el indicador de reproceso total")

        if str(flg_reprocesar_todo).lower() not in ["true","false"]:
            raise AppException(msg="Valor incorrecto en el indicador de reproceso total")
        
        reprocesador.flg_reprocesar_todo = True if str(flg_reprocesar_todo).lower() == "true" else False
        #asignamos el indicador de reproceso
        if reprocesador.flg_reprocesar_todo == True:
            return
                    
        if flg_opcion is None:
            raise AppException(msg="No se ha enviado si el symbol es una opcion")

        if str(flg_opcion).lower() not in ["true","false"]:        
            raise AppException(msg="Valor incorrecto en el indicador de la opcion")

        reprocesador.flg_opcion = True if str(flg_opcion).lower() == "true" else False

        if cod_symbol in [None,""] and cod_opcion in [None,""]:
            raise AppException(msg="Se debe seleccionar/ingresar un symbol o una opcion")


        reprocesador.cod_symbol = cod_symbol
        reprocesador.cod_opcion = cod_opcion         
        reprocesador.usuario_id = self.usuario.id
            




"""
class ProcesadorEntryPoint(OrdenManager):
    def __init__(self):
        pass

    def procesar(self, args={}):
        try:
            procesador = OrdenProcessor()
            self._validar_procesar(args)
            orden = self._collect(args)            
            procesador.ejecutar(orden)
            db.session.commit()
            return Response(msg="la orden se procesó correctamente").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)                 
"""

class ReprocesadorEntryPoint:
    def __init__(self):
        pass

    def reprocesar(self, args={}):
        try:

            db.session.commit()
            return Response(msg="Se han reprocesado los symbols de forma correcta")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def reprocesar_todo(self, args={}):
        try:
            reprocesador = Reprocesador()
            reprocesador.reprocesar_todo()
            db.session.commit()
            return Response(msg="Se ha reprocesado todo de forma correcta")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

class Reprocesador(OrdenManager):
    def __init__(self):
        self.symbols = []

    def reprocesar(self, symbols=[]):
        self.symbols = symbols

        #eliminamos las operaciones
        self.eliminar_operaciones()
        
        ordenes = self._obt_ordenes_reprocesar(symbols)
        self._reenumerar_ordenes(ordenes)
        self.gen_operaciones(ordenes)

    def reprocesar_todo(self):
        self.eli_todo_opers()
        ordenes = self._obt_todo_ordenes_reprocesar() 
        self._reenumerar_ordenes(ordenes)                   
        self.gen_operaciones(ordenes)

    def _obt_todo_ordenes_reprocesar(self):
        ordenes = OrdenModel.query.order_by(
            OrdenModel.order_date.asc(),
            OrdenModel.symbol.asc(),
            OrdenModel.num_orden.asc()
        ).all()
        return ordenes    

    def eli_todo_opers(self):
        StockTrade.query.delete()                

    def eliminar_operaciones(self):
        StockTrade.query.filter(
            StockTrade.symbol.in_(self.symbols)
        ).delete()

    def _obt_ordenes_reprocesar(self, symbols=[]):
        ordenes = OrderModel.query.filter(
            OrderModel.symbol.in_(symbols)
        ).all()
        return ordenes
    
class EliminadorEntryPoint:
    def __init__(self):
        pass

    def procesar(self, args={}):
        try:
            self._validar(args=args)
            eliminador = Eliminador()
            eliminador.procesar(args["ids_ordenes"])
            db.session.commit()
            return Response(msg="Se ha eliminado correctamente la lista de ordenes").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def _validar(self, args={}):
        errors = []
        if "ids_ordenes" not in args:
            errors.append("El parámetro 'ids_ordenes' no ha sido enviado en la petición")
        else:
            ids_ordenes = args["ids_ordenes"]
            if len(ids_ordenes) == 0:
                errors.append("No se ha indicado ninguna orden a eliminar")

        if len(errors) > 0:
            raise AppException(msg="Se han encontrado errores de entrada en la petición", errors=errors)


class Eliminador(OrdenManager):
    def __init__(self):
        pass

    def procesar(self, list_ordenes=[]):
        symbols = self.get_symbols(list_ordenes)
        #eliminamos las ordenes
        OrderModel.query.filter(
            OrderModel.order_id.in_(list_ordenes)
        ).delete()
    
        #Eliminar una orden implica reprocesar
        reprocesador = Reprocesador()
        reprocesador.reprocesar(symbols)

    def get_symbols(self, list_ordenes=[]):
        symbols = []
        results = db.session.query(
            OrderModel.symbol
        ).distinct().\
        filter(
            OrderModel.order_id.in_(list_ordenes)
        ).all()

        for elem in results:
            symbols.append(elem.symbol)
        
        return symbols


class Buscador(OrdenManager):    

    def get_historial_ordenes(self, args={}):
        results = OrdenReader.get_ordenes(self.usuario.id)
        return Response().from_raw_data(results)

    def get_max_fch_orden(self, args={}):
        response = Response()

        result = db.session.query(
            func.max(OrdenModel.fch_orden).label("fch_orden"),
            extract("year",func.max(OrdenModel.fch_orden)).label("anyo"),
            extract("month",func.max(OrdenModel.fch_orden)).label("mes")
        ).first()

        """
        response.elem("fch_orden",datetime.now().strftime(CLIENT_DATE_FORMAT))

        if result is not None and result.fch_orden is not None:            
            response.elem("fch_orden",result.fch_orden.strftime(CLIENT_DATE_FORMAT))
        """                
        return response.from_raw_data(result)

    def get_ordenes_x_fecha(self, args={}):
        fch_orden = args.get("fch_orden")        

        if fch_orden in [None,""]:
            raise AppException(msg="No se ha ingresado una fecha de orden")

        fch_orden = datetime.strptime(fch_orden, CLIENT_DATE_FORMAT)

        result = db.session.query(
            OrdenModel
        ).filter(
            OrdenModel.fch_orden == fch_orden
        ).all()

        return Response().from_raw_data(result)

    def get_fechas(self, args={}):
        anyo = args.get("anyo")
        mes  = args.get("mes")

        if anyo is None:
            raise AppException(msg="No se ha ingresado el Año")
        if mes is None:
            raise AppException(msg="No se ha ingresado el mes")

        results = db.session.query(
            OrdenModel.fch_orden,
            func.count(1).label("num_ordenes")
        ).filter(
            extract("year",OrdenModel.fch_orden) == anyo,
            extract("month",OrdenModel.fch_orden) == mes
        ).group_by(
            OrdenModel.fch_orden
        ).all()

        return Response().from_raw_data(results)

    def get_max_anyo(self, args={}):
        result = db.session.query(
            func.max(extract("year",OrderModel.order_date)).label("max_anyo")
        ).first()

        return Response().from_raw_data(result)

    def get_anyos(elf, args={}):        
        results = db.session.query(
            extract("year",OrdenModel.fch_orden).label("anyo")
        ).distinct("anyo").all()
        return Response().from_raw_data(results)             
    
    def get_meses(self, args={}):
        anyo = args.get("anyo")
        if anyo is None or anyo=="":
            raise AppException(msg="No se ha ingresado el año")
        
        results = db.session.query(
            extract("month",OrdenModel.fch_orden).label("mes")
        ).filter(
            extract("year",OrdenModel.fch_orden)==anyo
        ).distinct().all()

        return Response().from_raw_data(results)

class CargadorMultipleManager(Base):
    def __init__(self):
        self.fichero = None

    def ejecutar(self, args={}):
        try:
            fichero = args.get("files").get("fichero")
            form = args.get("form")

            flg_procesar_ordenes = form.get("flg_procesar_ordenes")

            if flg_procesar_ordenes is None:
                raise AppException(msg="No se ha enviado 'flg_procesar_ordenes'")

            if flg_procesar_ordenes.lower() not in ["false","true"]:
                raise AppException(msg="El indicador para procesar ordenes no es correcto")

            flg_procesar_ordenes = True if flg_procesar_ordenes.lower() == "true" else False

            cargador = CargadorMultipleProcessor()
            #cargador.flg_procesar_ordenes = bool(flg_procesar_ordenes)
            cargador.flg_procesar_ordenes = flg_procesar_ordenes
            cargador.procesar(fichero, self.usuario.id)
            db.session.commit()
            return Response(msg="Se ha cargado correctamente las ordenes")            
        except Exception as e:        
            db.session.rollback()
            return Response().from_exception(e)

    
            

    





        