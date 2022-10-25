from app import db
from common.AppException import AppException
from common.Formatter import Formatter
from common.Response import Response
from model.StockData import StockData as StockDataModel
from sqlalchemy.sql import extract
from controller.base import Base

class InformeStockController(Base):    

    def get_variacion_mensual(self, args={}):
        formatter = Formatter()

        symbol = args.get("symbol")
        if symbol is None or symbol =="":
            raise AppException(msg="No se ha ingresado el 'symbol'")

        result = db.session.query(
            StockDataModel.price_date.label("fch_mes"),
            extract("year",StockDataModel.price_date).label("anyo"),
            extract("month",StockDataModel.price_date).label("mes"),
            StockDataModel.open,
            StockDataModel.high,
            StockDataModel.low,
            StockDataModel.close
        ).filter(
            StockDataModel.symbol == symbol,
            StockDataModel.frequency=='monthly'
        ).order_by(
            StockDataModel.price_date.desc()
        ).all()

        response = []

        for elem in result:
            pct_high = round(((elem.high - elem.open)/elem.open)*100,2)
            pct_low = round(((elem.low - elem.open)/elem.open)*100,2)
            pct_close = round(((elem.close - elem.open)/elem.open)*100,2)
            var_high = round((elem.high - elem.open),2)
            var_low = round((elem.low - elem.open),2)
            var_close = round((elem.close - elem.open),2)

            elemfmt = formatter.format(elem)
            elemfmt["pct_high"] = float(pct_high)
            elemfmt["pct_low"] = float(pct_low)
            elemfmt["pct_close"] = float(pct_close)
            elemfmt["var_high"] = float(var_high)
            elemfmt["var_low"] = float(var_low)
            elemfmt["var_high_low"] = float(var_high) - float(var_low)
            elemfmt["var_close"] = float(var_close)

            response.append(elemfmt)
        return Response().from_raw_data(response)

    def get_variacion_semanal(self, args={}):
        formatter = Formatter()

        symbol = args.get("symbol")
        if symbol is None or symbol =="":
            raise AppException(msg="No se ha ingresado el 'symbol'")

        result = db.session.query(
            StockDataModel.price_date.label("fch_semana"),
            extract("year",StockDataModel.price_date).label("anyo"),     
            StockDataModel.semana,
            StockDataModel.open,
            StockDataModel.high,
            StockDataModel.low,
            StockDataModel.close
        ).filter(
            StockDataModel.symbol == symbol,
            StockDataModel.frequency=='weekly'
        ).order_by(
            StockDataModel.price_date.desc()
        ).all()

        response = []

        for elem in result:
            pct_high = round(((elem.high - elem.open)/elem.open)*100,2)
            pct_low = round(((elem.low - elem.open)/elem.open)*100,2)
            pct_close = round(((elem.close - elem.open)/elem.open)*100,2)
            var_high = round((elem.high - elem.open),2)
            var_low = round((elem.low - elem.open),2)
            var_close = round((elem.close - elem.open),2)

            elemfmt = formatter.format(elem)
            elemfmt["pct_high"] = float(pct_high)
            elemfmt["pct_low"] = float(pct_low)
            elemfmt["pct_close"] = float(pct_close)
            elemfmt["var_high"] = float(var_high)
            elemfmt["var_low"] = float(var_low)
            elemfmt["var_high_low"] = float(var_high) - float(var_low)
            elemfmt["var_close"] = float(var_close)

            response.append(elemfmt)
        return Response().from_raw_data(response)


        

