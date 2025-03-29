from model.variacionmensual import VariacionMensualModel
from model.seriemensual import SerieMensualModel
from reader.seriemensual import SerieMensualReader
from reader.variacionmensual import VariacionMensualReader
from domain.mes import Mes

import logging

logger = logging.getLogger(__name__)
from app import db

class VariacionMensualService:
    def generar_series(self, cod_symbol, fch_ini_procesamiento):
        mes_procesamiento = Mes.from_fecha(fch_ini_procesamiento)
        fch_mes_procesamiento = mes_procesamiento.to_fecha_mes()
        
        fch_mes_max = VariacionMensualReader.get_fch_mes_max(cod_symbol)

        self.del_series(cod_symbol, fch_mes_max, fch_mes_procesamiento)

        # Obtener las series mensuales
        series = self.get_series_mensuales(cod_symbol, fch_mes_procesamiento)

        self.procesar_series_mensuales(cod_symbol, series)

    def del_series(self, cod_symbol, fch_mes_max, fch_mes_procesamiento):
        if not fch_mes_max:
            return 0
        
        if fch_mes_max >= fch_mes_procesamiento:
            rows_affected = VariacionMensualModel.del_desde_fecha(cod_symbol, fch_mes_procesamiento)
            return rows_affected
        else:
            return 0

    def get_series_mensuales(self, cod_symbol, fch_mes_ini_procesamiento):
        series = SerieMensualReader.get_series_desde_fecha(cod_symbol, fch_mes_ini_procesamiento)          
        if len(series) == 0:
            raise Exception(f"No se han encontrado series para symbol: {cod_symbol} y fecha: {fch_mes_ini_procesamiento.isoformat()}")
            
        return series

    def get_primera_serie(self, series):
        if series:
            return series[0]

    def get_serie_mensual_anterior(self, cod_symbol, fch_serie):
        serie_anterior = SerieMensualReader.get_serie_anterior(cod_symbol, fch_serie)
        return serie_anterior


    def procesar_series_mensuales(self, cod_symbol, series):
        primera_serie = self.get_primera_serie(series)
        serie_anterior = self.get_serie_mensual_anterior(cod_symbol, primera_serie.fch_mes)

        for serie_mensual in series:
            self.ins_variacion_serie(cod_symbol, serie_mensual, serie_anterior)
            serie_anterior = serie_mensual

    def ins_variacion_serie(self, cod_symbol, serie_mensual, serie_mensual_anterior):
        imp_cierre_ant = 0
        imp_variacion_cierre = 0
        pct_variacion_cierre = 0
        imp_variacion_maximo = 0
        pct_variacion_maximo = 0
        imp_variacion_minimo = 0
        pct_variacion_minimo = 0

        if serie_mensual_anterior:
            imp_cierre_ant = float(serie_mensual_anterior.imp_cierre)
            imp_variacion_cierre = float(serie_mensual.imp_cierre) - imp_cierre_ant
            pct_variacion_cierre = (float(serie_mensual.imp_cierre) - imp_cierre_ant)/imp_cierre_ant
            imp_variacion_maximo = float(serie_mensual.imp_maximo) - imp_cierre_ant
            pct_variacion_maximo = (float(serie_mensual.imp_maximo) - imp_cierre_ant)/imp_cierre_ant
            imp_variacion_minimo = float(serie_mensual.imp_minimo) - imp_cierre_ant
            pct_variacion_minimo = (float(serie_mensual.imp_minimo) - imp_cierre_ant)/imp_cierre_ant

        
        mes_serie = Mes.from_fecha(serie_mensual.fch_mes)

        new_serie = VariacionMensualModel(
            cod_symbol=cod_symbol,
            fch_mes=serie_mensual.fch_mes,
            cod_mes=mes_serie.codigo(),
            anyo=serie_mensual.anyo,
            mes=serie_mensual.mes,
            imp_cierre_ant=imp_cierre_ant,
            imp_apertura=serie_mensual.imp_apertura,
            imp_maximo=serie_mensual.imp_maximo,
            imp_minimo=serie_mensual.imp_minimo,
            imp_cierre=serie_mensual.imp_cierre,
            pct_variacion_cierre=pct_variacion_cierre,
            imp_variacion_cierre=imp_variacion_cierre,
            pct_variacion_maximo=pct_variacion_maximo,
            imp_variacion_maximo=imp_variacion_maximo,
            pct_variacion_minimo=pct_variacion_minimo,
            imp_variacion_minimo=imp_variacion_minimo
        )
        
        db.session.add(new_serie)
        return new_serie
