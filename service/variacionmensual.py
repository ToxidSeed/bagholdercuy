from model.variacionmensual import VariacionMensualModel
from model.seriemensual import SerieMensualModel
from reader.seriemensual import SerieMensualReader
from domain.mes import Mes

class VariacionMensualProcesador:
    def __init__(cod_symbol, flg_reprocesar=True, flg_reprocesar_todo=True):
        self.cod_symbol=cod_symbol
        self.flg_reprocesar=flg_reprocesar
        self.flg_reprocesar_todo=flg_reprocesar_todo

    def procesar():
        if self.flg_reprocesar:
            VariacionMensualModel.eliminar_x_symbol(cod_symbol=self.cod_symbol)
    
        # obtenemos las series
        series = SerieMensualReader.get_series_desde_fecha(symbol=self.cod_symbol)

        # por cada pre-serie crear
        serie_ant = None
        for serie_mensual in series:
            self.__crear_variacion_mensual(serie_mensual, serie_ant)
            serie_ant = serie_mensual
    
    def __crear_variacion_mensual(self, serie_mensual: SerieMensualModel, serie_mensual_anterior:SerieMensualModel):
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

        
        mes_serie = from_fecha(serie_mensual.fch_ini_mes)

        new_serie = VariacionMensualModel(
            symbol=self.cod_symbol,
            fch_ini_mes=serie_mensual.fch_ini_mes,
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




