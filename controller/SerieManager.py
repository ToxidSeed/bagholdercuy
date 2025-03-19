import os
import uuid
import csv
from datetime import date, timedelta, datetime
import logging
from dateutil.relativedelta import relativedelta


from app import db, app
from common.AppException import AppException
from common.Response import Response
from common.Formatter import Formatter
from common.api.iexcloud import iexcloud, RangoHelper
from config.app_constants import SERIES_PROF_CARGA_ULT1ANYO
from config.app_constants import TIPO_FRECUENCIA_SERIE_DIARIA, SERIES_PROF_CARGA_MESACTUAL, SERIES_PROF_CARGA_YTD, \
    SERIES_PROF_CARGA_ULT3MESES, SERIES_PROF_CARGA_ULT6MESES
from controller.base import Base
from model.StockData import StockData
from model.seriediaria import SerieDiariaModel
from model.seriemensual import SerieMensualModel
from parser.serie import SimulacionVariacionParser, SerieManagerLoaderParser, SerieControllerParser, ReparadorSeriesParser
from processor.seriediaria import SerieDiariaWriter
from processor.seriesemanal import SerieSemanalLoader
from processor.variaciondiaria import VariacionDiariaLoader
from processor.variacionmensual import VariacionMensualWriter
from processor.variacionsemanal import VariacionSemanalWriter
from reader.seriediaria import SerieDiariaReader
from reader.variaciondiaria import VariacionDiariaReader
from reader.seriesemanal import SerieSemanalReader
from reader.seriemensual import SerieMensualReader
from reader.variacionmensual import VariacionMensualReader
from reader.variacionsemanal import VariacionSemanalReader
from manager.seriediaria import SimpleSerieDiariaManager
from manager.variaciaciondiaria import VariacionDiariaManager
from manager.serieintegridad import *
from service.seriediaria import SerieDiariaService
from service.variaciondiaria import VariacionDiariaService
# from service.variaciondiaria import VariacionDiariaProcesador
# from service.seriesemanal import SerieSemanalReprocesador
from service.variacionsemanal import ReprocesadorVariacionSemanalService
from service.seriemensual import SerieMensualProcesador
from service.variacionmensual import VariacionMensualProcesador
import structure.inputfiles as inputfiles

from domain.semana import CodigoSemana, Semana
from domain.mes import Mes

from dataclasses import dataclass
from rich.pretty import pprint

LUNES = 1
VIERNES = 5
SABADO = 6
DOMINGO = 7

logger = logging.getLogger(__name__)

WRITE_MODE_AGREGAR = app.config["WRITE_MODE_AGREGAR"]
WRITE_MODE_REEMPLAZAR = app.config["WRITE_MODE_REEMPLAZAR"]

class NASDAQSerieDiariaCsvHelper:
    def get_data(self, cod_symbol, file_storage, sort="asc"):
        ruta_fichero = self.guardar_fichero_temporal(file_storage=file_storage, cod_symbol=cod_symbol)
        records = self.leer_csv(ruta_fichero=ruta_fichero)
        return records

    def leer_csv(self, ruta_fichero):
        contenido = []
        with open(ruta_fichero, "r") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            col_fch_serie = 0
            col_cierre = 1
            col_volumen = 2
            col_apertura = 3
            col_maximo = 4
            col_minimo = 5

            #quitando la primera linea por que son las cabeceras
            next(csvreader)
            for row in csvreader:
                fch_serie = datetime.strptime(row[col_fch_serie], "%m/%d/%Y").date()
                imp_cierre = float(row[col_cierre][1:])
                imp_apertura = float(row[col_apertura][1:])
                imp_maximo = float(row[col_maximo][1:])
                imp_minimo = float(row[col_minimo][1:])
                quote = (fch_serie, imp_cierre , int(row[col_volumen]), imp_apertura, imp_maximo, imp_minimo)
                contenido.append(quote)

        contenido = sorted(contenido)
        return contenido


    def guardar_fichero_temporal(self, file_storage, cod_symbol):
        tmp_dir = app.config.get("RUTA_TMP")
        fch_actual_iso = date.today().isoformat()
        fichero_nombre = f"nasdaq_{cod_symbol}_{str(uuid.uuid1())}.csv"
        fichero_ruta = os.path.join(tmp_dir, fichero_nombre)
        file_storage.save(fichero_ruta)
        return fichero_ruta



