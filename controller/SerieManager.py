from controller.base import Base

from common.Response import Response
from common.AppException import AppException
from common.api.Alphavantage import Alphavantage
from common.api.iexcloud import iexcloud

from model.StockData import StockData
from model.CalendarioSemanal import CalendarioSemanalModel
from model.seriesemanal import SerieSemanalModel
from model.seriemensual import SerieMensualModel

from processor.variacionsemanal import VariacionSemanalWriter
from processor.variacionmensual import VariacionMensualWriter
from processor.variaciondiaria import VariacionDiariaLoader

from processor.seriediaria import SerieDiariaWriter
from processor.seriesemanal import SerieSemanalLoader

from reader.stockdata import StockDataReader
from reader.seriemensual import SerieMensualReader
from reader.seriediaria import SerieDiariaReader
from reader.variaciondiaria import VariacionDiariaReader

from parser.serie import SimulacionVariacionParser, SerieManagerLoaderParser

from config.negocio import TIPO_FRECUENCIA_SERIE_DIARIA, SERIES_PROF_CARGA_MESACTUAL, SERIES_PROF_CARGA_MAX, SERIES_PROF_CARGA_YTD, NUM_SEMANAS_REPROCESAR_MES,TIPO_FRECUENCIA_SERIE_SEMANAL,TIPO_FRECUENCIA_SERIE_MENSUAL,SERIES_PROF_CARGA_ULT3MESES,SERIES_PROF_CARGA_ULT6MESES
from config.negocio import SERIES_PROF_CARGA_ULT1ANYO
import common.api.iexcloud as iexcloud

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from app import db
from sqlalchemy import func
from sqlalchemy.orm import join
from sqlalchemy import and_

from sqlalchemy.exc import NoResultFound, MultipleResultsFound

LUNES = 1
VIERNES = 5
SABADO = 6
DOMINGO = 7


class SerieController(Base):
    def get_lista_fechas_maximas_x_symbol(self, args={}):                
        elements = []
        records = SerieDiariaReader().get_lista_fechas_maximas_x_symbol()
        for elem in records:
            hoy = date.today()                        
            ayer = hoy - timedelta(days=1)
            fch_ult_dia_util = None

            anyo, semana, dia = ayer.isocalendar()
            if dia in [SABADO, DOMINGO]:
                fch_ult_dia_util = date.fromisocalendar(anyo, semana, VIERNES)
            else:
                fch_ult_dia_util = ayer

            # si la fecha de la ultima serie es menor a la fecha del ultimo dia util, la carga esta desactualizada
            estado = "Desactualizado" if fch_ult_dia_util > elem.fch_serie else "Actualizado"

            record = {
                "cod_symbol": elem.symbol,
                "fch_serie": elem.fch_serie,
                "num_dias_desde_ultima_serie": (fch_ult_dia_util - elem.fch_serie).days,
                "estado":estado
            }
            elements.append(record)
        
        return Response().from_raw_data(elements)


