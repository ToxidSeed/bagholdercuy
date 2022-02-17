from common.Error import Error
from common.Response import Response
from common.api.MarketAPI import MarketAPI
from model.StockData import StockData
from app import db
from sqlalchemy.sql.expression import func
from datetime import date


class DataLoader:
    def __init__(self):
        self.elements = []
        self.stats = {}

    def load(self, args={}):
        error = self._val_entry_data(args)
        if error is not None:
            return Response().from_error(error).get() 

        market_api = MarketAPI()
        symbol = args["symbol"]
        method = args["method"]

        self.elements = market_api.get_historical_prices(symbol)

        if method == "replace":
            self.__replace(symbol)

        if method == "append":
            self.__append(symbol)

        db.session.commit()
    
        return Response(msg="Se ha cargado correctamente", extradata=self.stats).get()

    def _val_entry_data(self, args=None):
        error = Error()
        if args is None:
            error.add("No se ha enviado ningún parámetro")

        if "symbol" not in args:
            error.add("El argumento 'symbol' no ha sido enviado")

        if "method" not in args:
            error.add("El argumento 'method' no ha sido enviado")
        else:
            #valid methods
            method = args["method"]
            if method not in ["replace","append"]:
                error.add("El parámetro 'method' no tiene un valor permitido")

        if error.has_errors():
            return error

        return None

    def __replace(self, symbol=""):

        #delete all records from symbol
        StockData.query.filter(
            StockData.symbol == symbol
        ).delete()

        first_date = ""
        last_date = ""
        if len(self.elements) > 0:
            first_date = self.elements[0]["date"]
            last_date = self.elements[-1]["date"]
        
        for element in self.elements:                        
            db.session.add(
                StockData().from_iexcloud(element)
            )        

        self.stats ={
            "symbol":symbol,
            "ctd_records_loaded":len(self.elements),
            "first_date":first_date,
            "last_date":last_date
        }        

    def __append(self, symbol):

        #get last historical price
        last_loaded_quote = db.session.query(
            func.max(StockData.price_date)
        ).filter(
            StockData.symbol == symbol
        ).first()        

        first_date = ""
        last_date = ""
        if len(self.elements) > 0:                
            last_date = self.elements[-1]["date"]        

        ctd_records_loaded = 0
        for element in self.elements:
            if date.fromisoformat(element["date"]) > last_loaded_quote.price_date:
                ctd_records_loaded += 1
                if ctd_records_loaded == 1:
                    first_date = date.fromisoformat(element["date"])

                db.session.add(
                    StockData().from_iexcloud(element)
                )
        
        self.stats ={
            "symbol":symbol,
            "ctd_records_loaded":len(ctd_records_loaded),
            "first_date":first_date,
            "last_date":last_date
        }        
    