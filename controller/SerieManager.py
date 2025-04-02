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
from service.seriesemanal import SerieSemanalService
# from service.variacionsemanal import ReprocesadorVariacionSemanalService
from service.variacionsemanal import VariacionSemanalService
from service.seriemensual import SerieMensualService
from service.variacionmensual import VariacionMensualService
from service.resumenserie import ResumenSerieService

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
        fch_inicio_insercion = serie_diaria_service.insertar_multiples_series(cod_symbol, series, flg_importes_ajustados, mode)
        db.session.flush()
        return fch_inicio_insercion

    def generar_variaciones_diarias(self, cod_symbol, fch_inicio_procesamiento):
        variacion_diaria_service = VariacionDiariaService()
        variacion_diaria_service.generar_variaciones(cod_symbol, fch_inicio_procesamiento)
        db.session.flush()

    def generar_series_semanales(self, cod_symbol, fch_inicio_procesamiento):
        serie_semanal_service = SerieSemanalService()
        serie_semanal_service.generar_series(cod_symbol, fch_inicio_procesamiento)
        db.session.flush()
        
    def generar_variaciones_semanales(self, cod_symbol, fch_inicio_procesamiento):
        variacion_semanal_service = VariacionSemanalService()
        variacion_semanal_service.generar_series(cod_symbol, fch_inicio_procesamiento)
        db.session.flush()        

    def generar_series_mensuales(self, cod_symbol, fch_inicio_procesamiento):
        serie_mensual_service = SerieMensualService()
        serie_mensual_service.generar_series(cod_symbol, fch_inicio_procesamiento)
        db.session.flush()

    def generar_variaciones_mensuales(self, cod_symbol, fch_inicio_procesamiento):
        var_mensual_service = VariacionMensualService()
        var_mensual_service.generar_series(cod_symbol, fch_inicio_procesamiento)

    def guardar_resumen_series(self, cod_symbol):
        rss = ResumenSerieService()
        rss.guardar(cod_symbol)
    

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
        fch_inicio_procesamiento = self.generar_series_diarias(cod_symbol, series=series, flg_importes_ajustados=True, mode=modo_carga)        

        # generar las variaciones
        self.generar_variaciones_diarias(cod_symbol, fch_inicio_procesamiento)        
        self.generar_series_semanales(cod_symbol, fch_inicio_procesamiento)        
        self.generar_variaciones_semanales(cod_symbol, fch_inicio_procesamiento)
        self.generar_series_mensuales(cod_symbol, fch_inicio_procesamiento)
        self.generar_variaciones_mensuales(cod_symbol, fch_inicio_procesamiento)
        self.guardar_resumen_series(cod_symbol)
        

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
                imp_cierre = float(row[col_cierre].replace("$",""))
                imp_apertura = float(row[col_apertura].replace("$",""))
                imp_maximo = float(row[col_maximo].replace("$",""))
                imp_minimo = float(row[col_minimo].replace("$",""))
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

