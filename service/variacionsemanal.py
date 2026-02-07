from model.variacionsemanal import VariacionSemanalModel
from model.seriesemanal import SerieSemanalModel
from reader.seriesemanal import SerieSemanalReader
from reader.variacionsemanal import VariacionSemanalReader

from domain.semana import CodigoSemana
import logging

logger = logging.getLogger(__name__)
from app import db

class VariacionSemanalService:
    def generar_series(self, cod_symbol, fch_inicio_procesamiento):

        semana_procesamiento = CodigoSemana.from_fecha(fch_inicio_procesamiento)
        fch_semana_procesamiento = semana_procesamiento.to_fecha_inicio_semana()

        max_fch_semana_var = VariacionSemanalReader.get_max_fch_variacion(cod_symbol)

        # eliminar de acuerdo a condiciones
        self.del_variaciones(cod_symbol, max_fch_semana_var, fch_semana_procesamiento)                 

        # Obtener las series para procesar
        series = self.get_series_semanales(cod_symbol, fch_semana_procesamiento)

        # Procesamos las series obtenidas
        self.procesar_series_semanales(cod_symbol, series)

    def del_variaciones(self, cod_symbol, max_fch_semana_var, fch_semana_procesamiento):
        rows_affected = 0
        if not max_fch_semana_var:
            rows_affected = VariacionSemanalModel.eliminar_x_symbol(cod_symbol)

        elif max_fch_semana_var >= fch_semana_procesamiento:
            rows_affected = VariacionSemanalModel.eliminar_desde_fecha(cod_symbol, fch_semana_procesamiento)
        
        else:
            logger.info(f"Nada que eliminar para max_fch_semana_var:{max_fch_semana_var} y fch_semana_procesamiento:{fch_semana_procesamiento}")
        
        return rows_affected

    def get_series_semanales(self, cod_symbol, fch_semana_inicio_procesamiento):
        records = SerieSemanalReader.get_series_desde_fecha(cod_symbol, fch_semana_inicio_procesamiento)
        if len(records) == 0:
            raise Exception(f"No hay series que procesar para cod_symbol: {cod_symbol}, fch_semana_inicio_procesamiento:{fch_semana_inicio_procesamiento.isoformat()}")

        return records

    def get_primera_serie(self, series):
        if series:
            return series[0]

    def get_serie_semanal_anterior(self, cod_symbol, fch_serie):        
        serie_anterior = SerieSemanalReader.get_serie_anterior(cod_symbol, fch_serie)
        return serie_anterior

    def procesar_series_semanales(self, cod_symbol, series):
        primera_serie = self.get_primera_serie(series)
        serie_anterior = self.get_serie_semanal_anterior(cod_symbol, primera_serie.fch_semana)

        for serie in series:
            self.ins_varicion(cod_symbol, serie, serie_anterior)
            serie_anterior = serie

    def ins_varicion(self, cod_symbol, serie_semanal, serie_semanal_anterior):
        imp_cierre_ant = 0
        imp_variacion_cierre = 0
        pct_variacion_cierre = 0
        imp_variacion_maximo = 0
        pct_variacion_maximo = 0
        imp_variacion_minimo = 0
        pct_variacion_minimo = 0

        if serie_semanal_anterior:
            imp_cierre_ant = float(serie_semanal_anterior.imp_cierre)
            imp_variacion_cierre = float(serie_semanal.imp_cierre) - imp_cierre_ant
            pct_variacion_cierre = ((float(serie_semanal.imp_cierre) - imp_cierre_ant)/imp_cierre_ant)*100
            imp_variacion_maximo = float(serie_semanal.imp_maximo) - imp_cierre_ant
            pct_variacion_maximo = ((float(serie_semanal.imp_maximo) - imp_cierre_ant)/imp_cierre_ant)*100
            imp_variacion_minimo = float(serie_semanal.imp_minimo) - imp_cierre_ant
            pct_variacion_minimo = ((float(serie_semanal.imp_minimo) - imp_cierre_ant)/imp_cierre_ant)*100

        new_serie = VariacionSemanalModel(
            symbol=cod_symbol,
            fecha=serie_semanal.fch_semana,
            cod_semana=serie_semanal.cod_semana,
            anyo=serie_semanal.anyo,
            semana=serie_semanal.semana,
            imp_cierre_ant=imp_cierre_ant,
            imp_apertura=serie_semanal.imp_apertura,
            imp_maximo=serie_semanal.imp_maximo,
            imp_minimo=serie_semanal.imp_minimo,
            imp_cierre=serie_semanal.imp_cierre,
            imp_variacion_cierre=imp_variacion_cierre,
            pct_variacion_cierre=pct_variacion_cierre,
            imp_variacion_maximo=imp_variacion_maximo,
            pct_variacion_maximo=pct_variacion_maximo,
            imp_variacion_minimo=imp_variacion_minimo,
            pct_variacion_minimo=imp_variacion_minimo
        )

        db.session.add(new_serie)
        return new_serie

