import requests, json

class Datapoints:
    def __init__(self):
        pass

    def get(self):
        result = requests.get("https://cloud.iexapis.com/stable/data-points/aapl?token=sk_fb6bb5e2d78e4a7d95d39e1dc03e6cf5")

        data = json.loads(result.text)

        for element in data:
            print(element["key"])
        
