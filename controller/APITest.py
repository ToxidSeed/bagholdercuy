from common.api.Alphavantage import Alphavantage
from api.marketstack import MarketStackAPI

class APITest:
    def __init__(self):
        pass

    def fx_daily(self, args={}):
        results = Alphavantage().fx_faily(params=args)
        return results

class MarketStackAPITest:
    AUTH_REQUIRED=False
    def __init__(self):
        pass

    def get_ticketlist(self, args={}):
        search = args.get("search")
        results = MarketStackAPI.get_ticketlist(search)
        return results



