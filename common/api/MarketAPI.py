from config.general import MARKET_API, MARKET_API_LIST

class MarketAPI:
    def __init__(self, apiname=MARKET_API):
        self.modulename = MARKET_API_LIST[apiname] 
        self.classname = MARKET_API_LIST[apiname]
        self.apiname = apiname        

    def get_api(self):
        mod = __import__("common.api."+self.modulename,fromlist=[None])
        return getattr(mod,self.classname)()


