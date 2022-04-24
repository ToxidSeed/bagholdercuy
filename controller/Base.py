import config as CONFIG

class Base:
    def __init__(self, modulename=""):
        self.apiname = ""
        self.classname = ""
        self.modulename = modulename        
        self.default_bridge = self._get_bridge()        

    def _get_bridge(self,apiname=CONFIG.MARKET_API):        
        self.apiname = apiname
        self.classname = "{0}_bridge".format(CONFIG.MARKET_API_LIST[apiname])
        mod = __import__(self.modulename, fromlist=[None])
        obj = getattr(mod, self.classname)()
        return obj

