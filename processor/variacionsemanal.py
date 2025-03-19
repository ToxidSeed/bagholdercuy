from model.variacionsemanal import VariacionSemanalModel
from model.StockData import StockData
from model.seriesemanal import SerieSemanalModel
from reader.calendariosemanal import CalendarioSemanalReader
# from reader.stockdata import StockDataReader
from reader.seriesemanal import SerieSemanalReader
from reader.seriediaria import SerieDiariaReader
from domain.semana import Semana

from sqlalchemy import func, and_
from sqlalchemy.orm import join
from datetime import timedelta, date
from app import db

from common.AppException import AppException


class VariacionSemanalWriter:
    def __init__(self):
        self.symbol = None
        self.anyo = None
        self.semana = None
        self.fch_semana_inicio = None
        self.fch_semana_primera_serie = None

    def procesar(self, symbol, anyo=None, semana=None):
        self.symbol = symbol
        self.anyo = anyo
        self.semana = semana

        if anyo is not None and semana is not None:
            self.fch_semana_inicio = date.fromisocalendar(anyo, semana, 1)

        # obtener la primera serie
        fch_primera_serie = SerieDiariaReader.get_fecha_primera_serie(cod_symbol=symbol)
        self.fch_semana_primera_serie = Semana.from_fecha(fch_primera_serie).fch_semana()

        # eliminar los registros desde la semana que se esta procesando / reprocesando
        self.__eliminar()

        # generamos los registros de variacion
        self.__crear()

    def __eliminar(self):
        if self.fch_semana_inicio is None:
            self.__eliminar_todo()
        else:
            self.__eliminar_desde_fecha()

    def __eliminar_todo(self):

        stmt = db.delete(VariacionSemanalModel).where(
            VariacionSemanalModel.symbol == self.symbol
        )
        db.session.execute(stmt)

    def __eliminar_desde_fecha(self):

        stmt = db.delete(VariacionSemanalModel).where(
            VariacionSemanalModel.symbol == self.symbol,
            VariacionSemanalModel.fecha >= self.fch_semana_inicio
        )
        db.session.execute(stmt)

    def __crear(self):

        series = SerieSemanalReader.get_series_desde_fecha(self.symbol, self.fch_semana_inicio)
        if len(series) == 0:
            raise AppException(msg="No se han encontrado series semanales")

        self.__crear_elementos(series)

    def __crear_elementos(self, series=[]):

        prev_serie_semanal = None
        flg_carga_total = True if self.fch_semana_primera_serie == self.fch_semana_inicio or \
                                  self.fch_semana_inicio is None else False

        # Si la serie esta vacia no hacer nada
        if not series:
            return

        # Obtenemos la primera serie
        primera_serie_semanal = series[0]

        # Si no es una carga total obtenemos la semana previa
        if not flg_carga_total:
            prev_serie_semanal = self.__get_serie_previa(primera_serie_semanal)
            if prev_serie_semanal is None:
                raise AppException(msg="No se ha encontrado una serie previa a la semana ".format(
                    primera_serie_semanal.fch_semana.isoformat()))

        # Procesamos las series
        for rownum, serie_semanal in enumerate(series, start=1):
            self.__crear_nuevo_elemento(serie_semanal, prev_serie_semanal)
            prev_serie_semanal = serie_semanal

    def __get_serie_previa(self, serie_semanal):
        delta = timedelta(weeks=-1)

        fch_semana_anterior = serie_semanal.fch_semana + delta
        (anyo, semana, dia) = fch_semana_anterior.isocalendar()

        fch_serie_previa = date.fromisocalendar(anyo, semana, 1)
        return SerieSemanalReader.get_serie(serie_semanal.symbol, fch_serie_previa)

    def __crear_nuevo_elemento(self, serie_semanal: SerieSemanalModel, prev_serie: SerieSemanalModel = None):

        (anyo, semana, dia) = serie_semanal.fch_semana.isocalendar()
        fch_semana = date.fromisocalendar(anyo, semana, 1)

        if prev_serie is None:
            imp_cierre_ant = 0
            imp_variacion_cierre = float(serie_semanal.imp_cierre)
            pct_variacion_cierre = 100
            imp_variacion_maximo = 0
            pct_variacion_maximo = 0
            imp_variacion_minimo = 0
            pct_variacion_minimo = 0
        else:
            imp_cierre_ant = float(prev_serie.imp_cierre)
            imp_variacion_cierre = float(serie_semanal.imp_cierre) - imp_cierre_ant
            pct_variacion_cierre = float(round(((imp_variacion_cierre) / imp_cierre_ant) * 100, 2))
            imp_variacion_maximo = float(serie_semanal.imp_maximo) - imp_cierre_ant
            pct_variacion_maximo = float(round(imp_variacion_maximo / imp_cierre_ant * 100, 2))
            imp_variacion_minimo = float(serie_semanal.imp_minimo) - imp_cierre_ant
            pct_variacion_minimo = float(round(imp_variacion_minimo / imp_cierre_ant * 100, 2))

        nueva_variacion_semanal = VariacionSemanalModel(
            symbol=serie_semanal.symbol,
            fecha=fch_semana,
            anyo=anyo,
            semana=semana,
            cod_semana=serie_semanal.cod_semana,
            imp_cierre_ant=imp_cierre_ant,
            imp_apertura=serie_semanal.imp_apertura,
            imp_maximo=serie_semanal.imp_maximo,
            imp_minimo=serie_semanal.imp_minimo,
            imp_cierre=serie_semanal.imp_cierre,
            pct_variacion_cierre=pct_variacion_cierre,
            imp_variacion_cierre=imp_variacion_cierre,
            pct_variacion_maximo=pct_variacion_maximo,
            imp_variacion_maximo=imp_variacion_maximo,
            pct_variacion_minimo=pct_variacion_minimo,
            imp_variacion_minimo=imp_variacion_minimo
        )

        db.session.add(nueva_variacion_semanal)
