import requests
from app import app, db
import config as config
from common.StatusMessage import StatusMessage
from datetime import datetime, date
from common.Error import Error
from common.Response import Response
from common.api.Quote import Quote

class iexcloud:
    def __init__(self):
        self.status = StatusMessage()
        self.base_endpoint = "https://cloud.iexapis.com/stable"
        self.key = app.config["IEXCLOUD_KEY"]                
        pass

    def get_last_intraday(self, args={}):
        symbol = args["symbol"]
        headers = {
            'Content-Type': 'application/json'
        }
        params = {         
            "token":self.key
        }

        endpoint = "{0}/stock/{1}/quote".format(self.base_endpoint, symbol)

        response = requests.get(endpoint,params=params, headers=headers)
        result = response.json()
        latestUpdate = datetime.fromtimestamp(int(result["latestUpdate"]/1000)).date()
             
        quote = Quote(
            symbol=symbol,
            price_date=latestUpdate,
            open=result["open"],
            high=result["high"],
            low=result["low"],
            close=result["close"],            
            latest_price = result["latestPrice"],
            volume=result["latestVolume"]
        )
        return quote    
        
    def get_last_quote(self, args={}):
        error = Error()
        symbol = ""
        if "symbol" not in args:
            error.add("iexcloud bind, symbol is mandatory")
        else:
            symbol = args["symbol"]

        if "asset_type" not in args:
            error.add("asset type is mandatory")

        asset_type = args["asset_type"].upper()
        
        error.msg = "Se han encontrado errores al obtnener la última cotización para el symbol {} : ".format(symbol)

        if len(error.errors) > 0:
            return (None, error)
        
        if asset_type in ["STOCK","ETF"]:
            return (self.get_quote(args), None)

        if asset_type == "OPTIONS":
            return (self.get_option_eod_data(args), None)
        
    def get_contracts(self, symbol=""):
        #symbol = args["symbol"]
        endpoint = "{0}/ref-data/options/symbols/{1}".format(self.base_endpoint,symbol)
        headers = {
            'Content-Type': 'application/json'
        }
        params = {         
            "token":self.key
        }
        requestResponse = requests.get(endpoint,params=params, headers=headers)
        return requestResponse.json()

    def get_quote(self, args={}):
        
        symbol = args["symbol"]
        headers = {
            'Content-Type': 'application/json'
        }
        params = {         
            "token":self.key
        }

        endpoint = "{0}/stock/{1}/quote".format(self.base_endpoint, symbol)

        response = requests.get(endpoint,params=params, headers=headers)
        result = response.json()

        return result

    def get_option_eod_data(self, args={}):
        contract_symbol = args["symbol"]
        jsonrsp = False
        if "json" in args and args["json"] == True:
            jsonrsp = True

        endpoint = "{0}/options/{1}/chart".format(self.base_endpoint,contract_symbol)
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "token":self.key
        }

        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()

        elem = next(iter(data))
        last_trade_date = elem["lastTradeDate"]
        last_update = date.today()      

        quote = Quote(
            asset_type="options",
            symbol=contract_symbol,
            price_date=last_trade_date,
            open=elem["open"],
            high=elem["high"],
            low=elem["low"],
            close=elem["close"],
            volume=elem["volume"],
            last_update=last_update,
            last_price_date=last_trade_date
        )

        if jsonrsp:
            return Response(input_data=quote).get()

        return quote

    def get_historical_prices(self, symbol):        
        endpoint = "{0}/stock/{1}/chart/max".format(self.base_endpoint, symbol)
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "token":self.key
        }        

        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()

        return data
            
    def fx_historical(self, params={}):        

        endpoint = "{0}/fx/historical/".format(config.IEXCLOUD_ENDPOINT)
        headers = {
            'Content-Type': 'application/json'
        }

        params["token"] = config.IEXCLOUD_KEY

        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()

        return data
        
    def symbols(self, params={}):
        endpoint = "{0}/ref-data/symbols".format(config.IEXCLOUD_ENDPOINT)
        headers = {
            'Content-Type': 'application/json'
        }

        params["token"] = config.IEXCLOUD_KEY
        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()
        return data

    def etf_symbols(self, params={}):
        endpoint = "{0}/ref-data/mutual-funds/symbols".format(config.IEXCLOUD_ENDPOINT)
        headers = {
            'Content-Type': 'application/json'
        }

        params["token"] = config.IEXCLOUD_KEY
        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()
        return data