class SerieController(Base):

    def _crear_elemento_stats(self, key, label, objeto=None):
        base_dict = {
            "key": key,
            "label": label
        }

        if objeto is None:
            base_dict["min"] = ""
            base_dict["max"] = ""
            base_dict["cantidad"] = 0
        else:
            base_dict["min"] = objeto.min
            base_dict["max"] = objeto.max
            base_dict["cantidad"] = objeto.cantidad

        return base_dict

    def get_lista_fechas_maximas_x_symbol(self, args={}):                
        elements = []
        vr = VariacionDiariaReader()
        records = SerieDiariaReader().get_lista_fechas_maximas_x_symbol()
        for elem in records:


            fch_ultimo_dia_util = self._get_ultimo_dia_util()
            record = {
                "cod_symbol": elem.cod_symbol,
                "min_fch_serie": elem.min_fch_serie,
                "max_fch_serie": elem.max_fch_serie,
                "num_series": elem.num_series,
                "num_dias_desde_ultima_serie": (fch_ultimo_dia_util - elem.max_fch_serie).days,                
                "serie_diaria_integridad":{
                    "dsc_estado":"Correcto",
                    "dsc_estado_split":"ok",
                    "dsc_est_num_dias_separacion":"ok"
                },                                
                "est_var_diaria": "Correcto",
                "est_serie_semanal": "Correcto",
                "est_var_semanal": "Correcto",
                "est_serie_mensual": "Correcto",
                "est_var_mensual": "Correcto"
            }

            estados = [record.get(key) for key in ['est_serie_diaria','est_var_diaria','est_serie_semanal','est_var_semanal','est_serie_mensual','est_var_mensual']]
            record["estado"] = self._determinar_estado(estados=estados, fch_ult_dia_util=fch_ultimo_dia_util, fch_ult_serie=elem.max_fch_serie)

            elements.append(record)
        
        return Response().from_raw_data(elements)

    def _get_ultimo_dia_util(self):
        hoy = date.today()
        ayer = hoy - timedelta(days=1)
        anyo, semana, dia = ayer.isocalendar()
        if dia in [SABADO, DOMINGO]:
            fch_ult_dia_util = date.fromisocalendar(anyo, semana, VIERNES)
        else:
            fch_ult_dia_util = ayer
        return fch_ult_dia_util

    def get_serie_diaria_integridad(self, cod_symbol):
        serie_integridad_manager = SerieDiariaIntegridad()
        info = serie_integridad_manager.evaluar(cod_symbol)

        integridad = info.__dict__
        integridad["dsc_estado"] = "Correcto" if info.correcto is True else "Defectuoso"
        integridad["dsc_estado_split"] = "ok" if info.split_correcto is True else "Error"
        # integridad["dsc_est_num_dias_separacion"] = "ok" if info.num_dias_separacion_correcto is True else "Error"        
        integridad["dsc_est_num_dias_separacion"] = "ok"
        return integridad


    def _determinar_estado_var_diaria(self, reader:VariacionDiariaReader, cod_symbol, num_series_diarias):
        stats = reader.get_estadisticas(cod_symbol=cod_symbol)
        if stats.cantidad == num_series_diarias:
            return "Correcto"
        else:
            return "Defectuoso"

    def _determinar_estado_serie_semanal(self, cod_symbol, min_fch_serie, max_fch_serie):
        stats = SerieSemanalReader.get_estadisticas(cod_symbol=cod_symbol)
        min_cod_semana = stats.min_cod_semana
        min_semana_serie = Semana.from_fecha(fecha=min_fch_serie).codigo()

        max_cod_semana = stats.max_cod_semana
        max_semana_serie = Semana.from_fecha(fecha=max_fch_serie).codigo()

        if min_cod_semana == min_semana_serie and max_cod_semana == max_semana_serie:
            return "Correcto"
        else:
            return "Defectuoso"

    def _determinar_estado_variacion_semanal(self, cod_symbol, min_fch_serie, max_fch_serie):
        stats = VariacionSemanalReader.get_estadisticas(cod_symbol=cod_symbol)
        min_cod_semana = stats.min_cod_semana
        min_semana_serie = Semana.from_fecha(fecha=min_fch_serie).codigo()

        max_cod_semana = stats.max_cod_semana
        max_semana_serie = Semana.from_fecha(fecha=max_fch_serie).codigo()

        if min_cod_semana == min_semana_serie and max_cod_semana == max_semana_serie:
            return "Correcto"
        else:
            return "Defectuoso"

    def _determinar_estado_series_mensuales(self, cod_symbol,  min_fch_serie, max_fch_serie):
        stats = SerieMensualReader.get_estadisticas(cod_symbol=cod_symbol)
        if stats.min_fch_mes is None or stats.max_fch_mes is None:
            return "Defectuoso"

        min_cod_mes = Mes.from_fecha(stats.min_fch_mes).codigo()
        min_mes_serie = Mes.from_fecha(fecha=min_fch_serie).codigo()

        max_cod_mes = Mes.from_fecha(stats.max_fch_mes).codigo()
        max_mes_serie = Mes.from_fecha(fecha=max_fch_serie).codigo()

        if min_cod_mes == min_mes_serie and max_cod_mes == max_mes_serie:
            return "Correcto"
        else:
            return "Defectuoso"

    def _determinar_estado_variaciones_mensuales(self, cod_symbol,  min_fch_serie, max_fch_serie):
        stats = VariacionMensualReader.get_estadisticas(cod_symbol=cod_symbol)
        if stats.min_fch_mes is None or stats.max_fch_mes is None:
            return "Defectuoso"

        min_cod_mes = Mes.from_fecha(stats.min_fch_mes).codigo()
        min_mes_serie = Mes.from_fecha(fecha=min_fch_serie).codigo()

        max_cod_mes = Mes.from_fecha(stats.max_fch_mes).codigo()
        max_mes_serie = Mes.from_fecha(fecha=max_fch_serie).codigo()

        if min_cod_mes == min_mes_serie and max_cod_mes == max_mes_serie:
            return "Correcto"
        else:
            return "Defectuoso"


    def _determinar_estado(self, estados,  fch_ult_dia_util:date, fch_ult_serie:date):
        if "Defectuoso" in estados:
            return "Defectuoso"

        estado = "Desactualizado" if fch_ult_dia_util > fch_ult_serie else "Actualizado"
        return estado

    def get_series_diarias(self, args={}):
        try:
            parser = SerieControllerParser()
            params = parser.parse_args_get_series_diarias(args=args)
            records = SerieDiariaReader.get_series_entre_fechas(symbol=params.get("cod_symbol"),
                                                                fch_inicio=params.get("fch_desde"),
                                                                fch_fin=params.get("fch_hasta")
                                                      )
            return Response().from_raw_data(records)
        except Exception as e:
            return Response().from_exception(e)


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



    def actualizar_serie(self, args={}):
        try:
            serie_manager_loader_parser = SerieManagerLoaderParser()
            serie_diaria_reader = SerieDiariaReader()
            args = serie_manager_loader_parser.parse_args_actualizar_serie(args=args)

            #
            cod_symbol = args.get("cod_symbol")

            # obtener la fecha de la serie mas reciente por symbol
            result = serie_diaria_reader.get_fecha_maxima_x_symbol(cod_symbol=cod_symbol)
            fch_ultima_serie = result.max_fch_serie

            # obtener el rango y fechas de la ultima fecha de la serie
            profundidad, fch_desde, fch_hasta = self._get_rango(fch_referencia=fch_ultima_serie)

            # obtener las series
            series = self.get_historial_prices(symbol=cod_symbol, profundidad=profundidad)

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

    def _get_rango(self, fch_referencia):
        rango_helper = RangoHelper()
        rango = rango_helper.get_rango(fch_referencia=fch_referencia)
        if rango is None:
            raise AppException(
                msg=f"No se ha encontrado un rango en que la fecha {fch_referencia.isoformat()} pueda encajar")

        return rango

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
        return iexcloud().get_historical_prices(args)

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

