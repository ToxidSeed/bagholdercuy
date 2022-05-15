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
        symbol=args["symbol"] #symbol is required
        expiration_date=""
        strike=""
        if "expiration_date" in args:
            expiration_date = args["expiration_date"]
        if "strike" in args:
            strike = args["strike"]
        #strike = args["strike"]

        calls_query = db.session.query(
            OptionContract
        ).filter(
            OptionContract.side == 'call',
            OptionContract.expiration_date >= date.today().isoformat(),
            OptionContract.underlying == symbol
        ).order_by(OptionContract.expiration_date, OptionContract.strike)

        if expiration_date != "":
            calls_query = calls_query.filter(OptionContract.expiration_date == expiration_date)
        if strike != "":
            calls_query = calls_query.filter(OptionContract.strike == strike)

        calls = calls_query.all()

        puts_query = db.session.query(
            OptionContract
        ).filter(
            OptionContract.side == 'put',
            OptionContract.expiration_date >= date.today().isoformat(),
            OptionContract.underlying == symbol
        ).order_by(OptionContract.expiration_date, OptionContract.strike)
        
        if expiration_date != "":
            puts_query = puts_query.filter(OptionContract.expiration_date == expiration_date)
        if strike != "":
            puts_query = puts_query.filter(OptionContract.strike == strike)

        puts = puts_query.all()
                
        data = {
            "calls":Converter.process_list(calls),
            "puts":Converter.process_list(puts),
            "exp_dates":Converter.format(self.get_expiration_dates(args=args)),
            "strikes":self.get_strikes(symbol, exp_date=expiration_date,strike=strike)
        }
                
        return Response().from_raw_data(data)

    def get_expiration_dates(self, args={}):
        symbol=args["symbol"] #symbol is required
        expiration_date=date.today().isoformat()
        strike=""
        if "expiration_date" in args:
            expiration_date = args["expiration_date"]
        if "strike" in args:
            strike = args["strike"]

        query = db.session.query(
            OptionContract.expiration_date
        ).distinct(OptionContract.expiration_date)

        query.filter(
            OptionContract.expiration_date >= expiration_date,
            OptionContract.underlying == symbol
        )

        if strike != "":
            query.filter(
                OptionContract.strike == strike
            )

        results = query.all()

        exp_list = []
        for row in results:
            exp_list.append(row.expiration_date)

        return exp_list

    def get_strikes(self, symbol="", exp_date=date.today().isoformat(),strike=""):
        query = db.session.query(
            OptionContract.strike
        ).distinct(OptionContract.strike)

        query.filter(
            OptionContract.expiration_date >= exp_date,
            OptionContract.underlying == symbol
        )

        if strike != "":
            query.filter(
                OptionContract.strike == strike
            )

        results = query.all()

        strikes = []
        for row in results:
            strikes.append(row.strike)
        
        return strikes