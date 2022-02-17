from common.api.iexcloud import iexcloud
import common.Converter as Converter
from common.Error import Error
import json
import os

class MarketAPI:
    def __init__(self):
        self.engine = iexcloud()

    def get_last_quote(self, args={}):
        return self.engine.get_last_quote(args)

    def get_last_intraday(self, args={}):
        return self.engine.get_last_intraday(args)

    def get_last_daily_quote(self, args={}):
        return self.engine.get_last_daily_quote(args)

    def get_daily_data_since(self, symbol, since):
        return self.engine.get_daily_data_since(symbol, since)

    def load_dailydata(self, symbol, since):
        self.engine.__load_dailydata(symbol, since)

    def get_option_contracts(self, symbol=""):
        self.engine = iexcloud()
        return self.engine.get_contracts(symbol="")
    
    def get_historical_prices(self, symbol=""):
        return self.engine.get_historical_prices(symbol)


class Stats:
    tmp_path = "tmp/"

    def __init__(self):
        pass

    def save(self,quote):
        error = self.__val_quote(quote)
        if error is not None:
            return error            
        
        stats = Converter.to_dict(quote)

        filename = "{}{}.json".format(self.tmp_path,quote.symbol)
        with open(filename,'w') as f:
            f.write(json.dumps(stats))
        
    def get(self,symbol=""):
        filepath = "{}{}.json".format(self.tmp_path,symbol)
        exists = os.path.isfile(filepath)
        data = ""

        #if not exist create an empty file
        if exists:
            with open(filepath) as f:
                data = f.read()
        else:
            with open(filepath,'w') as f:
                f.write("")

        #if empty return None
        if data=="":
            return None
        else:
            return json.loads(data)  

    
    def __val_quote(self, quote):
        errors = []

        if quote.asset_type == "":
            errors.append("asset_type is mandatory")

        if quote.symbol == "":
            errors.append("symbol is mandatory")    

        if quote.price_date == "":
            errors.append("price_date is mandatory")

        if quote.open == 0:
            errors.append("open is mandatory")
        
        if quote.high == 0:
            errors.append("high is mandatory")
            
        if quote.low == 0:
            errors.append("low is mandatory")

        if quote.close == 0:
            errors.append("close is mandatory")

        if quote.volume == 0:
            errors.append("volume is mandatory")        

        if quote.last_update == "":
            errors.append("last_update is mandatory")

        if quote.last_price_date == "":
            errors.append("last_price_date is mandatory")

        if quote.prev_close == 0:
            if quote.asset_type != "options":
                errors.append("prev_close is mandatory")
        
        #if quote.prev_price_date == "":
        #    errors.append("prev_price_date is mandatory")

        if len(errors) > 0:
            error = Error()
            error.msg = "Error al guardar las estadisticas para el symbol: {}".format(quote.symbol)
            error.errors = errors
            return error
        else:
            return None