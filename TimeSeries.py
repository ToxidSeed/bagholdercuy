import requests, json, datetime

class TimeSeries:
    def __init__(self):
        pass

    def get(self):
        #result = requests.get("https://cloud.iexapis.com/stable/time-series?token=sk_fb6bb5e2d78e4a7d95d39e1dc03e6cf5")
        result = requests.get("https://cloud.iexapis.com/stable/time-series/HISTORICAL_PRICES/AAPL?token=sk_fb6bb5e2d78e4a7d95d39e1dc03e6cf5")

        data = json.loads(result.text)

        for element in data:
            humandate = datetime.datetime.fromtimestamp(element["date"]/1000)
            print(humandate)