from common.Response import Response
from common.AppException import AppException
from model.StockData import StockData
from model.CalendarioSemanal import CalendarioSemanal
from common.api.Alphavantage import Alphavantage
from common.api.iexcloud import iexcloud
from config.negocio import TIPO_FRECUENCIA_SERIE_DIARIA, SERIES_PROF_CARGA_MESACTUAL, SERIES_PROF_CARGA_MAX, SERIES_PROF_CARGA_YTD, NUM_SEMANAS_REPROCESAR_MES,TIPO_FRECUENCIA_SERIE_SEMANAL,TIPO_FRECUENCIA_SERIE_MENSUAL

from model.StockData import StockData
from datetime import date, datetime
from app import db
from sqlalchemy import func
from sqlalchemy.orm import join
from sqlalchemy import and_


class SerieManager:
    def __init__(self):
        pass

    def procesar(self, args={}):
        try:                        
            profundidad = args.get("profundidad")
            symbol = args.get("symbol")

            self.load_daily_series(symbol, profundidad)
            SerieSemanalLoader().procesar(symbol, profundidad)
            SerieMensualLoader().procesar(symbol, profundidad)            
            db.session.commit()
            return Response(msg="Se ha cargado correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def get_fch_ini_reprocesar(self, profundidad=""):
        fecha = None
        fch_actual = date.today()

        if profundidad == SERIES_PROF_CARGA_YTD:
            fecha = "{0}-{1}-{2}".format(fch_actual.year,'01','01')
        if profundidad == SERIES_PROF_CARGA_MESACTUAL:
            mes = str(fch_actual.month).zfill(2)
            fecha = "{0}-{1}-{2}".format(fch_actual.year,mes,'01')

        return fecha

    def get_profundidad_api(self, profundidad=""):
        profundidad_api = profundidad
        if profundidad == SERIES_PROF_CARGA_MESACTUAL:
            profundidad_api = SERIES_PROF_CARGA_YTD
        return profundidad_api        

    def get_historial_prices(self, symbol="", profundidad=""):
        prof_api = self.get_profundidad_api(profundidad)
        args = {
            "symbol":symbol,
            "range":prof_api
        }        
        return iexcloud().get_historical_prices(args)        

    def load_daily_series(self, symbol="", profundidad=""):        
        self.remove_daily_series(symbol, profundidad)
        data = self.get_historial_prices(symbol, profundidad=profundidad)

        fch_registro = date.today()

        for elem in data:
            uopen = elem.get("uOpen")
            adj_open = elem.get("open")
            split_factor = round(uopen / adj_open,0)
            price_date = date.fromisoformat(elem.get("date"))
            (year, week, weekday) = price_date.isocalendar()

            new_serie = StockData(
                symbol = symbol,
                price_date = price_date,
                anyo = year,
                mes = price_date.month,
                semana = week,
                frequency = TIPO_FRECUENCIA_SERIE_DIARIA,
                open = uopen,
                high = elem.get("uHigh"),
                low = elem.get("uLow"),
                close = elem.get("uClose"),
                volume = elem.get("uVolume"),
                adj_open = adj_open,
                adj_high = elem.get("high"),
                adj_low = elem.get("low"),
                adj_close = elem.get("close"),
                adj_volume = elem.get("volume"),
                split_factor = split_factor,
                fch_registro = fch_registro
            )
            db.session.add(new_serie)            

    def remove_daily_series(self, symbol="", profundidad=None):
        fch_ini_reprocesar = self.get_fch_ini_reprocesar(profundidad=profundidad)        
        if fch_ini_reprocesar is None:
            StockData.query.filter(
                StockData.symbol == symbol
            ).delete()
        else:
            StockData.query.filter(
                StockData.symbol == symbol,
                StockData.frequency == TIPO_FRECUENCIA_SERIE_DIARIA,
                StockData.price_date == fch_ini_reprocesar
            ).delete()

    

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


class SerieSemanalLoader(SerieManager):    
    def __init__(self):
        pass    

    def procesar(self,symbol, profundidad):                
        (anyo, semana_ini) = self.eliminar_serie_semanal(symbol=symbol, profundidad=profundidad)
        base = self.get_base_semanal(symbol, anyo, semana_ini)        
                
        fch_registro = date.today()
        for semana in base:            
            self._procesar_serie(symbol=symbol, semana=semana, fch_registro=fch_registro)

    def get_semana_ini_reprocesar(self, symbol="", profundidad=""):
        semana_ini_repro = None
        fch_actual = date.today()
        
        (anyo, semana, diasemana) = fch_actual.isocalendar()

        if profundidad == SERIES_PROF_CARGA_MESACTUAL:
            semana_ini_repro = (semana - NUM_SEMANAS_REPROCESAR_MES)+1
        if profundidad == SERIES_PROF_CARGA_YTD:
            semana_ini_repro = 1

        return (anyo, semana_ini_repro)

    def eliminar_serie_semanal(self, symbol="", profundidad=""):
        (anyo, semana_ini) = self.get_semana_ini_reprocesar(symbol, profundidad=profundidad)

        query = StockData.query.filter(
                    StockData.symbol == symbol,
                    StockData.frequency == TIPO_FRECUENCIA_SERIE_SEMANAL,            
                )
                    
        if semana_ini is not None:
            query.filter(
                StockData.anyo == anyo,
                StockData.semana >= semana_ini    
            )       
        query.delete()     
        return (anyo, semana_ini)
    
    def _procesar_serie(self,symbol="", semana=None, fch_registro=None):
        open_data = self.get_open_data(symbol, semana.open_date)            
        close_data = self.get_close_data(symbol, semana.close_date)                        

        new_serie = StockData(
            symbol = symbol,
            price_date = semana.fch_semana,
            anyo = semana.anyo,                
            semana = semana.semana,
            frequency = TIPO_FRECUENCIA_SERIE_SEMANAL,
            open = open_data.open,
            high = semana.high,
            low = semana.low,
            close = close_data.close,                
            adj_open = open_data.adj_open,
            adj_high = semana.adj_high,
            adj_low = semana.adj_low,
            adj_close = close_data.adj_close,
            fch_registro = fch_registro           
        )
        db.session.add(new_serie)


    def get_base_semanal(self, symbol="", anyo=None,semana_ini_proceso=None):    
        query = db.session.query(
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
        )

        if semana_ini_proceso is not None:
            query.filter(
                StockData.anyo >= anyo,
                StockData.semana >= semana_ini_proceso
            )
        
        return query.all()        
        

class SerieMensualLoader(SerieManager):
    def __init__(self):
        pass

    def procesar(self, symbol=None, profundidad=None):
        (anyo, mes) = self.eliminar_series_mensual(symbol=symbol, profundidad=profundidad)
        data = self.get_base_mensual(symbol=symbol, anyo=anyo, mes=mes)

        fch_registro = date.today()
        for datosmes in data:
            self.procesar_mes(datosmes, fch_registro)

    def procesar_mes(self, datosmes=None, fch_registro=None):
        symbol = datosmes.symbol
        price_date = datetime(datosmes.anyo,datosmes.mes, 1)
        open_data = self.get_open_data(symbol, datosmes.open_date)            
        close_data = self.get_close_data(symbol, datosmes.close_date)

        new_serie = StockData(
            symbol = symbol,
            price_date = price_date,
            anyo = datosmes.anyo,                
            mes = datosmes.mes,
            frequency = TIPO_FRECUENCIA_SERIE_MENSUAL,
            open = open_data.open,
            high = datosmes.high,
            low = datosmes.low,
            close = close_data.close,                
            adj_open = open_data.adj_open,
            adj_high = datosmes.adj_high,
            adj_low = datosmes.adj_low,
            adj_close = close_data.adj_close,
            fch_registro=fch_registro  
        )
        db.session.add(new_serie)

    def eliminar_series_mensual(self, symbol=None, profundidad=None):
        (anyo, mes) = self.get_ini_mes_reprocesar(symbol, profundidad)
        
        query = StockData.query.filter(
            StockData.symbol == symbol,
            StockData.frequency == TIPO_FRECUENCIA_SERIE_MENSUAL
        )
        
        if mes is not None:
            query.filter(
                StockData.anyo == anyo,
                StockData.mes >= mes
            )

        query.delete()
        return (anyo, mes)

    def get_ini_mes_reprocesar(self, symbol=None, profundidad=None):
        fch_actual = date.today()
        anyo = fch_actual.year
        mes = fch_actual.month

        if profundidad == SERIES_PROF_CARGA_MAX:
            mes = None
        if profundidad == SERIES_PROF_CARGA_YTD:
            mes = 1
        
        return (anyo, mes)

    
    def get_base_mensual(self, symbol="", anyo=None, mes=None):
        query = db.session.query(
            StockData.symbol,
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
                StockData.frequency == TIPO_FRECUENCIA_SERIE_DIARIA,
                StockData.symbol == symbol
            )
        ).group_by(
            StockData.symbol,
            StockData.anyo,
            StockData.mes
        )

        if mes is not None:
            query.filter(
                StockData.anyo == anyo,
                StockData.mes >= mes
            )
        
        return query.all()

