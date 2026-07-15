import requests
from app import app
from datetime import datetime
import logging

BASE_ENDPOINT = app.config["MARKETDATA_ENDPOINT"]
TOKEN = app.config["MARKETDATA_API_TOKEN"]

logger = logging.getLogger(__name__)


class MarketDataAPI:
    def get_bulk_quotes(self, cod_symbol_list=[]):
        cod_symbol_list_as_string = ",".join(cod_symbol_list)

        headers = {"Accept": "application/json", "Authorization": f"Bearer {TOKEN}"}

        endpoint = (
            f"{BASE_ENDPOINT}stocks/bulkquotes/?symbols={cod_symbol_list_as_string}"
        )
        logger.info(f"bulkquotes: start_date: {str(datetime.now())}")
        response = requests.request("GET", endpoint, headers=headers)
        logger.info(f"bulkquotes: end_date: {str(datetime.now())}")
        result = response.json()
        return result

    def quote(self, cod_symbol):
        headers = {"Accept": "application/json", "Authorization": f"Bearer {TOKEN}"}

        endpoint = f"{BASE_ENDPOINT}stocks/quotes/{cod_symbol}/?extended=false"
        response = requests.request("GET", endpoint, headers=headers)
        result = response.json()
        return result

    def get_options_chain(self, cod_subyacente=None, fch_expiracion=None):
        url = f"{app.config['MARKETDATA_ENDPOINT']}/options/chain/{cod_subyacente}/"

        headers = {"Content-Type": "application/json"}
        params = {"token": app.config.get("MARKETDATA_API_TOKEN")}

        if fch_expiracion is not None:
            params["expiration"] = fch_expiracion.isoformat()

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        contratos = []
        for index, cod_symbol in enumerate(data.get("optionSymbol"), start=0):
            contratos.append(
                {
                    "optionSymbol": cod_symbol,
                    "underlying": data["underlying"][index],
                    "expiration": data["expiration"][index],
                    "strike": data["strike"][index],
                    "side": data["side"][index],
                }
            )

        return contratos

    @staticmethod
    def stock_prices(cod_symbol_list=[]):
        cod_symbol_list_as_string = ",".join(cod_symbol_list)
        headers = {"Accept": "application/json", "Authorization": f"Bearer {TOKEN}"}

        endpoint = f"{BASE_ENDPOINT}stocks/prices/?symbols={cod_symbol_list_as_string}"
        response = requests.request("GET", endpoint, headers=headers)
        result = response.json()
        return result

    @staticmethod
    def candles(cod_symbol, interval="1D", start_date="", end_date=""):
        headers = {"Accept": "application/json", "Authorization": f"Bearer {TOKEN}"}

        endpoint = f"{BASE_ENDPOINT}/stocks/candles/{interval}/{cod_symbol}/?from={start_date}&to={end_date}"
        response = requests.request("GET", endpoint, headers=headers)
        result = response.json()
        return result
