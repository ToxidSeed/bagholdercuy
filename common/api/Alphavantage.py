from app import app, db
import requests
from datetime import datetime, date

import config as CONFIG


class Alphavantage:
    def __init__(self):
        self.default_endpoint = "https://www.alphavantage.co/query"
        self.key = app.config["ALPHAVANTAGE_KEY"]        
        pass    

    def fx_faily(self, params={}):
        params["function"] = "FX_DAILY"
        params["apikey"] = CONFIG.ALPHAVANTAGE_KEY

        response = requests.get(CONFIG.ALPHAVANTAGE_ENDPOINT, params=params)
        data = response.json()
        return data

    def get_daily_data_since(self, symbol, since):
        outputsize = "compact"
        if since == "":
            outputsize = "full"

        function = "TIME_SERIES_DAILY"
        params = {
            "function":function,            
            "symbol":symbol,
            "outputsize":outputsize,
            "apikey":CONFIG.ALPHAVANTAGE_KEY
        }        

        response = requests.get(self.default_endpoint, params=params)
        data = response.json()
        series = data["Time Series (Daily)"]

        new_quote = None
        last_quote = None
        rownumber = 0
        if since == "":
            since_date = date.min
        else:
            since_date = date.fromisoformat(since)

        result = []
        for price_date, raw_quote in series.items():
            if date.fromisoformat(price_date) > since_date: 
                rownumber+=1
                new_quote = Quote(
                    price_date = price_date,
                    symbol = symbol,                    
                    open = float(raw_quote["1. open"]),
                    high = float(raw_quote["2. high"]),
                    low = float(raw_quote["3. low"]),
                    close= float(raw_quote["4. close"])
                )

                #since Alphavantage returns in descending order
                if rownumber == 1:
                    last_quote = new_quote                
                result.append(new_quote)

        #returning the last quote loaded
        return (last_quote, result)

    def get_last_intraday(self, args={}):
        symbol = args["symbol"]
        function = "TIME_SERIES_INTRADAY"
        interval = "1min"

        #get data from API        
        params = {
            "function":function,
            "adjusted":"false",
            "symbol":symbol,
            "outputsize":"compact",
            "apikey":self.key,
            "interval":interval
        }        

        response = requests.get(self.default_endpoint, params=params)
        data = response.json()
        series_key = "Time Series ({})".format(interval)
        series = data[series_key]        
        price_date, data = next(iter(series.items()))
        quote = Quote(
            symbol=symbol,
            price_date=price_date,
            open=float(data["1. open"]),
            high=float(data["2. high"]),
            low=float(data["3. low"]),
            close=float(data["4. close"]),
            volume=float(data["5. volume"])
        )
                
        return quote

    def get_last_daily_quote(self, args={}):
        function = "TIME_SERIES_DAILY"
        symbol = args["symbol"]
        #date_price = args["date_price"]

        params = {
            "function":function,            
            "symbol":symbol,
            "outputsize":"compact",
            "apikey":self.key
        }

        response = requests.get(self.default_endpoint, params=params)
        data = response.json()
        series = data["Time Series (Daily)"]

        key, data = next(iter(series.items()))
        quote = Quote(
            symbol=symbol,
            price_date=key,
            open=float(data["1. open"]),
            high=float(data["2. high"]),
            low=float(data["3. low"]),
            close=float(data["4. close"]),
            volume=float(data["5. volume"])
        )
                
        return quote

    def time_series_weekly_adjusted(self, args={}):
        function = "TIME_SERIES_WEEKLY_ADJUSTED"
        symbol = args["symbol"]

        params = {
            "function":function,            
            "symbol":symbol,            
            "apikey":CONFIG.ALPHAVANTAGE_KEY
        }
        response = requests.get(CONFIG.ALPHAVANTAGE_ENDPOINT,params)
        data = response.json()
        series = data["Weekly Adjusted Time Series"]
        return series

    def time_series_monthly_adjusted(self, args={}):
        function = "TIME_SERIES_MONTHLY_ADJUSTED"
        symbol = args["symbol"]

        params = {
            "function":function,            
            "symbol":symbol,            
            "apikey":CONFIG.ALPHAVANTAGE_KEY
        }

        response = requests.get(CONFIG.ALPHAVANTAGE_ENDPOINT,params)
        data = response.json()
        series = data["Monthly Adjusted Time Series"]
        return series
        