class SerieManagerLoader(Base):    
    def __init__(self):    
        self.fch_ini_procesar = None
        self.series = []
        self.profundidad = None
        self.symbol = None
        self.anyo = None
        self.semana = None
        self.mes = None
        self.dia = None

    def procesar_desde_ultima_fecha(self, args={}):
        try:
            serie_manager_loader_parser = SerieManagerLoaderParser()
            serie_diaria_reader = SerieDiariaReader()
            args = serie_manager_loader_parser.parse_args_procesar_desde_fecha(args=args)

            cod_symbol = args.get("cod_symbol")
            fch_ultima_serie = serie_diaria_reader.get_fecha_maxima_x_symbol(cod_symbol=cod_symbol)

            rango_helper = iexcloud.RangoHelper()
            rango = rango_helper.get_rango(fch_referencia=fch_ultima_serie)
            if rango is None:
                raise AppException(msg=f"No se ha encontrado un rango en que la fecha {fch_ultima_serie.isoformat()} pueda encajar")

            profundidad, fch_desde, fch_hasta = rango

            iexcloud_api = iexcloud.iexcloud()
            series = iexcloud_api.get_historical_prices({
                "symbol": cod_symbol,
                "profundidad": profundidad
            })

            anyo_semana, num_semana, dia_semana = fch_ultima_serie.isocalendar()

            # cargar las distintas series y variaciones
            SerieDiariaWriter().cargar(cod_symbol, series, fch_ultima_serie)
            VariacionDiariaLoader().procesar(cod_symbol, fch_ultima_serie)
            db.session.flush()

            SerieSemanalLoader().procesar(cod_symbol, anyo=anyo_semana, semana=num_semana)
            db.session.flush()

            VariacionSemanalWriter().procesar(cod_symbol, anyo=anyo_semana, semana=num_semana)
            db.session.flush()

            # procesamiento de las series mensuales
            SerieMensualLoader().procesar(cod_symbol, anyo=fch_ultima_serie.year, mes=fch_ultima_serie.month)
            VariacionMensualWriter().procesar(cod_symbol, anyo=fch_ultima_serie.year, mes=fch_ultima_serie.month)

            db.session.commit()
            return Response(msg="Se ha cargado correctamente")

        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def procesar(self, args={}):
        try:                                    
            self.profundidad = args.get("profundidad")
            self.symbol = args.get("symbol")

            self.series = self.get_historial_prices(self.symbol, profundidad=self.profundidad)
            self.get_fechas_proceso()         

            # cargar las distintas series y variaciones
            SerieDiariaWriter().cargar(self.symbol, self.series, self.fch_ini_procesar)
            VariacionDiariaLoader().procesar(self.symbol, self.fch_ini_procesar)
            db.session.flush()

            SerieSemanalLoader().procesar(self.symbol, anyo=self.anyo, semana=self.semana)
            db.session.flush()
            
            VariacionSemanalWriter().procesar(self.symbol, anyo=self.anyo, semana=self.semana)
            db.session.flush()

            # procesamiento de las series mensuales
            SerieMensualLoader().procesar(self.symbol, anyo=self.anyo, mes=self.mes)
            VariacionMensualWriter().procesar(self.symbol, anyo=self.anyo, mes=self.mes)

            # SerieMensualLoader().procesar(symbol, profundidad)
            db.session.commit()
            return Response(msg="Se ha cargado correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def get_fechas_proceso(self):
        self.fch_ini_procesar = self.get_fecha_inicio_proceso(self.profundidad)
        if self.fch_ini_procesar is not None:
            (self.anyo, self.semana, self.dia) = self.fch_ini_procesar.isocalendar()
            self.mes = self.fch_ini_procesar.month

        return self.fch_ini_procesar

    def get_fecha_inicio_proceso(self, profundidad=""):
                
        fecha_actual = date.today()
        fecha = None

        if profundidad == SERIES_PROF_CARGA_MESACTUAL:
            mes = str(fecha_actual.month).zfill(2)
            fecha = date.fromisoformat("{0}-{1}-{2}".format(fecha_actual.year,mes,'01'))

        if profundidad == SERIES_PROF_CARGA_YTD:
            fecha = date.fromisoformat("{0}-{1}-{2}".format(fecha_actual.year,'01','01')) 

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
        return iexcloud.iexcloud().get_historical_prices(args)

    def load_daily_series(self, symbol="", profundidad=""):   
        # obtener la fecha de inicio en base a la profundidad
        fch_ini_reprocesar = self.get_fechas_proceso(profundidad=profundidad)         
        # eliminar las series diarias desde la fecha de inicio
        self.remove_daily_series(symbol, fch_ini_reprocesar=fch_ini_reprocesar)
        # obtener los datos desde la api en base a la profundidad
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
                StockData.symbol == symbol,
                StockData.frequency == TIPO_FRECUENCIA_SERIE_DIARIA,
            ).delete()
        else:
            StockData.query.filter(
                StockData.symbol == symbol,
                StockData.frequency == TIPO_FRECUENCIA_SERIE_DIARIA,
                StockData.price_date >= fch_ini_reprocesar
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

class SerieMensualLoader():  

    def __init__(self):
        self.symbol = None
        self.anyo = None
        self.mes = None
        self.fch_ini_mes = None 

    def procesar(self, symbol, anyo=None, mes=None):

        self.symbol = symbol
        self.anyo = anyo
        self.mes = mes

        if anyo is not None and mes is not None:
            self.fch_ini_mes = date(anyo, mes, 1)

        self.eliminar_series_mensuales()
        
        #Obtenemos las series mensuales
        pre_series_mensuales = SerieDiariaReader.get_preseries_mensual(self.symbol, self.fch_ini_mes)

        fch_registro = date.today()

        for rownum, preserie in enumerate(pre_series_mensuales, start=1):            
            self.procesar_mes(preserie, fch_registro)    

    def procesar_mes(self, preserie=None, fch_registro=None):
        
        fch_mes = preserie.fch_mes
        anyo = fch_mes.year
        mes = fch_mes.month
        price_date = date(anyo, mes, 1)
    
        serie_apertura = SerieDiariaReader.get_serie(preserie.symbol, preserie.fch_apertura)
        serie_cierre = SerieDiariaReader.get_serie(preserie.symbol, preserie.fch_cierre)

        serie_nueva = SerieMensualModel(
            symbol = preserie.symbol,
            fch_ini_mes = fch_mes,
            anyo = anyo,
            mes = mes,
            imp_apertura = serie_apertura.imp_apertura,
            imp_maximo = preserie.imp_maximo,
            imp_minimo = preserie.imp_minimo,
            imp_cierre = serie_cierre.imp_cierre,
            imp_apertura_ajus = serie_apertura.imp_apertura_ajus,
            imp_maximo_ajus = preserie.imp_maximo_ajus,
            imp_minimo_ajus = preserie.imp_minimo_ajus,
            imp_cierre_ajus = serie_cierre.imp_cierre_ajus,
            fch_registro = fch_registro
        )

        db.session.add(serie_nueva)

    def eliminar_series_mensuales(self):

        stmt = db.delete(SerieMensualModel).where(
            SerieMensualModel.symbol == self.symbol
        )

        if self.fch_ini_mes is not None:
            stmt = stmt.where(
                SerieMensualModel.fch_ini_mes >= self.fch_ini_mes
            )
        
        result = db.session.execute(stmt)
            
class SimulacionVariacionManager(Base):
    def __init__(self):
        self.serie_diaria_reader = SerieDiariaReader()
        self.variacion_diaria_reader = VariacionDiariaReader()

    def simular(self, args={}):
        args = SimulacionVariacionParser().parse_args_simular(args=args)
        cod_symbol = args.get("cod_symbol")
        fch_final = args.get("fch_final")
        fechas_iniciales = args.get("fechas_iniciales")

        serie_final = self.serie_diaria_reader.get_serie(symbol=cod_symbol, fch_serie=fch_final)

        variaciones = []

        for fch_inicial, value in fechas_iniciales.values():            
            
            serie_inicial = self.serie_diaria_reader.get_serie_anterior_a_fecha(cod_symbol=cod_symbol, fch_serie=fch_inicial)
            valores_limites = self.variacion_diaria_reader.get_valores_limites_entre_fechas(cod_symbol=cod_symbol, fch_inicial=fch_inicial, fch_final=fch_final)

            try:

                imp_apertura = serie_inicial.imp_apertura if serie_inicial is not None else 0

                record = {
                    "cod_symbol":cod_symbol,
                    "fch_final":fch_final.isoformat(),
                    "num_dias_profundidad":f"-{value}",
                    "fch_inicial":fch_inicial,
                    "imp_apertura":imp_apertura,
                    "imp_cierre":serie_final.imp_cierre,
                    "imp_maximo":valores_limites.imp_maximo,
                    "imp_minimo":valores_limites.imp_minimo,
                    "imp_var_apertura_cierre": float(serie_final.imp_cierre) - float(serie_inicial.imp_apertura),
                    "imp_var_minimo_maximo": float(valores_limites.imp_maximo) - float(valores_limites.imp_minimo),
                    "imp_var_aper_maximo": float(valores_limites.imp_maximo) - float(serie_inicial.imp_apertura),
                    "imp_var_cierre_maximo": float(valores_limites.imp_maximo) - float(serie_final.imp_cierre) ,
                    "imp_var_aper_minimo": float(valores_limites.imp_minimo) - float(serie_inicial.imp_apertura),
                    "imp_var_cierre_minimo": float(valores_limites.imp_minimo) - float(serie_final.imp_cierre)
                } 

                variaciones.append(record)
            except Exception as e:
                raise AppException(msg=f"Error al procesar la fecha {fch_inicial}, dias: {str(value)}, error={str(e)}")            

        return Response().from_raw_data(variaciones)