class ReprocesoSerieController(Base):
    def __init__(self):
        self.cod_symbol = None
    
    def reprocesar(self, args=None):
        try:

            file_storage = args.get("files").get("fichero")
            form = args.get("form")
            cod_symbol = form.get("cod_symbol")

            # Obtener los datos del fichero
            records = NASDAQSerieDiariaCsvHelper().get_data(cod_symbol, file_storage)

            # iniciamos el reproceso
            self.iniciar_reproceso(cod_symbol, series=records)   

            db.session.commit()
            return Response(msg=f"Se han reprocesado correctamente los datos para {cod_symbol}")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def iniciar_reproceso(self, cod_symbol, series:list):
        self.__reprocesar_series_diarias(cod_symbol=cod_symbol, series=series)
        self.__reprocesar_variaciones_diarias(cod_symbol)        
        #self.__reparar_series_semanales(serie_semanal_integridad)
        #self.__reparar_variaciones_semanales(var_semanal_integridad)
        #self.__reparar_series_mensuales(serie_mensual_integridad)
        #self.__reparar_variaciones_mensuales(var_mensual_integridad)

    def __reprocesar_series_diarias(self, cod_symbol, series):            
        pass
        #ReprocesoSeriesAjustadasService().reprocesar(cod_symbol=cod_symbol, series=series)
                

    
    def __reprocesar_variaciones_diarias(self, cod_symbol):
        """
        ReprocesadorVariacionSemanalService(
            cod_symbol=cod_symbol,
            flg_reprocesar_todo=True
        ).reprocesar()
        """

    def __reprocesar_series_semanales(self, serie_semanal_integridad: SerieSemanalIntegridad):
        if serie_semanal_integridad.correcto:
            logger.info("Series semanales integridad: No necesario")
            return        

        SerieSemanalReprocesador(
            cod_symbol=self.cod_symbol,
            flg_reprocesar=True,
            flg_reprocesar_todo=True
        ).procesar()

    def __reparar_variaciones_semanales(self, var_semanal_integridad: VariacionSemanalIntegridad):
        if var_semanal_integridad.correcto:
            logger.info("Variacion semanal integridad: No necesario")
            return

        VariacionSemanalReprocesador(
            cod_symbol=self.cod_symbol,
            flg_reprocesar_todo=True
        ).reprocesar()

    def __reparar_series_mensuales(self, serie_mensual_integridad, SerieMensualIntegridad):
        if serie_mensual_integridad.correcto:
            logger.info("Serie Mensual Integridad: No necesario")
            return

        smp = SerieMensualProcesador(
            cod_symbol=self.cod_symbol,
            flg_reprocesar=True,
            flg_reprocesar_todo=True
        )
        smp.procesar()

    def __reparar_variaciones_mensuales(self, var_mensual_integridad, VariacionMensualIntegridad):
        if var_mensual_integridad.correcto:
            logger.info("Variacion Mensual Integridad: No necesario")
            return

        vmp = VariacionMensualProcesador(
            cod_symbol=self.cod_symbol,
            flg_reprocesar=True,
            flg_reprocesar_todo=True
        )
        vmp.procesar()
    

