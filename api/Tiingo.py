import requests
from app import app

class Tiingo:
    def __init__(self):
        pass

    def last_price(self, args={}):
        tickers='ibm'
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "tickers":tickers,
            "token":app.config["TIINGO_KEY"]
        }
        requestResponse = requests.get("https://api.tiingo.com/iex/",params=params, headers=headers)
        return requestResponse.json()

    def historical_intraday(self, args={}):
        ticker='IBM'
        headers = {
            'Content-Type': 'application/json'
        }
        params = {            
            "token":app.config["TIINGO_KEY"],
            "startDate":"2021-07-09",
            "resampleFreq":"5min",
            "afterHours":"true"
        }
        requestResponse = requests.get("https://api.tiingo.com/iex/{}/prices/".format(ticker),params=params, headers=headers)
        return requestResponse.json()
        