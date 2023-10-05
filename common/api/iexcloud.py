import requests
from app import app, db
from config.general import IEXCLOUD_ENDPOINT, IEXCLOUD_KEY
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
        
    def get_contracts(self, cod_symbol, fch_expiracion):        
        endpoint = "{0}/ref-data/options/symbols/{1}/{2}".format(self.base_endpoint,cod_symbol, fch_expiracion)
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

    def get_option_eod_data(self, cod_opcion):
        cod_opcion = cod_opcion

        strike = int(cod_opcion[-6:])/1000
        sentido = 'call' if cod_opcion[-9:-8] == 'C'else 'put'
        expiracion = cod_opcion[-17:-9]
        cod_subyacente = cod_opcion[:-17]        
        
        endpoint = "{0}/stock/{1}/options/{2}".format(self.base_endpoint,cod_subyacente, expiracion)
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "token":self.key
        }

        rsp = requests.get(endpoint,params=params, headers=headers)
        return rsp.json()

    def get_historical_prices(self, args={}):      

        PROFUNDIDAD = {
            "YTD":"ytd",
            "MAX":"max",
            "MESACTUAL":"1m",
            "ULT3MESES":"3m",    
            "ULT6MESES":"6m",    
            "ULT1ANYO":"1y"
        }

        api_range = PROFUNDIDAD.get(args.get("range")).lower()
        symbol = args.get("symbol")
        
        endpoint = "{0}/stock/{1}/chart/{2}".format(self.base_endpoint, symbol, api_range)
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
                   

        endpoint = "{0}/fx/historical/".format(IEXCLOUD_ENDPOINT)
        headers = {
            'Content-Type': 'application/json'
        }

        
        params["token"] = IEXCLOUD_KEY
        params["symbols"] = "USDPEN"

        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()

        return data
        
    def symbols(self, params={}):
        endpoint = "{0}/ref-data/symbols".format(IEXCLOUD_ENDPOINT)
        headers = {
            'Content-Type': 'application/json'
        }

        params["token"] = IEXCLOUD_KEY
        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()
        return data

    def etf_symbols(self, params={}):
        endpoint = "{0}/ref-data/mutual-funds/symbols".format(IEXCLOUD_ENDPOINT)
        headers = {
            'Content-Type': 'application/json'
        }

        params["token"] = IEXCLOUD_KEY
        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()
        return data


