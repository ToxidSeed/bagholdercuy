from info.serie import SerieSemanalIntegridadInfo
from reader.seriediaria import SerieDiariaReader
from reader.seriesemanal import SerieSemanalReader
from model.seriesemanal import SerieSemanalModel
from datetime import date
from domain.semana import CodigoSemana
import logging

logger = logging.getLogger(__name__)
from config.extensions import db

class SerieSemanalService:
    def generar_series(self, cod_symbol, fch_inicio_procesamiento):
        #logger.info(f"cod_symbol: {cod_symbol}")

        semana_procesamiento = CodigoSemana.from_fecha(fch_inicio_procesamiento)
        fch_semana_procesamiento = semana_procesamiento.to_fecha_inicio_semana()
        #logger.info(f"semana procesamiento: {str(semana_procesamiento)}")

        max_fch_semana = SerieSemanalReader.get_max_fch_semana(cod_symbol)
        #logger.info(f"Max fch semana: {str(max_fch_semana)}")

        # Si hay datos luego de la fecha de semana inicio procesamiento
        if max_fch_semana is not None and max_fch_semana >= fch_semana_procesamiento:
            SerieSemanalModel.eliminar_por_symbol_desde_fecha(cod_symbol, fch_semana=fch_semana_procesamiento)

        # obtenemos las pre series
        pre_series = SerieDiariaReader.get_preseries_semanal(cod_symbol, fch_semana_procesamiento)

        # procesar las pre series
        self.procesar_pre_series(cod_symbol, pre_series)

    def procesar_pre_series(self, cod_symbol, pre_series):
        for pre_serie in pre_series:            
            self.insertar_serie(cod_symbol, pre_serie)

    def insertar_serie(self, cod_symbol, pre_serie):
        serie_apertura = SerieDiariaReader.get_serie(cod_symbol, pre_serie.open_date)   
        serie_cierre = SerieDiariaReader.get_serie(cod_symbol, pre_serie.close_date)

        nu_serie = SerieSemanalModel(
            symbol = cod_symbol,
            fch_semana = pre_serie.fch_semana,
            anyo = pre_serie.anyo,
            semana = pre_serie.semana,
            cod_semana = CodigoSemana(pre_serie.anyo, pre_serie.semana).value,
            imp_apertura = serie_apertura.imp_apertura,
            imp_maximo = pre_serie.imp_maximo,
            imp_minimo = pre_serie.imp_minimo,
            imp_cierre = serie_cierre.imp_cierre,
            fch_registro = date.today()
        )

        db.session.add(nu_serie)
        return nu_serie
        


class ReprocesadorSerieSemanalService:
    def __init__(self, cod_symbol, flg_reprocesar=False, flg_reprocesar_todo=False):
        self.cod_symbol = cod_symbol
        self.flg_reprocesar = flg_reprocesar
        self.flg_reprocesar_todo = flg_reprocesar_todo

    def procesar(self):
        if self.flg_reprocesar:
            #eliminar toda las series por symbol
            SerieSemanalModel.eliminar_x_symbol(cod_symbol=self.cod_symbol)

        # obtener las pre-series semanales
        pre_series = SerieDiariaReader.get_preseries_semanal(symbol=self.cod_symbol)
        
        # Insertar las pre series
        for item in pre_series:
            self.crear_serie_semanal(pre_serie=item)                     
        
    def crear_serie_semanal(self, pre_serie):
        serie_apertura = SerieDiariaReader.get_serie(self.cod_symbol, pre_serie.open_date)   
        serie_cierre = SerieDiariaReader.get_serie(self.cod_symbol, pre_serie.close_date)                        

        nu_serie = SerieSemanalModel(
            symbol = self.cod_symbol,
            fch_semana = pre_serie.fch_semana,
            anyo = pre_serie.anyo,
            semana = pre_serie.semana,
            cod_semana = Semana(pre_serie.anyo, pre_serie.semana).codigo(),
            imp_apertura = serie_apertura.imp_apertura,
            imp_maximo = pre_serie.high,
            imp_minimo = pre_serie.low,
            imp_cierre = serie_cierre.imp_cierre,
            fch_registro = date.today()
        )

        db.session.add(nu_serie)
        return nu_serie