class NasdaqCsvLoader(Base):
    def __init__(self):
        self.fichero_ruta = None

    def load(self, args=None):
        try:
            tmp_fichero = args.get("files").get("fichero")
            form = args.get("form")
            cod_symbol = form.get("cod_symbol")
            modo_carga = form.get("modo_carga")
            self.__guardar_fichero_temporal(tmp_fichero, cod_symbol)
            contenido = self.parse_contenido_fichero()
            self.__crear_series(series=contenido, cod_symbol=cod_symbol, modo_carga=modo_carga)
            db.session.commit()
            return Response(msg="Se ha procesado correctamente el fichero con los codigos de opcion")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def generar_series_diarias(self, cod_symbol, series, flg_importes_ajustados, mode):
        serie_diaria_service = SerieDiariaService()
        serie_diaria_service.insertar_multiples_series(cod_symbol, series, flg_importes_ajustados, mode)

    def generar_variaciones_diarias(self):
        pass

    def generar_series_semanales(self):
        pass

    def generar_variaciones_semanales(self):
        pass

    def generar_series_mensuales(self):
        pass

    def generar_variaciones_mensuales(self):
        pass

    

    def __crear_series(self, series, cod_symbol, modo_carga):   
        if not series:
            raise AppException("No hay series válidas")            

        if modo_carga == "Agregar":
            modo_carga = WRITE_MODE_AGREGAR
        elif modo_carga == "Reemplazar":
            modo_carga = WRITE_MODE_REEMPLAZAR
        else:
            raise AppException("{modo_carga} no es un modo válido")

        # generando los distintos tipos de series
        self.generar_series_diarias(cod_symbol, series=series, flg_importes_ajustados=True, mode=modo_carga)
        self.generar_variaciones_diarias()
        self.generar_series_semanales()
        self.generar_variaciones_semanales()
        self.generar_series_mensuales()
        self.generar_variaciones_mensuales()    

    def get_datos_primera_serie(self, primera_serie):
        fch_serie, *otros = primera_serie
        semana = CodigoSemana(fch_serie)
        mes = Mes.from_fecha(fch_serie)
        return semana, mes

    def __guardar_fichero_temporal(self, tmp_fichero, cod_symbol):
        tmp_dir = app.config.get("RUTA_TMP")
        fch_actual_iso = date.today().isoformat()
        fichero_nombre = f"nasdaq_{cod_symbol}_{str(uuid.uuid1())}.csv"
        self.fichero_ruta = os.path.join(tmp_dir, fichero_nombre)
        tmp_fichero.save(self.fichero_ruta)

    def parse_contenido_fichero(self):
        contenido = []
        with open(self.fichero_ruta, "r") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            col_fch_serie = 0
            col_cierre = 1
            col_volumen = 2
            col_apertura = 3
            col_maximo = 4
            col_minimo = 5

            #quitando la primera linea por que son las cabeceras
            next(csvreader)
            for row in csvreader:
                fch_serie = datetime.strptime(row[col_fch_serie], "%m/%d/%Y").date()
                imp_cierre = float(row[col_cierre])
                imp_apertura = float(row[col_apertura])
                imp_maximo = float(row[col_maximo])
                imp_minimo = float(row[col_minimo])
                volumen = int(row[col_volumen])
                serie = inputfiles.CsvNasdaq(
                    fch_serie,
                    imp_apertura,
                    imp_maximo,
                    imp_minimo,
                    imp_cierre, 
                    volumen
                )                
                contenido.append(serie)

        contenido = sorted(contenido)
        return contenido

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
                    "fch_final":fch_final.date().isoformat(),
                    "num_dias_profundidad":f"-{value}",
                    "fch_inicial":fch_inicial.date().isoformat(),
                    "imp_apertura":imp_apertura,
                    "imp_cierre":serie_final.imp_cierre,
                    "imp_maximo":valores_limites.imp_maximo,
                    "imp_minimo":valores_limites.imp_minimo,
                    "imp_var_apertura_cierre": float(serie_final.imp_cierre) - float(serie_inicial.imp_apertura),
                    "imp_var_minimo_maximo": float(valores_limites.imp_maximo) - float(valores_limites.imp_minimo),
                    "imp_var_aper_maximo": float(valores_limites.imp_maximo) - float(serie_inicial.imp_apertura),
                    "imp_var_cierre_maximo": float(serie_final.imp_cierre) - float(valores_limites.imp_maximo),
                    "imp_var_aper_minimo": float(valores_limites.imp_minimo) - float(serie_inicial.imp_apertura),
                    "imp_var_cierre_minimo": float(serie_final.imp_cierre) - float(valores_limites.imp_minimo)
                } 

                variaciones.append(record)
            except Exception as e:
                raise AppException(msg=f"Error al procesar la fecha {fch_inicial}, dias: {str(value)}, error={str(e)}")            

        return Response().from_raw_data(variaciones)


class SerieMensualLoader:

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

        # Obtenemos las series mensuales
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
            symbol=preserie.symbol,
            fch_ini_mes=fch_mes,
            anyo=anyo,
            mes=mes,
            imp_apertura=serie_apertura.imp_apertura,
            imp_maximo=preserie.imp_maximo,
            imp_minimo=preserie.imp_minimo,
            imp_cierre=serie_cierre.imp_cierre,
            imp_apertura_ajus=serie_apertura.imp_apertura_ajus,
            imp_maximo_ajus=preserie.imp_maximo_ajus,
            imp_minimo_ajus=preserie.imp_minimo_ajus,
            imp_cierre_ajus=serie_cierre.imp_cierre_ajus,
            fch_registro=fch_registro
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