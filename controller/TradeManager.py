from re import S
from app import app, db
from model.StockTrade import StockTrade
from model.StockSymbol import StockSymbol
from model.OrderModel import OrderModel
from datetime import datetime, date, time
from common.Response import Response
from model.StockTrade import StockTrade
from common.Error import Error
from sqlalchemy import desc


class TradeManager:
    ASSET_TYPE_STOCKS = "stocks"
    ASSET_TYPE_OPTIONS = "options"
    
    def __init__(self):
        pass
    
    def order(self, args={}):
        error = self.__validate(args)
        if error is not None:
            return Response().from_error(error)

        order = Order().save(args)

        #asset type
        symbol = args["symbol"]
        asset_type = args["asset_type"]
        trade_type = args["order_type"]
        symbol_obj = db.session.query(StockSymbol).filter(
            StockSymbol.symbol == symbol
        ).first()

        #check existence of symbol
        if symbol_obj is None:
            return Response(msg="El symbol {} no existe".format(symbol)).get()

        #stock
        if trade_type == "B":            
            BuyManager(order).buy()
            
        if trade_type == "S":            
            SellManager(order).sell()

        try:            
            db.session.commit()
            return Response(msg="Orden de compra ejecutada").get()
        except:
            return Response(success=False,msg="Error al guardar la orden de compra").get()

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

class BuyManager:    
    def __init__(self, order:Order=None):
        self.order = order
        self.shares_order_balance = order.quantity

    def buy(self):
        shares = float(self.order.quantity)
        self.__buy_holdings()
        self.__buy_with_no_holdings()    
    
    def __get_holdings(self):
        db.session.query(
            StockTrade
        ).filter(
            #StockTrade.asset_type == "stocks",
            StockTrade.shares_balance > 0,
            StockTrade.symbol == self.order.symbol,
            StockTrade.trade_type == 'S'
        ).order_by(StockTrade.trade_date, StockTrade.id).all()

    def __buy_holdings(self):
        shares = 0
        trade_date = self.order.order_date
        price_per_share = self.order.price
        trade_month = trade_date.month

        holdings = self.__get_holdings()

        order_shares = self.shares_order_balance

        for trade in holdings:
            if order_shares == 0:
                break

            if trade.shares_balance < order_shares:
                order_shares = order_shares - trade.shares_balance
                shares = trade.shares_balance

                #update the balance
                trade.shares_balance = 0

            if trade.shares_balance > order_shares:
                shares = order_shares
                #update the balance
                trade.shares_balance = trade.shares_balance - order_shares

            if trade.shares_balance == order_shares:
                shares = order_shares
                #update the balance
                trade.shares_balance = 0           

            new_trade = StockTrade(
                symbol=self.order.symbol,
                trade_type = self.order.order_type,
                asset_type = self.order.asset_type,
                shares_quantity = shares,
                shares_balance = 0,
                premium = 0,
                trade_date = trade_date ,
                trade_month = trade_month,
                buy_price = price_per_share,
                buy_price_per_trade = shares * price_per_share,
                sell_price = 0,
                sell_price_per_trade = 0,
                realized_gl=0,
                register_date = datetime.now().date(),
                register_time = datetime.now().time()
            )

            db.session.add(new_trade)
        return order_shares

    def __buy_with_no_holdings(self):        
        asset_type = self.order.asset_type
        trade_date = date.fromisoformat(self.order.order_date)
        price_per_share = float(self.order.price)
        price_per_trade = float(self.shares_order_balance * price_per_share)

        trade_month = self.order.order_date.month
        premium = 0

        if asset_type == self.ASSET_TYPE_OPTIONS:              
            premium = self.shares_order_balance * price_per_share
        

        trade = StockTrade(
            symbol=self.order.symbol,
            trade_type = self.order.order_type,
            asset_type = self.order.asset_type,
            shares_quantity = self.shares_order_balance,
            shares_balance = self.shares_order_balance,
            premium = premium,
            trade_date = trade_date ,
            trade_month = trade_month,
            buy_price = price_per_share,
            buy_price_per_trade = price_per_trade,
            sell_price = 0,
            sell_price_per_trade = 0,
            realized_gl=0,
            register_date = datetime.now().date(),
            register_time = datetime.now().time()
        )

        db.session.add(trade) 

class SellManager:
    def __init__(self, order):
        self.order = order
        self.order_shares_balance = order.quantity

    def sell(self):                               
        self.__sell_holdings()
        self.__sell_with_no_holdings()

    def __sell_with_no_holdings(self):
        if self.order_shares_balance == 0:
            print("sell with no holdings, sell order shares is zero")
            return

        asset_type = self.order.asset_type
        trade_date = date.fromisoformat(self.order.order_type)
        price_per_share = float(self.order.price)
        trade_month = trade_date.month
        premium = 0

        if asset_type == self.ASSET_TYPE_OPTIONS:              
            premium = self.order_shares_balance * price_per_share
        
        trade = StockTrade(
            symbol=self.order.symbol,
            trade_type = self.order.order_type,
            asset_type = self.order.asset_type,
            shares_quantity = self.order_shares_balance,
            shares_balance = self.order_shares_balance,
            premium = premium,
            trade_date = trade_date ,
            trade_month = trade_month,
            buy_price = 0,
            buy_price_per_trade = 0,
            sell_price = price_per_share,
            sell_price_per_trade = premium,
            realized_gl=0,
            register_date = datetime.now().date(),
            register_time = datetime.now().time()
        )

        db.session.add(trade)        

    def __sell_holdings(self):
        shares = 0
        trade_date = self.order.order_date
        price_per_share = self.order.price
        trade_month = trade_date.month

        #get current holdings and balance
        holdings = db.session.query(
            StockTrade
        ).filter(
            #StockTrade.asset_type == "stocks",
            StockTrade.shares_balance > 0,
            StockTrade.symbol == self.order.symbol,
            StockTrade.trade_type == 'B'
        ).order_by(StockTrade.trade_date, StockTrade.id).all()

        for trade in holdings:
            if self.order_shares_balance == 0:
                break

            holding_shares_balance = float(trade.shares_balance)
            if holding_shares_balance < self.order_shares_balance:
                self.order_shares_balance = self.order_shares_balance - holding_shares_balance
                shares = holding_shares_balance

                #update the balance
                trade.shares_balance = 0

            if holding_shares_balance > self.order_shares_balance:
                shares = self.order_shares_balance
                #update the balance
                trade.shares_balance = holding_shares_balance - self.order_shares_balance
                self.order_shares_balance = 0


            if holding_shares_balance == self.order_shares_balance:
                shares = self.order_shares_balance
                self.order_shares_balance = 0
                #update the balance
                trade.shares_balance = 0           

            new_trade = StockTrade(
                symbol=self.order.symbol,
                trade_type = self.order.order_type,
                asset_type = self.order.asset_type,
                order_id = self.order.order_id,
                ref_trade_id = trade.id,
                shares_quantity = shares,
                shares_balance = 0,
                premium = 0,
                trade_date = trade_date ,
                trade_month = trade_month,
                buy_price = 0,
                buy_price_per_trade = 0,
                sell_price = price_per_share,
                sell_price_per_trade = shares * price_per_share,
                realized_gl=0,
                register_date = datetime.now().date(),
                register_time = datetime.now().time()
            )

            db.session.add(new_trade)
        