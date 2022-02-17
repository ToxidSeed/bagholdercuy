from app import app, db
import requests, json, csv
from model.StockTrade import StockTrade
from model.StockData import StockData
from controller.DataManager import DataManager
from sqlalchemy import func
import common.Converter as Converter
from common.Response import Response
from common.StatusMessage import StatusMessage
from pytz import HOUR, timezone
from datetime import datetime, date
from config import APP_DEC_PREC
#from controller.StockDataProvider import StockDataProvider
import common.Markets as Markets



class HoldingsManager:
    def __init__(self):
        self.status = StatusMessage()        

    def __get_active_holdings(self):
        holdings = db.session.query(
            StockTrade.symbol,
            StockTrade.asset_type,
            func.min(StockTrade.trade_date).label('holding_since'),
            func.sum(StockTrade.buy_price).label("sum_buy_price"),
            func.sum(StockTrade.buy_price_per_trade).label("sum_buy_price_per_trade"),
            func.sum(StockTrade.sell_price).label("sum_sell_price"),
            func.sum(StockTrade.shares_balance).label("sum_shares_balance"),
            func.min(StockTrade.trade_date).label("min_trade_date")
        ).filter(
            StockTrade.shares_balance != 0
        ).group_by(StockTrade.symbol)\
        .all()

        return holdings

    def get_list(self, args={}):
        dm = DataManager()
        
        active_holdings = self.__get_active_holdings()

        #shares_balance * current_price
        results = []
        for elem in active_holdings:       
            elem_dict = Converter.to_dict(elem) 

            quote, error = dm.get_last_quote(elem.symbol)
            if error is not None:
                return Response().from_error(error)
            else:      
                if quote is None:
                    continue

                if quote.asset_type == "options":
                    price = self.__options_price(elem_dict,quote)
                    results.append(price)
                    continue

                if quote.asset_type == "Stock":
                    price = self.__stocks_price(elem_dict,quote)
                    results.append(price)
                    continue
                

        return Response(input_data=results).get()

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
        sum_shares_balance = float(holding["sum_shares_balance"])
        sum_buy_price_per_trade = float(holding["sum_buy_price_per_trade"])            
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

