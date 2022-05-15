from re import S
from app import app, db
from common.AppException import AppException
from model.StockTrade import StockTrade
from model.StockSymbol import StockSymbol
from model.OrderModel import OrderModel

from model.StockTrade import StockTrade
from model.TipoModel import TipoModel

from datetime import datetime, date, time
from common.Response import Response
from common.Error import Error
from sqlalchemy import desc
from sqlalchemy.orm import join
import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract
import config as CONFIG


class OperacionesManager:        
    def __init__(self):
        self.handlers = {
            "equity":GenericManager,
            "etf":GenericManager
        }

    def _get_handler(self, asset_type="equity"):
        return self.handlers[asset_type]

class EliminadorEntryPoint:
    def __init__(self):
        pass

    def procesar(self, args={}):
        try:
            self._validar(args)
            opers = self._collect(args)
            eliminador = Eliminador()
            eliminador.procesar(opers)
            db.session.commit()
            return Response(msg="Las Operaciones se han eliminado correctamente").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def _validar(self, args={}):
        errors = []
        if "del_opers" not in args:
            errors.append("El parámetro 'del_opers' no ha sido enviado")
        
        if len(errors) > 0:
            raise AppException(msg="Se han encontrado errores de validación",errors=errors)

    def _collect(self, args={}):
        return args["del_opers"]    

class Eliminador(OperacionesManager):
    def __init__(self):
        self.ids_opers = []        

    def procesar(self, ids_opers=[]):
        self.ids_opers = ids_opers
        self._eliminar_opers()
        self._eliminar_ordenes()        

    def _eliminar_opers(self):
        StockTrade.query.filter(
            StockTrade.id.in_(self.ids_opers)
        ).delete()

    def _eliminar_ordenes(self):
        ids_orden = self._get_ordenes_a_eliminar()
        from controller.OrdenManager import Eliminador
        Eliminador().procesar(ids_orden)

    def _get_ordenes_a_eliminar(self):
        ids_orden = []

        ordenes = db.session.query(
            StockTrade.order_id
        ).distinct().\
        filter(
            StockTrade.id.in_(self.ids_opers)
        ).all()

        for orden in ordenes:
            ids_orden.append(orden)

        ids_orden = set(ids_orden)
        return ids_orden

class GenericManager:
    def __init__(self):
        self.order = None
        self.saldo_orden = 0

    def procesar(self, order:OrderModel):
        self.order = order
        self.saldo_orden = order.quantity

        if self.order.order_type == CONFIG.ORDEN_TIPO_COMPRA:
            self.comprar()
        if self.order.order_type == CONFIG.ORDEN_TIPO_VENTA:
            self.vender()

    def comprar(self):
        num_operacion = self.__get_num_operacion()
        
        trade_date = self.order.order_date        
        trade_month = trade_date.month
        trade = StockTrade(
            symbol=self.order.symbol,
            num_operacion=num_operacion,
            trade_type = self.order.order_type,
            asset_type = self.order.asset_type,
            cantidad = self.order.quantity,
            saldo = self.order.quantity,
            premium = 0,
            trade_date = trade_date ,
            trade_month = trade_month,
            imp_accion = self.order.price,
            imp_operacion = self.order.price * self.order.quantity,
            imp_accion_origen=0,
            realized_gl=0,
            register_date = datetime.now().date(),
            register_time = datetime.now().time(),
            order_id = self.order.order_id,
            num_orden = self.order.num_orden            
        )

        db.session.add(trade) 

    def vender(self, args={}):
        num_operacion = self.__get_num_operacion()
        opers_con_saldo = self.__obt_operaciones_saldo()
        for oper in opers_con_saldo:            
            self.__vender(oper, num_operacion)
            num_operacion+=1

    def __vender(self, oper:StockTrade=None, num_operacion=1):
        trade_date = self.order.order_date        
        trade_month = trade_date.month
        saldo_orden = float(self.saldo_orden)
        saldo_oper = float(oper.saldo)

        if saldo_orden == 0:
            return None               

        cantidad = 0
        if saldo_oper == saldo_orden:
            cantidad = saldo_orden

        if saldo_oper < saldo_orden:
            cantidad = saldo_oper

        if saldo_oper > saldo_orden:
            cantidad = saldo_orden

        self.saldo_orden-=cantidad

        realized_gl = (self.order.price * cantidad) - (float(oper.imp_accion) * cantidad)

        trade = StockTrade(
            num_operacion=num_operacion,
            symbol=self.order.symbol,
            trade_type = self.order.order_type,
            asset_type = self.order.asset_type,
            ref_trade_id = oper.id,
            cantidad = cantidad,
            saldo = 0,
            premium = 0,
            trade_date = trade_date ,
            trade_month = trade_month,
            imp_accion = self.order.price,
            imp_operacion = self.order.price * cantidad,
            imp_accion_origen=oper.imp_accion,
            realized_gl=realized_gl,
            register_date = datetime.now().date(),
            register_time = datetime.now().time()
        )

        db.session.add(trade) 

        #actualizar la operacion origen
        oper.saldo = float(oper.saldo) - cantidad        

    def __obt_operaciones_saldo(self):
        data = db.session.query(
            StockTrade
        ).filter(
            #StockTrade.asset_type == "stocks",
            StockTrade.saldo != 0,
            StockTrade.symbol == self.order.symbol,
            StockTrade.trade_type == CONFIG.ORDEN_TIPO_COMPRA
        ).order_by(StockTrade.num_operacion).all()
        return data
    
    def __get_num_operacion(self):    
        result = db.session.query(
            func.max(StockTrade.num_operacion).label("num_operacion")
        ).\
        filter(
            StockTrade.trade_date == self.order.order_date,
            StockTrade.symbol == self.order.symbol
        ).first()            

        if result is None:
            return 1
        if result.num_operacion is None:
            return 1
        if result.num_operacion > 0:
            return result.num_operacion + 1

        

class BuscadorOperaciones:
    def __init__(self):
        pass

    def obt_historial_oper(self, args={}):
        try:
            query = db.session.query(
                StockTrade.id,
                StockTrade.num_operacion,
                StockTrade.order_id,
                StockTrade.num_orden,
                StockTrade.asset_type,
                StockTrade.symbol,
                StockTrade.trade_type,
                TipoModel.tipo_nombre.label("tipo_oper_nombre"),
                StockTrade.cantidad,
                StockTrade.saldo,
                StockTrade.trade_date,
                StockTrade.trade_month,
                StockTrade.imp_accion,
                StockTrade.imp_operacion,
                StockTrade.imp_accion_origen,
                StockTrade.realized_gl                
            ).outerjoin(TipoModel, StockTrade.trade_type == TipoModel.tipo_id)
            query = query.order_by(StockTrade.trade_date.desc(),StockTrade.symbol.asc(),StockTrade.num_operacion.desc())
            data = query.all()
            return Response(raw_data=data).get()
        except Exception as e:
            return Response().from_exception(e)
