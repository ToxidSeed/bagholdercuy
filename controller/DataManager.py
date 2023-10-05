from tokenize import Ignore
from common.Error import Error
from common.StatusMessage import StatusMessage
from model.OptionContract import OptionContractModel
from os import error, stat
from re import S
import requests, json, csv
from pytz import  timezone
from sqlalchemy import func, true
from datetime import date, datetime
from app import app, db
from model.StockData import StockData
from model.StockSymbol import StockSymbol
#from common.api.MarketAPI import MarketAPI
from common.api.Quote import Quote
from common.Response import Response
import common.converter as converter
import common.Markets as Markets
from datetime import datetime, date

class DataManager:

    ASSET_TYPE_STOCK = "Stock"
    ASSET_TYPE_ETF = "ETF"
    ASSET_TYPE_OPTIONS = "options"

    def __init__(self):
        self.status = StatusMessage()        
        pass

    def get_last_quote(self, symbol=""):
        if symbol=="":
            self.status.error(msg="No se puede obtener el último precio porque no se ha indicado ningún símbolo")
            return

        symbolobj = db.session.query(
            StockSymbol
        ).filter(
            StockSymbol.symbol==symbol
        ).first()

        asset_type = symbolobj.asset_type

        quote, error = MarketAPI().get_last_quote({"symbol":symbol,"asset_type":asset_type})
        if error is not None:
            return (None, error)

        #current_date = date.today().isoformat()
        #quote = None

        #get stats
        #stats = self.__get_symbol_stats(symbol)

        """
        if Markets.is_intraday():
            quote = self.get_last_intraday(symbol=symbol, current_date=current_date)
        else:
            quote, msg, errors = self.get_last_daily_quote(symbol=symbol, current_date=current_date)
            if quote is None:
                return (None, msg, errors)
        """

        #guardar las estadisticas de la cotización
        #error = Stats().save(quote)        
        if error is not None:                       
            return (None, error)

        return (quote, None)

    """
    def get_last_intraday(self, symbol="", current_date=""):
        #stats = Stats().get(symbol)
        quote = MarketAPI().get_last_intraday({"symbol":symbol})

        last_update = ""
        if stats is not None:
            last_update = stats["last_update"]
        
        if last_update == current_date:
            quote.prev_close = stats["prev_close"]            
        else:
            #update quotes
            self.load_daily_data(symbol, last_update)
            #get prev quote
            prev_quote = self.get_prev_daily_quote(ref_date=current_date, symbol=symbol)
            quote.prev_close = float(prev_quote.close)
            quote.last_update = current_date
            #update stats
            self.__save_stock_stats(symbol, quote)

        return quote
    """
 
    def load_daily_data(self, symbol, since):
        last_loaded_date = self.get_max_loaded_daily_price(symbol)
        last_quote, quotes = MarketAPI().get_daily_data_since(symbol=symbol, since=since)   

        if last_quote is None:
            return None

        if date.fromisoformat(last_quote.price_date) > last_loaded_date:
            for item in quotes:
                sd = StockData(
                    symbol=item.symbol,
                    price_date=item.price_date,
                    frequency="daily",
                    open=item.open,
                    high=item.high,
                    low=item.low,
                    close=item.close,
                    volume=item.volume
                )
                db.session.add(sd)
            db.session.commit()
        return last_quote

    """
    def get_last_daily_quote(self, symbol="", current_date=""):
        stats = Stats().get(symbol)

        last_update = ""
        if stats is not None:
            last_update = stats["last_update"]
        
        quote = None
        if  last_update == current_date:            
            quote = Quote().from_stats(stats)            
        else:
            quote, error = MarketAPI().get_last_daily_quote({"symbol":symbol})
             
        return (quote, error)

    def __get_last_loaded_daily_quote(self, symbol=""):
        last_loaded_date = self.get_max_loaded_daily_price(symbol)

        sd = db.session.query(
            StockData
        ).filter(
            StockData.symbol == symbol,
            StockData.price_date == last_loaded_date
        ).first()

        return Quote().from_sd(sd)
    """

    def get_prev_daily_quote(self, ref_date="", symbol=""):
        max_price_date_obj = db.session.query(
            func.max(StockData.price_date).label("prev_price_date")
        ).filter(
            StockData.price_date < ref_date,
            StockData.symbol==symbol
        ).first()

        prev_quote = db.session.query(
            StockData
        ).filter(
            StockData.symbol == symbol,
            StockData.price_date == max_price_date_obj.prev_price_date
        ).first()

        return prev_quote

    def get_max_loaded_daily_price(self, symbol=""):
        result = db.session.query(
            func.max(StockData.price_date).label("max_price_date")
        ).filter(
            StockData.frequency=="daily",
            StockData.symbol==symbol
        ).first()

        max_price_date = result.max_price_date
        return max_price_date    

    @DeprecationWarning
    def load(self, args={}):
        symbol = args["symbol"]
        frequency = args["frequency"]

        last_price_result = self.get_last_price_date(symbol=symbol, frequency=frequency)

        function = "TIME_SERIES_{}".format(frequency.upper())        

        key = app.config["ALPHAVANTAGE_KEY"]
        endpoint = "https://www.alphavantage.co/query"
        params = {
            "function":function,
            "symbol":symbol,    
            "outputsize":"full",
            "apikey":key
        }

        #series key 
        series_key = {
            "daily":"Time Series (Daily)",
            "weekly":"Weekly Time Series"
        }


        response = requests.get(endpoint, params=params) 
        data = response.json()

        symbol = data["Meta Data"]["2. Symbol"]
        series = data[series_key[frequency]]

        for key, element in series.items():
            price_date = datetime.strptime(key, '%Y-%m-%d').date()
            if price_date > last_price_result["max_price_date"]: 
                stock_data_row = StockData(
                    symbol=symbol,
                    price_date=key,
                    frequency=frequency,
                    open=element["1. open"],
                    high=element["2. high"],
                    low=element["3. low"],
                    close=element["4. close"],
                    volume=element["5. volume"]
                )

                db.session.add(stock_data_row)
            else:
                break
        
        db.session.commit()
        msg = "Cargado correctamente hasta: {}".format(data["Meta Data"]["3. Last Refreshed"])
        return Response(msg=msg).get()

    def get_list(self, args):
        quotes = StockData.query.filter(
            StockData.price_date >= '2021-05-25'
        ).all()

        return Response(input_data=quotes, formatter=ChangeFormatter()).get()

