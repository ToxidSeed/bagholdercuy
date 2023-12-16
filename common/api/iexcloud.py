import requests
from app import app, db
from config.app_constants import IEXCLOUD
from common.StatusMessage import StatusMessage
from datetime import datetime, date, timedelta
from common.Error import Error
from common.Response import Response
from common.api.Quote import Quote


class iexcloud:

    def __init__(self):
        self.status = StatusMessage()
        self.base_endpoint = "https://cloud.iexapis.com/stable"
        self.key = app.config["IEXCLOUD_KEY"]

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

        api_range = args.get("range").lower()
        symbol = args.get("symbol")
        
        endpoint = "{0}/stock/{1}/chart/{2}".format(self.base_endpoint, symbol, api_range)
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "token": self.key
        }        

        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()

        return data
            
    def fx_historical(self, params={}):     
                   

        endpoint = "{0}/fx/historical/".format(app.config.get("IEXCLOUD_ENDPOINT"))
        headers = {
            'Content-Type': 'application/json'
        }

        
        params["token"] = app.config.get("IEXCLOUD_KEY")
        params["symbols"] = "USDPEN"

        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()

        return data
        
    def symbols(self, params={}):
        endpoint = "{0}/ref-data/symbols".format(IEXCLOUD_ENDPOINT)
        headers = {
            'Content-Type': 'application/json'
        }

        params["token"] = app.config.get("IEXCLOUD_KEY")
        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()
        return data

    def etf_symbols(self, params={}):
        endpoint = "{0}/ref-data/mutual-funds/symbols".format(IEXCLOUD_ENDPOINT)
        headers = {
            'Content-Type': 'application/json'
        }

        params["token"] = app.config.get("IEXCLOUD_KEY")
        rsp = requests.get(endpoint,params=params, headers=headers)
        data = rsp.json()
        return data


class ProfundidadHelper:
    def get_fechas_equivalentes(self):
        equivalencias = {}
        for profundidad in IEXCLOUD.PROFUNDIDADES.value:
            fecha = self.profundidad_a_fecha(profundidad=profundidad)
            equivalencias[profundidad] = fecha

        return equivalencias

    def profundidad_a_fecha(self, profundidad):
        hoy = date.today()
        profundidad_config = {
            "5d": hoy - timedelta(5),
            "1m": hoy - timedelta(30),
            "3m": hoy - timedelta(90),
            "6m": hoy - timedelta(180),
            "ytd": date(hoy.year, hoy.month, 1),
            "1y": hoy - timedelta(365),
            "2y": hoy - timedelta(730),
            "5y": hoy - timedelta(1825),
            "max": None
        }
        return profundidad_config.get(profundidad)


class RangoHelper:

    def get_rango(self, fch_referencia):
        fechas_limite = self.get_fechas_limite()
        for rango_desde, fecha_desde, fecha_hasta in fechas_limite:
            if fecha_hasta > fch_referencia >= fecha_desde:
                return rango_desde, fecha_desde, fecha_hasta

        return None

    def get_fechas_limite(self):
        fechas = []
        for profundidad_desde, profundidad_hasta in IEXCLOUD.RANGOS.value:
            fecha_desde = self.get_fecha_limite_desde(profundidad_desde)
            fecha_hasta = self.get_fecha_limite_hasta(profundidad_hasta)
            fechas.append((profundidad_desde, fecha_desde, fecha_hasta))

        return fechas

    def get_fecha_limite_hasta(self, profundidad_hasta):
        profundidad_helper = ProfundidadHelper()

        hoy = date.today()
        if profundidad_hasta == "":
            return hoy

        fch_hasta = profundidad_helper.profundidad_a_fecha(profundidad=profundidad_hasta)
        return fch_hasta

    def get_fecha_limite_desde(self, profundidad_desde):
        profundidad_helper = ProfundidadHelper()

        if profundidad_desde == "max":
            return None

        fch_desde = profundidad_helper.profundidad_a_fecha(profundidad=profundidad_desde)
        return fch_desde



