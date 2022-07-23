from common.api.Alphavantage import Alphavantage

class APITest:
    def __init__(self):
        pass

    def fx_daily(self, args={}):
        results = Alphavantage().fx_faily(params=args)
        return results
