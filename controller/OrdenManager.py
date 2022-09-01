from app import app, db
from model.OrderModel import OrderModel
from datetime import datetime, date, time
from common.AppException import AppException
from common.Response import Response

from model.StockSymbol import StockSymbol
from model.StockTrade import StockTrade
from model.OrderModel import OrderModel

from controller.Base import Base

import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract

import json
from config.general import CLIENT_DATE_FORMAT

class OrdenManager(Base):
    def __init__(self, num_orden_ref=0, accion=""):
        self.num_orden_ref = num_orden_ref
        self.num_orden_ini = 0
        self.accion=accion
        self.prev_orden = None

    def gen_operaciones(self, ordenes=[]):
        from controller.OperacionesManager import GenericManager
        orden:OrderModel
        for orden in ordenes:            
            GenericManager().procesar(orden)   

    def gen_operaciones_x_orden(self, orden:OrderModel):
        from controller.OperacionesManager import GenericManager
        GenericManager().procesar(orden)

    """
    Las ordenes estan numeradas por fecha y symbol
    """
    def _reenumerar_ordenes(self, ordenes=[]):        
        prev_orden = None

        orden:OrderModel
        for orden in ordenes:                        
            orden.num_orden = self._get_sig_num_orden(orden, prev_orden)
            prev_orden = orden

    def _get_sig_num_orden(self,orden:OrderModel, prev_orden:OrderModel=None):
        if prev_orden == None:
            return 1
        if orden.order_date != prev_orden.order_date:
            return 1
        if orden.symbol != prev_orden.symbol:
            return 1
        
        return prev_orden.num_orden + 1

    def get_symbol(self, symbol=""):
        symbol = StockSymbol.query.filter(
            StockSymbol.symbol == symbol
        ).first()

        if symbol is None:
            raise AppException(msg="No se ha encontrado el symbolo {}".format(symbol))

        return symbol


class ProcesadorEntryPoint(OrdenManager):
    def __init__(self):
        pass

    def procesar(self, args={}):
        try:
            procesador = Procesador()
            self._validar_procesar(args)
            orden = self._collect(args)            
            procesador.procesar(orden)
            db.session.commit()
            return Response(msg="la orden se procesó correctamente").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def _collect(self, args={}):        
               
        order = OrderModel(
                symbol = args["symbol"],                                
                order_type = args["order_type"],
                quantity = int(args["shares_quantity"]),
                price = float(args["price_per_share"]),
                order_date = datetime.strptime(args["order_date"],CLIENT_DATE_FORMAT).date(),
                register_date = datetime.now().date()
            )        

        return order            

    def _validar_procesar(self, args={}):
        #validate symbol    
        errors = []
        if "symbol" not in args:
            errors.append("No se ha enviado symbol como parámetro en httprequest")                        
        
        trade_type = args["order_type"]
        if trade_type not in ["B","S"]:
            errors.append("el valor del parámetro [order_type] es invalido, valor enviado: {}".format(trade_type))

        if "shares_quantity" not in args:
            errors.append("No se ha enviado [shares_quantity] como parámetro del request")

        shares_quantity = args["shares_quantity"]
        if float(shares_quantity) <= 0.00:
            errors.append("La cantidad de participaciones no puede ser menor o igual a 0")

        args["shares_quantity"] = float(shares_quantity)

        if "order_date" not in args:
            errors.append("No se ha enviado [order_date] como parámetro del request")
        
        order_date = datetime.strptime(args.get("order_date"),CLIENT_DATE_FORMAT).date()        
        if order_date is None:
            errors.append("No se ha enviado una fecha de transacción correcta, valor enviado: {}".format(args["order_date"]))

        if "price_per_share" not in args:
            errors.append("No se ha enviado [price_per_share] como parámetro del request")
        
        trade_price = float(args["price_per_share"])
        if float(trade_price) <= 0.00:
            errors.append("El precio de la orden no puede ser menor o igual a 0")

        args["price_per_share"] = float(trade_price) 

        """
        if "action" not in args:
            errors.append("No se ha enviado [action] como parámetro del request")
        else:
            if args["action"] not in ["ins_antes","ins_despues",""]:
                errors.append("El parámetro 'action' tiene el valor no permitido: {0}".format(args["action"]))
        """

        if len(errors) > 0:
            raise AppException(msg="Se han encontrado errores de validacion", errors=errors)
            

