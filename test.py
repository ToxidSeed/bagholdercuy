import requests, json
from datetime import date
#response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=VJKI9C3OGUWBXVXK")
#print(response.json())

#result = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=VJKI9C3OGUWBXVXK")
#print(result.json())

"""
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/aapl/prices?token=a114a15463338bba4a974b91ca4602c103d5d82e", headers=headers)
print(requestResponse.json())
"""

"""
result = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?start_date=1985-05-01&end_date=1997-07-01&order=asc&column_index=4&collapse=quarterly&transformation=rdiff")
print(result)
"""

"""
result = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/FB/data.json?api_key=kQ3LNi9AzAyc-Soz4pJr")
print(result.text)
"""

#path = "data/time_series_{}.json".format(date.today())
"""
result = requests.get("https://cloud.iexapis.com/stable/time-series?token=sk_fb6bb5e2d78e4a7d95d39e1dc03e6cf5")
path = "data/time_series_{}.json".format(date.today())
with open(path, 'w') as f:
    f.write(result.text)
"""

"""
with open(path,'r') as f:
    text = f.read()    

data = json.loads(text)

for element in data:
    identifier = element["id"]
    print(identifier)
"""

"""
from Datapoints import Datapoints
dp = Datapoints()
dp.get()"""

from TimeSeries import TimeSeries
ts = TimeSeries()
ts.get()