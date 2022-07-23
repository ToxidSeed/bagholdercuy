from common.Response import Response
from model.StockData import StockData
from model.CalendarioSemanal import CalendarioSemanal
from common.api.Alphavantage import Alphavantage
from common.api.iexcloud import iexcloud
from model.StockData import StockData
from datetime import date, datetime
from app import db
from sqlalchemy import func
from sqlalchemy.orm import join
from sqlalchemy import and_


class SerieManager:
    def __init__(self):
        pass

    def load(self, args={}):
        try:            
            symbol = args["symbol"]
            method = args["method"]
            frequency = args["frequency"]

            self.load_daily_series(symbol, method)
            self.load_series_semanales(symbol, method)
            self.load_series_mensuales(symbol)

            db.session.commit()
            return Response(msg="Se ha cargado correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def load_daily_series(self, symbol, method):
        self.remove_series(symbol)
        data = iexcloud().get_historical_prices(symbol)        
        
        for elem in data:
            uopen = elem["uOpen"]
            adj_open = elem["open"]
            split_factor = round(uopen / adj_open,0)
            price_date = date.fromisoformat(elem["date"])
            (year, week, weekday) = price_date.isocalendar()

            new_serie = StockData(
                symbol = symbol,
                price_date = price_date,
                anyo = year,
                mes = price_date.month,
                semana = week,
                frequency = "daily",
                open = uopen,
                high = elem["uHigh"],
                low = elem["uLow"],
                close = elem["uClose"],
                volume = elem["uVolume"],
                adj_open = adj_open,
                adj_high = elem["high"],
                adj_low = elem["low"],
                adj_close = elem["close"],
                adj_volume = elem["volume"],
                split_factor = split_factor
            )
            db.session.add(new_serie)            

    def remove_series(self, symbol=""):
        StockData.query.filter(
            StockData.symbol == symbol
        ).delete()

    def load_series_semanales(self, symbol, method):        
        base = self.get_base_semanal(symbol)        
        
        counter=1
        for semana in base:
            open_data = self.get_open_data(symbol, semana.open_date)            
            close_data = self.get_close_data(symbol, semana.close_date)                        

            new_serie = StockData(
                symbol = symbol,
                price_date = semana.fch_semana,
                anyo = semana.anyo,                
                semana = semana.semana,
                frequency = "weekly",
                open = open_data.open,
                high = semana.high,
                low = semana.low,
                close = close_data.close,                
                adj_open = open_data.adj_open,
                adj_high = semana.adj_high,
                adj_low = semana.adj_low,
                adj_close = close_data.adj_close                
            )
            db.session.add(new_serie)

            counter += 1            
            if counter % 50 == 0:
                print(datetime.today())

    def get_open_data(self, symbol, open_date):
        result = StockData.query.filter(
            StockData.frequency == "daily",
            StockData.symbol == symbol,
            StockData.price_date == open_date
        ).first()

        return result

    def get_close_data(self, symbol, close_date):
        result = StockData.query.filter(
            StockData.frequency == "daily",
            StockData.symbol == symbol,
            StockData.price_date == close_date
        ).first() 

        return result

    def load_series_mensuales(self, symbol):
        baseresult = self.get_base_mensual(symbol)
        for datosmes in baseresult:
            price_date = datetime(datosmes.anyo,datosmes.mes, 1)
            open_data = self.get_open_data(symbol, datosmes.open_date)            
            close_data = self.get_close_data(symbol, datosmes.close_date)

            new_serie = StockData(
                symbol = symbol,
                price_date = price_date,
                anyo = datosmes.anyo,                
                mes = datosmes.mes,
                frequency = "monthly",
                open = open_data.open,
                high = datosmes.high,
                low = datosmes.low,
                close = close_data.close,                
                adj_open = open_data.adj_open,
                adj_high = datosmes.adj_high,
                adj_low = datosmes.adj_low,
                adj_close = close_data.adj_close  
            )
            db.session.add(new_serie)


    def get_base_semanal(self, symbol=""):    
        result = db.session.query(
            CalendarioSemanal.fch_semana,
            CalendarioSemanal.anyo,
            CalendarioSemanal.semana,
            func.min(StockData.price_date).label("open_date"),
            func.max(StockData.price_date).label("close_date"),
            func.min(StockData.low).label("low"),
            func.max(StockData.high).label("high"),
            func.min(StockData.adj_low).label("adj_low"),
            func.min(StockData.adj_high).label("adj_high"),                        
        ).select_from(
            StockData
        ).outerjoin(
            CalendarioSemanal,
            and_(
                StockData.anyo == CalendarioSemanal.anyo,
                StockData.semana == CalendarioSemanal.semana
            )
        ).filter(
            and_(
                StockData.frequency == "daily",
                StockData.symbol == symbol
            )
        ).group_by(
            CalendarioSemanal.fch_semana
        ).order_by(
            CalendarioSemanal.fch_semana.desc()
        ).all()

        return result     

    def get_base_mensual(self, symbol=""):
        result = db.session.query(
            StockData.anyo,
            StockData.mes,
            func.min(StockData.low).label("low"),
            func.max(StockData.high).label("high"),
            func.min(StockData.adj_low).label("adj_low"),
            func.max(StockData.adj_high).label("adj_high"),
            func.min(StockData.price_date).label("open_date"),
            func.max(StockData.price_date).label("close_date")
        ).filter(
            and_(
                StockData.frequency == "daily",
                StockData.symbol == symbol
            )
        ).group_by(
            StockData.anyo,
            StockData.mes
        ).all()

        return result
