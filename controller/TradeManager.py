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


class TradeManager:        
    def __init__(self):
        self.handlers = {
            "equity":GenericManager,
            "etf":GenericManager
        }
    
    def order(self, args={}):
        try:
            error = self.__validate(args)
            if error is not None:
                return Response().from_error(error)

            symbol_obj = self.__get_symbol(args["symbol"])        
            args["asset_type"] = symbol_obj.asset_type
            order = Order().save(args)                            

            #stock
            handler = self.handlers[symbol_obj.asset_type]
            handler(order).procesar()
        
            db.session.commit()
            return Response(msg="Orden de compra ejecutada").get()
        except Exception as e:
            return Response().from_exception(e)

    def __get_symbol(self, symbol=""):
        #asset type                   
        symbol_obj = db.session.query(StockSymbol).filter(
            StockSymbol.symbol == symbol
        ).first()

        #check existence of symbol
        if symbol_obj is None:
            raise AppException(msg="El symbol {0} no se encuentra registrado".format(symbol))

        return symbol_obj

    def __validate(self, args={}):
        #validate symbol
        error = Error()
        if "symbol" not in args:
            error.add("No se ha enviado symbol como parámetro en httprequest")                        

        symbol_input = args["symbol"]
        symbol = StockSymbol.query.filter(
            StockSymbol.symbol == symbol_input
        ).first()

        if symbol is None:
            error.add("No se ha encontrado el symbolo {}".format(symbol_input))            

        if "order_type" not in args:
            error.add("No se ha enviado order_type como parámetro del request")

        trade_type = args["order_type"]
        if trade_type not in ["B","S"]:
            error.add("el valor del parámetro [order_type] es invalido, valor enviado: {}".format(trade_type))

        if "shares_quantity" not in args:
            error.add("No se ha enviado [shares_quantity] como parámetro del request")

        shares_quantity = args["shares_quantity"]
        if float(shares_quantity) <= 0.00:
            error.add("La cantidad de participaciones no puede ser menor o igual a 0")

        args["shares_quantity"] = float(shares_quantity)

        if "order_date" not in args:
            error.add("No se ha enviado [order_date] como parámetro del request")
        
        order_date = date.fromisoformat(args["order_date"])
        if order_date is None:
            error.add("No se ha enviado una fecha de transacción correcta, valor enviado: {}".format(args["order_date"]))

        if "price_per_share" not in args:
            error.add("No se ha enviado [price_per_share] como parámetro del request")
        
        trade_price = float(args["price_per_share"])
        if float(trade_price) <= 0.00:
            error.add("El precio de la orden no puede ser menor o igual a 0")

        args["price_per_share"] = float(trade_price)        

        if error.has_errors():
            return error
        else:
            return None

class Order:
    def __init__(self):
        pass        

    def save(self, args={}):        
        order = OrderModel(
                symbol = args["symbol"],
                asset_type = args["asset_type"],
                order_type = args["order_type"],
                quantity = args["shares_quantity"],
                price = args["price_per_share"],
                order_date = date.fromisoformat(args["order_date"]),
                register_date = datetime.now().date()
            )

        db.session.add(
            order
        )

        db.session.flush()

        return order

class GenericManager:
    def __init__(self, order:OrderModel=None):
        self.order = order
        self.saldo_orden = self.order.quantity

    def procesar(self, args={}):
        if self.order.order_type == CONFIG.ORDEN_TIPO_COMPRA:
            self.comprar()
        if self.order.order_type == CONFIG.ORDEN_TIPO_VENTA:
            self.vender()

    def comprar(self, args={}):
        num_operacion = self.__get_ult_num_operacion(self.order.order_date.year)
        
        trade_date = self.order.order_date        
        trade_month = trade_date.month
        trade = StockTrade(
            symbol=self.order.symbol,
            num_operacion=num_operacion+1,
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
            register_time = datetime.now().time()
        )

        db.session.add(trade) 

    def vender(self, args={}):
        num_operacion = self.__get_ult_num_operacion(self.order.order_date.year)
        
        opers_con_saldo = self.__obt_operaciones_saldo()
        for oper in opers_con_saldo:
            num_operacion+=1
            self.__vender(oper, num_operacion)

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

    def __get_ult_num_operacion(self, anyo=0):
        result = db.session.query(
            func.max(StockTrade.num_operacion).label("num_operacion")
        ).\
        filter(extract('year',StockTrade.trade_date) == anyo).first()

        num_operacion = 0
        if result is not None and result.num_operacion is not None:
            num_operacion = result.num_operacion

        return num_operacion

class BuscadorOperaciones:
    def __init__(self):
        pass

    def obt_list(self, args={}):
        try:
            query = db.session.query(
                StockTrade.id,
                StockTrade.num_operacion,
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
            data = query.all()
            return Response(raw_data=data).get()
        except Exception as e:
            return Response().from_exception(e)
