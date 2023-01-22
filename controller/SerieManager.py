from controller.base import Base

from common.Response import Response
from common.AppException import AppException
from common.api.Alphavantage import Alphavantage
from common.api.iexcloud import iexcloud

from model.StockData import StockData
from model.CalendarioSemanal import CalendarioSemanalModel
from model.seriesemanal import SerieSemanalModel

from writer.variacionsemanal import VariacionSemanalWriter

from reader.stockdata import StockDataReader

from config.negocio import TIPO_FRECUENCIA_SERIE_DIARIA, SERIES_PROF_CARGA_MESACTUAL, SERIES_PROF_CARGA_MAX, SERIES_PROF_CARGA_YTD, NUM_SEMANAS_REPROCESAR_MES,TIPO_FRECUENCIA_SERIE_SEMANAL,TIPO_FRECUENCIA_SERIE_MENSUAL,SERIES_PROF_CARGA_ULT3MESES,SERIES_PROF_CARGA_ULT6MESES
from config.negocio import SERIES_PROF_CARGA_ULT1ANYO


from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from app import db
from sqlalchemy import func
from sqlalchemy.orm import join
from sqlalchemy import and_


class SerieManagerLoader(Base):    
    def __init__(self,access_token):
        super().__init__(access_token=access_token)
        self.fch_ini_procesar = None


    def procesar(self, args={}):
        try:                        
            anyo = semana = dia = None        

            profundidad = args.get("profundidad")
            symbol = args.get("symbol")

            self.fch_ini_procesar = self.get_fch_ini_reprocesar(profundidad=profundidad)         

            self.load_daily_series(symbol, profundidad)

            #procesamiento de series semanales
            if self.fch_ini_procesar is not None:
                (anyo, semana, dia) = self.fch_ini_procesar.isocalendar()

            SerieSemanalLoader().procesar(symbol, anyo=anyo, semana=semana)
            db.session.flush()
            
            VariacionSemanalWriter().procesar(symbol, anyo=anyo, semana=semana)
            db.session.flush()

            SerieMensualLoader().procesar(symbol, profundidad)            
            db.session.commit()
            return Response(msg="Se ha cargado correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def get_fch_ini_reprocesar(self, profundidad=""):
                
        fecha_actual = date.today()

        fecha = None

        if profundidad == SERIES_PROF_CARGA_MESACTUAL:
            mes = str(fecha_actual.month).zfill(2)
            fecha = date.fromisoformat("{0}-{1}-{2}".format(fch_actual.year,mes,'01'))

        if profundidad == SERIES_PROF_CARGA_YTD:
            fecha = date.fromisoformat("{0}-{1}-{2}".format(fch_actual.year,'01','01')) 

        if profundidad == SERIES_PROF_CARGA_ULT3MESES:
            fecha = fecha_actual + relativedelta(months=-3)

        if profundidad == SERIES_PROF_CARGA_ULT6MESES:
            fecha = fecha_actual + relativedelta(months=-6)

        if profundidad == SERIES_PROF_CARGA_ULT1ANYO:
            fecha = fecha_actual + relativedelta(years=-1)

        return fecha
      

    def get_historial_prices(self, symbol="", profundidad=""):
        args = {
            "symbol":symbol,
            "range":profundidad
        }        
        return iexcloud().get_historical_prices(args)        

    def load_daily_series(self, symbol="", profundidad=""):   
        #obtener la fecha de inicio en base a la profundidad
        fch_ini_reprocesar = self.get_fch_ini_reprocesar(profundidad=profundidad)         
        #eliminar las series diarias desde la fecha de inicio        
        self.remove_daily_series(symbol, fch_ini_reprocesar=fch_ini_reprocesar)
        #obtener los datos desde la api en base a la profundidad
        data = self.get_historial_prices(symbol, profundidad=profundidad)              

        for elem in data:                        
            price_date = date.fromisoformat(elem.get("date"))            

            if fch_ini_reprocesar is None:
                self.insertar_serie_diaria(elem=elem)
                continue        

            if price_date >= fch_ini_reprocesar:
                self.insertar_serie_diaria(elem=elem)
                continue            

    def insertar_serie_diaria(self, elem=None):
        uopen = elem.get("uOpen")
        adj_open = elem.get("open")
        symbol = elem.get("symbol")
        split_factor = round(uopen / adj_open,0)
        price_date = date.fromisoformat(elem.get("date"))
        (year, week, weekday) = price_date.isocalendar()
        fch_registro = date.today()  

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


    def remove_daily_series(self, symbol="", fch_ini_reprocesar=None):        
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

    

    def get_open_data(symbol, open_date):
        result = StockData.query.filter(
            StockData.frequency == "daily",
            StockData.symbol == symbol,
            StockData.price_date == open_date
        ).first()

        return result

    def get_close_data(symbol, close_date):
        result = StockData.query.filter(
            StockData.frequency == "daily",
            StockData.symbol == symbol,
            StockData.price_date == close_date
        ).first() 

        return result


class SerieSemanalLoader():   
    def __init__(self):
        self.symbol = None
        self.anyo = None
        self.semana = None
        self.fch_semana_inicio = None     

    def procesar(self,symbol, anyo = None, semana = None):                
        self.symbol = symbol
        self.anyo = anyo
        self.semana = semana
        
        if anyo is not None and semana is not None:
            self.fch_semana_inicio = date.fromisocalendar(anyo, semana, 1)
        
        self.__eliminar_series_semanales()
        
                #(anyo, semana_ini) = self.eliminar_serie_semanal(symbol=symbol, profundidad=profundidad)
        base = StockDataReader.get_base_semanal(self.symbol, self.fch_semana_inicio)        
                
        fch_registro = date.today()
        for preserie_semana in base:            
            self._procesar_serie(symbol=symbol, preserie_semana=preserie_semana, fch_registro=fch_registro)

    def __eliminar_series_semanales(self):
        
        stmt = (
            db.delete(SerieSemanalModel).
            where(SerieSemanalModel.symbol == self.symbol)
        )

        if self.fch_semana_inicio is not None:
            stmt = stmt.where(
                SerieSemanalModel.fch_semana >= self.fch_semana_inicio        
            )

        db.session.execute(stmt)
    
    def _procesar_serie(self,symbol, preserie_semana, fch_registro):
        serie_apertura = StockDataReader.get_serie(symbol, preserie_semana.open_date)            
        serie_cierre = StockDataReader.get_serie(symbol, preserie_semana.close_date)                        

        nueva_serie_semanal = SerieSemanalModel(
            symbol = preserie_semana.symbol,
            fch_semana = preserie_semana.fch_semana,
            anyo = preserie_semana.anyo,
            semana = preserie_semana.semana,
            imp_apertura = serie_apertura.StockData.open,
            imp_maximo = preserie_semana.high,
            imp_minimo = preserie_semana.low,
            imp_cierre = serie_cierre.StockData.close,
            imp_apertura_ajus = serie_apertura.StockData.adj_open,
            imp_maximo_ajus = preserie_semana.adj_high,
            imp_minimo_ajus = preserie_semana.adj_low,
            imp_cierre_ajus = serie_cierre.StockData.adj_close
        )

        db.session.add(nueva_serie_semanal)


class SerieMensualLoader():    

    def procesar(self, symbol=None, profundidad=None):
        (anyo, mes) = self.eliminar_series_mensual(symbol=symbol, profundidad=profundidad)
        data = self.get_base_mensual(symbol=symbol, anyo=anyo, mes=mes)

        fch_registro = date.today()
        for datosmes in data:
            self.procesar_mes(datosmes, fch_registro)

    def procesar_mes(self, datosmes=None, fch_registro=None):
        symbol = datosmes.symbol
        price_date = datetime(datosmes.anyo,datosmes.mes, 1)
        open_data = SerieManagerLoader.get_open_data(symbol, datosmes.open_date)            
        close_data = SerieManagerLoader.get_close_data(symbol, datosmes.close_date)

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

