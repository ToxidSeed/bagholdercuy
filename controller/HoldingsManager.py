from app import app, db
import requests, json, csv
from common.api.MarketAPI import MarketAPI
from model.StockTrade import StockTrade
from model.StockData import StockData
from controller.DataManager import DataManager
from sqlalchemy import func
import common.Converter as Converter
from common.Response import Response
from common.StatusMessage import StatusMessage
from common.api.iexcloud import iexcloud
from pytz import HOUR, timezone
from datetime import datetime, date
from config.general import APP_DEC_PREC, MARKET_API_LIST

#from controller.StockDataProvider import StockDataProvider
import common.Markets as Markets
from controller.Base import Base


class HoldingsManager(Base):
    def __init__(self):
        super().__init__(__name__)
        self.status = StatusMessage()                

    def __get_active_holdings(self):
        holdings = db.session.query(
            StockTrade.symbol,
            StockTrade.asset_type,
            func.min(StockTrade.trade_date).label('holding_since'),
            func.sum(StockTrade.imp_accion).label("sum_imp_accion"),
            func.sum(StockTrade.imp_operacion).label("sum_imp_operacion"),
            func.sum(StockTrade.imp_accion_origen).label("sum_imp_accion_origen"),
            func.sum(StockTrade.saldo).label("sum_shares_balance"),
            func.min(StockTrade.trade_date).label("min_trade_date")
        ).filter(
            StockTrade.saldo != 0
        ).group_by(StockTrade.symbol)\
        .all()

        return holdings

    def get_list(self, args={}):                             
        active_holdings = self.__get_active_holdings()

        #shares_balance * current_price
        results = []
        for elem in active_holdings:       
            elem_dict = Converter.to_dict(elem) 
            vals_adic = self.default_bridge.calc_val_adic(elem)
            elem_dict.update(vals_adic)
            results.append(elem_dict)        
        return Response().from_raw_data(results)

    def __options_price(self,holding={},quote=None):
        sum_shares_balance = float(holding["sum_shares_balance"])
        sum_buy_price_per_trade = float(holding["sum_buy_price_per_trade"])
        avg_buy_price = round(sum_buy_price_per_trade/sum_shares_balance,APP_DEC_PREC)
        
        market_value = round((sum_shares_balance * quote.close)*100, APP_DEC_PREC)
        prev_close = quote.open
        daily_change = round(((quote.close - prev_close)/prev_close)*100,APP_DEC_PREC)

        total_change = round(((quote.close - avg_buy_price)/avg_buy_price)*100,APP_DEC_PREC)
        total_pl = round(market_value - sum_buy_price_per_trade,APP_DEC_PREC)

        #holding["sum_trade_buy_price"] = "{0}(x100)".format(holding["sum_trade_buy_price"]) 
        holding["sum_shares_balance"] = "{0}(x100)".format(int(holding["sum_shares_balance"]))
        holding["avg_buy_price"] = "{:.2f}".format(avg_buy_price)
        holding["daily_change"] = "{:.2f}".format(daily_change)
        holding["total_change"] = "{:.2f}".format(total_change)
        holding["total_pl"] = "{:.2f}".format(total_pl)
        holding["last_price_date"] = quote.price_date            
        holding["last_price"] = "{:.2f}".format(quote.close)
        holding["market_value"] = "{:.2f}".format(market_value)

        return holding

    def __stocks_price(self, holding={}, quote=None):
        sum_shares_balance = holding["sum_shares_balance"]
        sum_buy_price_per_trade = holding["sum_buy_price_per_trade"]
        avg_buy_price = round(sum_buy_price_per_trade/sum_shares_balance,APP_DEC_PREC)
        
        market_value = round(sum_shares_balance * quote.close, APP_DEC_PREC)
        prev_close = quote.prev_close
        daily_change = round(((quote.close - prev_close)/prev_close)*100,APP_DEC_PREC)

        total_change = round(((quote.close - avg_buy_price)/avg_buy_price)*100,APP_DEC_PREC)
        total_pl = round(market_value - sum_buy_price_per_trade,APP_DEC_PREC)

        holding["avg_buy_price"] = avg_buy_price
        holding["daily_change"] = daily_change
        holding["total_change"] = total_change
        holding["total_pl"] = total_pl
        holding["last_price_date"] = quote.price_date            
        holding["last_price"] = quote.close
        holding["market_value"] = market_value

        return holding

class ResumenController(Base):
    def __init__(self):
        pass

    

class iexcloud_bridge:
    def __init__(self):
        #self.apiobj = MarketAPI().get_api()
        self.api = iexcloud()

    def calc_val_adic(self, holding=None):        
        vals = {}
        if holding.asset_type in ["equity","etf"]:
            vals = self.__calc_val_equity(holding)
        if holding.asset_type == "opciones":
            vals = self.__calc_val_opciones(holding)

        return vals

    def __calc_val_opciones(self, holding=None):
        pass

    def __calc_val_equity(self, holding=None):        
        imp_open, imp_close,prev_close, close_date = self.get_quote(holding.symbol.upper())

        sum_shares_balance = float(holding["sum_shares_balance"])
        sum_imp_operacion = float(holding["sum_imp_operacion"])            
        avg_buy_price = round(sum_imp_operacion/sum_shares_balance,APP_DEC_PREC)        
        market_value = round(sum_shares_balance * imp_close, APP_DEC_PREC)        
        daily_change = round(((imp_close - prev_close)/prev_close)*100,APP_DEC_PREC)
        total_change = round(((imp_close - avg_buy_price)/avg_buy_price)*100,APP_DEC_PREC)
        total_pl = round(market_value - sum_imp_operacion,APP_DEC_PREC)
        
        vals = {
            "avg_buy_price" : avg_buy_price,
            "daily_change" : daily_change,
            "total_change":total_change,
            "total_pl":total_pl,
            "last_price_date": close_date,
            "last_price":imp_close,
            "market_value":market_value
        }

        return vals

    def get_quote(self, symbol=""):
        args = {
            "symbol":symbol
        }

        print(datetime.now())
        quote = self.api.get_quote(args)
        print(datetime.now())

        imp_open = quote.get("open")
        if imp_open is None:
            imp_open = quote.get("iexOpen")

        imp_close = quote.get("close")        
        if imp_close is None:
            imp_close = quote.get("iexRealtimePrice")
        
        imp_prev_close = quote.get("previousClose")

        close_date = quote.get("closeTime")
        if close_date is None:
            close_date = quote.get("latestUpdate")

        return (imp_open, imp_close,imp_prev_close, close_date)


        
        


