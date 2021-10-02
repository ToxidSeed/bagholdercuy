from re import S
from app import app, db
from model.StockTrade import StockTrade
from model.StockSymbol import StockSymbol
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
            self.__buy(symbol, args)
            
        if trade_type == "S":            
            self.__sell(symbol, args)

        try:            
            db.session.commit()
            return Response(msg="Orden de compra ejecutada").get()
        except:
            return Response(success=False,msg="Error al guardar la orden de compra").get()

    def __buy(self, symbol, args):
        buy_order_shares = float(args["shares_quantity"])
        buy_order_shares_balance = self.__buy_holdings(symbol, buy_order_shares, args)
        self.__buy_with_no_holdings(symbol, buy_order_shares_balance, args)

    def __buy_holdings(self, symbol, order_shares, args):
        shares = 0
        trade_date = date.fromisoformat(args["order_date"])
        price_per_share = args["price_per_share"]
        trade_month = trade_date.month

        holdings = db.session.query(
            StockTrade
        ).filter(
            #StockTrade.asset_type == "stocks",
            StockTrade.shares_balance > 0,
            StockTrade.symbol == symbol,
            StockTrade.trade_type == 'S'
        ).order_by(StockTrade.trade_date, StockTrade.id).all()

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

            sell_order = StockTrade(
                symbol=symbol,
                trade_type = args["order_type"],
                asset_type = args["asset_type"],
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

            db.session.add(sell_order)
        return order_shares

    def __buy_with_no_holdings(self, symbol, order_shares, args={}):        
        asset_type = args["asset_type"]
        trade_date = date.fromisoformat(args["order_date"])
        price_per_share = float(args["price_per_share"])
        price_per_trade = float(order_shares * price_per_share)
        trade_month = trade_date.month
        premium = 0

        if asset_type == self.ASSET_TYPE_OPTIONS:              
            premium = order_shares * price_per_share
        

        trade = StockTrade(
            symbol=symbol,
            trade_type = args["order_type"],
            asset_type = args["asset_type"],
            shares_quantity = order_shares,
            shares_balance = order_shares,
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

    def __sell(self, symbol, args):                       
        sell_order_shares = args["shares_quantity"]
        sell_order_shares_balance = self.__sell_holdings(symbol, sell_order_shares, args)
        self.__sell_with_no_holdings(symbol, sell_order_shares_balance, args)

    def __sell_with_no_holdings(self, symbol, sell_order_shares, args={}):
        if sell_order_shares == 0:
            print("sell with no holdings, sell order shares is zero")
            return

        asset_type = args["asset_type"]
        trade_date = date.fromisoformat(args["order_date"])
        price_per_share = float(args["order_price"])
        trade_month = trade_date.month
        premium = 0

        if asset_type == self.ASSET_TYPE_OPTIONS:              
            premium = sell_order_shares * price_per_share
        
        trade = StockTrade(
            symbol=symbol,
            trade_type = args["order_type"],
            asset_type = args["asset_type"],
            shares_quantity = sell_order_shares,
            shares_balance = sell_order_shares,
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

    def __sell_holdings(self, symbol, sell_order_shares, args):
        shares = 0
        trade_date = date.fromisoformat(args["order_date"])
        price_per_share = args["price_per_share"]
        trade_month = trade_date.month

        #get current holdings and balance
        holdings = db.session.query(
            StockTrade
        ).filter(
            #StockTrade.asset_type == "stocks",
            StockTrade.shares_balance > 0,
            StockTrade.symbol == symbol,
            StockTrade.trade_type == 'B'
        ).order_by(StockTrade.trade_date, StockTrade.id).all()

        for trade in holdings:
            if sell_order_shares == 0:
                break

            holding_shares_balance = float(trade.shares_balance)
            if holding_shares_balance < sell_order_shares:
                sell_order_shares = sell_order_shares - holding_shares_balance
                shares = holding_shares_balance

                #update the balance
                trade.shares_balance = 0

            if holding_shares_balance > sell_order_shares:
                shares = sell_order_shares
                #update the balance
                trade.shares_balance = holding_shares_balance - sell_order_shares
                sell_order_shares = 0


            if holding_shares_balance == sell_order_shares:
                shares = sell_order_shares
                sell_order_shares = 0
                #update the balance
                trade.shares_balance = 0           

            sell_order = StockTrade(
                symbol=symbol,
                trade_type = args["order_type"],
                asset_type = args["asset_type"],
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

            db.session.add(sell_order)
        return sell_order_shares

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
        