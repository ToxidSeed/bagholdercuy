from cmath import exp
from app import app, db
from model.OptionContract import OptionContract
from datetime import date, datetime
import common.Converter as Converter
from common.Response import Response

class OpcionesContratoManager:
    def __init__(self):
        pass

    def get_options_chain(self, args={}):
        symbol = args["symbol"]
        expiration_date = args["expiration_date"]
        calls = self.get_calls(args=args)
        puts = self.get_puts(args=args)        
                
        data = {
            "calls":Converter.process_list(calls),
            "puts":Converter.process_list(puts),
            "exp_dates":Converter.format(self.get_expiration_dates(args=args)),
            "strikes":Converter.format(self.get_strikes(symbol, expiration_date))
        }
                
        return Response().from_raw_data(data)

    def get_calls(self, args={}):
        contract = args["contract"]

        query = db.session.query(
            OptionContract
        ).filter(
            OptionContract.side == 'call',
        )

        if contract != "":
            contract = "%{}%".format(contract)

            query = query.filter(
                OptionContract.symbol.ilike(contract)
            )       

            return query.all()

        symbol = args["symbol"]
        exp_date = args["expiration_date"]
        strike = args["strike"]

        if symbol != "":
            query = query.filter(
                OptionContract.underlying == symbol    
            )

        if exp_date == "":
            query = query.filter(
                OptionContract.expiration_date >= date.today().isoformat()
            )
        else:
            query = query.filter(
                OptionContract.expiration_date == exp_date
            )

        if strike != "":
            query = query.filter(
                OptionContract.strike == strike
            )

        query = query.order_by(OptionContract.expiration_date, OptionContract.strike)

        return query.all()

    def get_puts(self, args={}):
        contract = args["contract"]

        query = db.session.query(
            OptionContract
        ).filter(
            OptionContract.side == 'put',
        )

        if contract != "":
            contract = "%{}%".format(contract)

            query = query.filter(
                OptionContract.symbol.ilike(contract)
            )       

            return query.all()

        symbol = args["symbol"]
        exp_date = args["expiration_date"]
        strike = args["strike"]

        if symbol != "":
            query = query.filter(
                OptionContract.underlying == symbol    
            )

        if exp_date == "":
            query = query.filter(
                OptionContract.expiration_date >= date.today().isoformat()
            )
        else:
            query = query.filter(
                OptionContract.expiration_date == exp_date
            )

        if strike != "":
            query = query.filter(
                OptionContract.strike == strike
            )

        query = query.order_by(OptionContract.expiration_date, OptionContract.strike)

        return query.all()

    def get_expiration_dates(self, args={}):
        symbol=args["symbol"] #symbol is required
        expiration_date=date.today().isoformat()
        strike=""
        
        query = db.session.query(
            OptionContract.expiration_date
        ).distinct(OptionContract.expiration_date)

        query = query.filter(               
            OptionContract.underlying == symbol
        )
        query = query.filter(OptionContract.expiration_date >= expiration_date)

        results = query.all()

        exp_list = []
        for row in results:
            exp_list.append(row.expiration_date)

        return exp_list

    def get_strikes(self, symbol="", exp_date=""):                
        query = db.session.query(
            OptionContract.strike
        ).distinct(OptionContract.strike)

        query = query.filter(            
            OptionContract.underlying == symbol
        )        

        if exp_date == "":
            query = query.filter(            
                OptionContract.expiration_date  >= date.today().isoformat()
            )   
        else:
            query = query.filter(            
                OptionContract.expiration_date  == exp_date
            )

        query = query.order_by(OptionContract.strike)

        results = query.all()

        strikes = []
        for row in results:
            strikes.append(float(row.strike))
        
        return strikes