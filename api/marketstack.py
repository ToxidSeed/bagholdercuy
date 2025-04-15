import requests
from app import app
from datetime import datetime
import logging

BASE_ENDPOINT = app.config["MARKETSTACK_ENDPOINT"]
TOKEN = app.config["MARKETSTACK_API_TOKEN"]

logger = logging.getLogger(__name__)

class MarketStackAPI:
    def get_intraday_latest(self, cod_symbol):
        endpoint = f"{BASE_ENDPOINT}tickers/{cod_symbol}/intraday/latest?access_key=5162169157e08cd43335ea706a487027"

        response = requests.get(
            endpoint
        )

        response = requests.request("GET", endpoint)
        return response.json()