class Procesador(OrdenManager):
    def __init__(self):
        self.orden = None

    def procesar(self, nu_orden:OrderModel):        
        self.orden = nu_orden
        nu_orden.num_orden = self._get_sig_num_orden()
        symbol_obj = self.get_symbol(nu_orden.symbol)

        nu_orden.asset_type = symbol_obj.asset_type

        nu_orden = self._insertar(nu_orden)
        self.gen_operaciones_x_orden(nu_orden)

    def _get_sig_num_orden(self):
        orden = db.session.query(
            func.max(OrderModel.num_orden).label("num_orden")
        ).filter(
            OrderModel.symbol == self.orden.symbol,
            OrderModel.order_date == self.orden.order_date
        ).first()

        if orden is None:
            return 1
        if orden.num_orden is None:
            return 1
        
        return orden.num_orden + 1


    def _insertar(self, orden:OrderModel=None):
        db.session.add(
            orden
        )
        db.session.flush()
        return orden

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
        ordenes = OrderModel.query.order_by(
            OrderModel.order_date.asc(),
            OrderModel.symbol.asc(),
            OrderModel.num_orden.asc()
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
    def __init__(self):
        pass

    def get_historial_ordenes(self, args={}):
        results = db.session.query(
            OrderModel
        ).all()
        return Response(raw_data=results).get()

    def get_max_fch_orden(self, args={}):
        response = Response()

        result = db.session.query(
            func.max(OrderModel.order_date).label("fch_orden"),
            extract("year",func.max(OrderModel.order_date)).label("anyo"),
            extract("month",func.max(OrderModel.order_date)).label("mes")
        ).first()

        """
        response.elem("fch_orden",datetime.now().strftime(CLIENT_DATE_FORMAT))

        if result is not None and result.fch_orden is not None:            
            response.elem("fch_orden",result.fch_orden.strftime(CLIENT_DATE_FORMAT))
        """                
        return response.from_raw_data(result)

    def get_ordenes_x_fecha(self, args={}):
        fch_orden = args.get("fch_orden")        

        if fch_orden is None:
            raise AppException(msg="No se ha ingresado una fecha de orden")

        fch_orden = datetime.strptime(fch_orden, CLIENT_DATE_FORMAT)

        result = db.session.query(
            OrderModel
        ).filter(
            OrderModel.order_date == fch_orden
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
            OrderModel.order_date,
            func.count(1).label("num_ordenes")
        ).filter(
            extract("year",OrderModel.order_date) == anyo,
            extract("month",OrderModel.order_date) == mes
        ).group_by(
            OrderModel.order_date
        ).all()

        return Response().from_raw_data(results)

    def get_max_anyo(self, args={}):
        result = db.session.query(
            func.max(extract("year",OrderModel.order_date)).label("max_anyo")
        ).first()

        return Response().from_raw_data(result)

    def get_anyos(elf, args={}):        
        results = db.session.query(
            extract("year",OrderModel.order_date).label("anyo")
        ).distinct("anyo").all()
        return Response().from_raw_data(results)             
    
    def get_meses(self, args={}):
        anyo = args.get("anyo")
        if anyo is None or anyo=="":
            raise AppException(msg="No se ha ingresado el año")
        
        results = db.session.query(
            extract("month",OrderModel.order_date).label("mes")
        ).filter(
            extract("year",OrderModel.order_date)==anyo
        ).distinct().all()

        return Response().from_raw_data(results)







        