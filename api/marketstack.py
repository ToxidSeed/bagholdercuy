import requests
from app import app
from datetime import datetime
import logging

BASE_ENDPOINT = app.config["MARKETSTACK_ENDPOINT"]
TOKEN = app.config["MARKETSTACK_API_TOKEN"]

logger = logging.getLogger(__name__)

class MarketStackAPI:
    def get_intraday_latest(self, cod_symbol):
        endpoint = f"{BASE_ENDPOINT}tickers/{cod_symbol}/intraday/latest?access_key={TOKEN}"

        response = requests.get(
            endpoint
        )

        response = requests.request("GET", endpoint)
        return response.json()

    @staticmethod
    def get_historical_data(symbols, fch_desde, fch_hasta):
        endpoint = f"{BASE_ENDPOINT}eod"
 
        params = {
            'access_key': TOKEN,
            'symbols':symbols,
            'date_from': fch_desde,
            'date_to':fch_hasta,
            'limit':1000
        }

        response = requests.get(
            endpoint,
            params=params
        )
        
        return response.json()

    @staticmethod
    def get_ticketlist(search=""):
        endpoint = f"{BASE_ENDPOINT}tickerslist"
 
        params = {
            'access_key': TOKEN
        }

        if search:
            params["search"] = search

        response = requests.get(
            endpoint,
            params=params
        )
        
        return response.json()
