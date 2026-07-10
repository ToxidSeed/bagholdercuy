from model.seriemensual import SerieMensualModel
from reader.seriediaria import SerieDiariaReader
from reader.seriemensual import SerieMensualReader
from domain.mes import Mes
from datetime import date

import logging

logger = logging.getLogger(__name__)
from config.extensions import db

class SerieMensualService:
    def generar_series(self, cod_symbol, fch_ini_procesamiento):
        mes_procesamiento = Mes.from_fecha(fch_ini_procesamiento)
        fch_mes_procesamiento = mes_procesamiento.to_fecha_mes()

        fch_mes_max = SerieMensualReader.get_max_fch_mes(cod_symbol)

        # Eliminar si es que se traslapan series
        self.del_series(cod_symbol, fch_mes_max, fch_mes_procesamiento)

        # Obtener las preseries
        pre_series = self.get_preseries_mensual(cod_symbol, fch_mes_procesamiento)

        # procesar por pre series
        self.procesar_pre_series(cod_symbol, pre_series)

    def procesar_pre_series(self, cod_symbol, pre_series):
        for pre_serie in pre_series:
            self.ins_serie(cod_symbol, pre_serie)

    def ins_serie(self, cod_symbol, pre_serie):
        anyo, mes = Mes.from_fecha(pre_serie.fch_mes).to_partes()
        serie_apertura = SerieDiariaReader.get_serie(cod_symbol, pre_serie.fch_apertura)
        serie_cierre = SerieDiariaReader.get_serie(cod_symbol, pre_serie.fch_cierre)

        nueva_serie = SerieMensualModel(
            cod_symbol=pre_serie.cod_symbol,
            fch_mes=pre_serie.fch_mes,
            anyo=anyo,
            mes=mes,
            imp_apertura=serie_apertura.imp_apertura,
            imp_maximo=pre_serie.imp_maximo,
            imp_minimo=pre_serie.imp_minimo,
            imp_cierre=serie_cierre.imp_cierre,
            fch_registro=date.today()
        )

        db.session.add(
            nueva_serie
        )

        return nueva_serie
        

    def del_series(self, cod_symbol, fch_mes_max, fch_mes_procesamiento):
        if not fch_mes_max:
            return 0

        if fch_mes_max >= fch_mes_procesamiento:
            rows_affected = SerieMensualModel.del_series_desde_fecha(cod_symbol, fch_mes_procesamiento)
            return rows_affected
        else:
            return 0

    def get_preseries_mensual(self, cod_symbol, fch_mes_inicio_procesamiento):
        records = SerieDiariaReader.get_preseries_mensual(cod_symbol, fch_mes_inicio_procesamiento)
        if not records:
            raise Exception(f"No se han encontrado preseries para cod_symbol: {cod_symbol}, fch_mes_inicio_procesamiento: {fch_mes_inicio_procesamiento}") 

        return records




class SerieMensualProcesador:
    def __init__(self, cod_symbol, flg_reprocesar=False, flg_reprocesar_todo=False):
        self.cod_symbol = cod_symbol
        self.flg_reprocesar = flg_reprocesar
        self.flg_reprocesar_todo = flg_reprocesar_todo

    def procesar(self):
        if self.flg_reprocesar:
            SerieMensualModel.eliminar_x_symbol(cod_symbol=self.cod_symbol)

        #obtener pre-series mensuales
        pre_series = SerieDiariaReader.get_preseries_mensual(symbol=self.cod_symbol)

        #por cada serie crear        
        for pre_serie_mensual in pre_series:
            self._crear_serie_mensual(pre_serie_mensual)


    def _crear_serie_mensual(self, pre_serie):

        anyo, mes = Mes.from_fecha(pre_serie.fch_mes).to_partes()
        serie_apertura = SerieDiariaReader.get_serie(self.cod_symbol, pre_serie.fch_apertura)
        serie_cierre = SerieDiariaReader.get_serie(self.cod_symbol, pre_serie.fch_cierre)

        nueva_serie = SerieMensualModel(
            symbol=pre_serie.symbol,
            fch_ini_mes=pre_serie.fch_mes,
            anyo=anyo,
            mes=mes,
            imp_apertura=serie_apertura.imp_apertura,
            imp_maximo=pre_serie.imp_maximo,
            imp_minimo=pre_serie.imp_minimo,
            imp_cierre=serie_cierre.imp_cierre,
            fch_registro=date.today()
        )

        db.session.add(
            nueva_serie
        )

        return nueva_serie