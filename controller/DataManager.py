from common.Error import Error
from common.StatusMessage import StatusMessage
from model.OptionContract import OptionContract
from os import error, stat
from re import S
import requests, json, csv
from pytz import  timezone
from sqlalchemy import func
from datetime import date, datetime
from app import app, db
from model.StockData import StockData
from model.StockSymbol import StockSymbol
from model.OptionContract import OptionContract
from common.api.MarketAPI import MarketAPI, Stats
from common.api.Quote import Quote
from common.Response import Response
import common.Converter as Converter
import common.Markets as Markets
from datetime import datetime, date


class DataManager:
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
            return (None, Error)

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
        error = Stats().save(quote)        
        if error is not None:                       
            return (None, error)

        return (quote, None)

    def get_last_intraday(self, symbol="", current_date=""):
        stats = Stats().get(symbol)
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
        search_text="%{}%".format(args["symbol"])
        #asset_type =args["asset_type"]

        symbol_list = db.session.query(
            StockSymbol
        ).filter(
            StockSymbol.symbol.ilike(search_text)#,
            #StockSymbol.asset_type == asset_type
        ).all()

        return Response(input_data=symbol_list).get()

class Options:
    def __init__(self):
        pass

    def load_contracts(self, args={}):
        symbol=args["symbol"]
        #contracts = MarketApi().get_option_contracts(symbol=symbol)

        with open('tmp/CCLContracts.json') as f:
            contracts = f.read()

        contracts = json.loads(contracts)
        for elem in contracts:
            contract_symbol = elem["symbol"]
            sym = self.get_symbol(contract_symbol)
            if sym is None:
                ss = StockSymbol(
                    symbol = contract_symbol,
                    name = elem["description"],
                    exchange = elem["exchange"],
                    asset_type = "options"
                )
                db.session.add(ss)
                db.session.flush()

                #adding the details
                oc = OptionContract(
                    symbol_id = ss.id,
                    contract_size = elem["contractSize"],
                    currency = elem["currency"],
                    description = elem["description"],
                    expiration_date = elem["expirationDate"],
                    side = elem["side"],
                    strike = elem["strike"],
                    symbol = elem["symbol"],
                    underlying = elem["underlying"],
                    register_date = date.today()
                )
                db.session.add(oc)
        db.session.commit()

        return Response(msg="Se han cargado correctamente los symbol de los contratos para {}".format(symbol)).get()

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
            OptionContract
        ).filter(
            OptionContract.side == 'call',
            OptionContract.expiration_date >= date.today().isoformat(),
            OptionContract.underlying == symbol
        ).order_by(OptionContract.expiration_date, OptionContract.strike)

        if expiration_date != "":
            calls_query = calls_query.filter(OptionContract.expiration_date == expiration_date)
        if strike != "":
            calls_query = calls_query.filter(OptionContract.strike == strike)

        calls = calls_query.all()

        puts_query = db.session.query(
            OptionContract
        ).filter(
            OptionContract.side == 'put',
            OptionContract.expiration_date >= date.today().isoformat(),
            OptionContract.underlying == symbol
        ).order_by(OptionContract.expiration_date, OptionContract.strike)
        
        if expiration_date != "":
            puts_query = puts_query.filter(OptionContract.expiration_date == expiration_date)
        if strike != "":
            puts_query = puts_query.filter(OptionContract.strike == strike)

        puts = puts_query.all()
        
        calls = Converter.process_list(calls)
        puts = Converter.process_list(puts)
        
        return Response(input_data={"calls":calls,"puts":puts}).get() 
        
    def get_symbol(self, symbol=""):
        sym = db.session.query(
            StockSymbol
        ).filter(
            StockSymbol.symbol == symbol
        ).first()

        return sym




class ChangeFormatter:
    def __init__(self):
        pass

    def format(self, records):
        formatted_records = []

        for element in records:
            #row = model_to_dict(element)
            row = None

            open_price  = float(row["open"]) 
            close = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])

            change = round((close - open_price)/open_price ,2)*100
            change_high = round((high - open_price)/open_price,2)*100
            change_low  = round((low - open_price)/open_price,2)*100

            extra = {
                "change":change,
                "change_high":change_high,
                "change_low":change_low
            }

            row.update(extra)
             
            formatted_records.append(row)
        
        return formatted_records