class Symbol:
    def __init__(self):
        pass

    def load(self, args={}):

        key = app.config["ALPHAVANTAGE_KEY"]
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={}'.format(key)

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            rownumber = 0
            for row in my_list:
                rownumber+=1
                if rownumber >1:
                    symbol = StockSymbol(
                        symbol=row[0],
                        name=row[1],
                        exchange=row[2],
                        asset_type=row[3]
                    )

                    db.session.add(symbol)

            db.session.commit()

        return Response(msg="Se ha cargado correctamente los símbolos").get()

    def search(self, args={}):
        try:
            search_text="%{}%".format(args["symbol"])

            asset_type_args =args["asset_type"]
            asset_type = []

            if asset_type_args["stock"]:
                asset_type.append(DataManager.ASSET_TYPE_STOCK)

            if asset_type_args["etf"]:
                asset_type.append(DataManager.ASSET_TYPE_ETF)
            
            if asset_type_args["options"]:
                asset_type.append(DataManager.ASSET_TYPE_OPTIONS)

            symbol_list = db.session.query(
                StockSymbol
            ).filter(
                StockSymbol.symbol.ilike(search_text),
                StockSymbol.asset_type.in_(asset_type)
            ).all()
            return Response(raw_data=symbol_list).get()
        except Exception as e:
            return Response().from_exception(e)

    def get_options_chain(self, args={}):
        symbol=args["symbol"] #symbol is required
        expiration_date=""
        strike=""
        if "expiration_date" in args:
            expiration_date = args["expiration_date"]
        if "strike" in args:
            strike = args["strike"]
        #strike = args["strike"]

        calls_query = db.session.query(
            OptionContractModel
        ).filter(
            OptionContractModel.side == 'call',
            OptionContractModel.expiration_date >= date.today().isoformat(),
            OptionContractModel.underlying == symbol
        ).order_by(OptionContractModel.expiration_date, OptionContractModel.strike)

        if expiration_date != "":
            calls_query = calls_query.filter(OptionContractModel.expiration_date == expiration_date)
        if strike != "":
            calls_query = calls_query.filter(OptionContractModel.strike == strike)

        calls = calls_query.all()

        puts_query = db.session.query(
            OptionContractModel
        ).filter(
            OptionContractModel.side == 'put',
            OptionContractModel.expiration_date >= date.today().isoformat(),
            OptionContractModel.underlying == symbol
        ).order_by(OptionContractModel.expiration_date, OptionContractModel.strike)
        
        if expiration_date != "":
            puts_query = puts_query.filter(OptionContractModel.expiration_date == expiration_date)
        if strike != "":
            puts_query = puts_query.filter(OptionContractModel.strike == strike)

        puts = puts_query.all()
        
        calls = converter.process_list(calls)
        puts = converter.process_list(puts)
                
        return Response().from_raw_data({"calls":calls,"puts":puts})
            

