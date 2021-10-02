class Quote:   
    def __init__(self, asset_type="", symbol="", price_date="", open=0,high=0,low=0,close=0,volume=0,last_update="",last_price_date="", prev_close=0):        
        self.asset_type = asset_type
        self.symbol = symbol
        self.price_date = price_date        
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume        
        self.last_update = last_update
        self.last_price_date = last_price_date
        self.prev_close = prev_close
        self.prev_price_date = ""

    def from_stats(self, stats={}):
        for key, value in stats.items():
            setattr(self, key, value)                
        return self

    def from_sd(self, sd=None):
        if sd is not None:
            self.symbol = sd.symbol
            self.open = sd.open
            self.high = sd.high
            self.low = sd.low
            self.close = sd.close
            self.price_date = sd.price_date
        
        return self