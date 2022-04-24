import config as CONFIG

class MarketAPI:
    def __init__(self, apiname=CONFIG.MARKET_API):
        self.modulename = CONFIG.MARKET_API_LIST[apiname] 
        self.classname = CONFIG.MARKET_API_LIST[apiname]
        self.apiname = apiname        

    def get_api(self):
        mod = __import__("common.api."+self.modulename,fromlist=[None])
        return getattr(mod,self.classname)()


