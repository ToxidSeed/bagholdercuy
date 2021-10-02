from datetime import timedelta
from app import app, db
from model.StockData import StockData
from sqlalchemy import func
from datetime import timedelta, date
from helper.Response import Response

class SimulationManager:
    def __init__(self):
        self.results = []

    def run(self, args={}):
        idx = 1
        for iteration in args["sim_params"]:
            element = self.__sim_iteration(iteration)
            element["idx"] = idx
            self.results.append(element)
            idx+=1

        return Response(input_data=self.results).get()

        

    def __sim_iteration(self, iteration=None):        
        #symbol = iteration["symbol"]
        symbol = "CCL"
        iter_result = {}

        quantity=iteration["quantity"]
        frequency=iteration["frequency"]

        current_date = self.__get_last_date(symbol=symbol)
        max_price = self.__get_high_price(symbol, current_date, iteration)        
        max_price_date = self.__get_max_price_date(symbol,max_price)
        current_price = self.__get_current_price(symbol, current_date)
        pct_change = self.__get_pc_variation(current_price, max_price)
        time_to_recover = self.__get_time_to_recover(current_date,max_price_date)
        growth_potential = self.__get_growth_potential(current_price, max_price)

        pct_change_dec = round(float(pct_change),3)
        growth_potential_dec = round(float(growth_potential),3)

        iter_result={
            "deep_text":"{0} {1}".format(quantity, frequency),
            "max_price":float(max_price),
            "max_price_date":max_price_date.strftime('%Y-%m-%d'),
            "current_price":float(current_price),
            "pct_change":pct_change_dec,
            "pct_change_text":"{}%".format(pct_change_dec),
            "time_to_recover":time_to_recover,
            "time_to_recover_text":"{} days".format(time_to_recover),
            "growth_potential":growth_potential_dec,
            "growth_potential_text":"{}%".format(growth_potential_dec)
        }

        return iter_result

    def __get_last_date(self, symbol=""):
        result = db.session.query(
            func.max(StockData.price_date).label("price_date").label("max_price_date")
        ).filter(
            StockData.symbol==symbol,
            StockData.frequency=="daily"            
        ).one()

        return dict(result)["max_price_date"]    

    def __get_high_price(self,symbol="", last_date=None, iteration={}):
        quantity = iteration["quantity"]

        frequency = iteration["frequency"]
        if frequency != 'all time':
            quantity = int(quantity)

        days = 0
        if frequency=="days":
            days = quantity
        if frequency=="weeks":
            days = quantity*7
        if frequency=="months":
            days = quantity*30
        if frequency=="years":
            days = quantity*365

        if days == 0:
            since_date = date.min
        else:
            since_date = last_date - timedelta(days=days)

        result = db.session.query(
            func.max(StockData.close).label("max_price")
        ).filter(
            StockData.symbol==symbol,
            StockData.frequency=="daily",
            StockData.price_date >= since_date            
        ).one()

        return dict(result)["max_price"]

    def __get_max_price_date(self, symbol="", max_price=None):

        result = None
        if max_price is not None:
            result = db.session.query(
                func.max(StockData.price_date).label("max_price_date")
            ).filter(
                StockData.symbol==symbol,
                StockData.frequency=="daily",
                StockData.close >= float(max_price)
            ).one()

        return dict(result)["max_price_date"]

    def __get_current_price(self, symbol, current_date):        
        result = db.session.query(
                StockData.close.label("current_price")
        ).filter(
            StockData.symbol==symbol,
            StockData.frequency=="daily",
            StockData.price_date == current_date
        ).one()

        return dict(result)["current_price"]

    def __get_pc_variation(self, current_price, reference_price):
        pct_variation = ((current_price - reference_price)/reference_price)*100
        return pct_variation

    def __get_time_to_recover(self, current_price_date, ref_price_date):
        date_diff_days = abs((current_price_date - ref_price_date).days)
        return date_diff_days

    def __get_date_to_recover(self, current_date, date_diff_days):
        target_date = current_date + timedelta(days=date_diff_days)
        return target_date

    def __get_growth_potential(self,current_price, reference_price ):
        growth_potential = ((reference_price - current_price)/current_price)*100
        return growth_potential
