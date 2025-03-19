from model.variacionsemanal import VariacionSemanalModel
from model.seriesemanal import SerieSemanalModel
from reader.seriesemanal import SerieSemanalReader

class ReprocesadorVariacionSemanalService:
    def __init__(self, cod_symbol, flg_reprocesar_todo):
        self.cod_symbol = cod_symbol
        self.flg_reprocesar_todo = flg_reprocesar_todo

    def reprocesar(self):

        # eliminar symbol
        VariacionSemanalModel.eliminar_x_symbol(cod_symbol=self.cod_symbol)

        # obtener las series
        series = SerieSemanalReader.get_series_desde_fecha(symbol=self.cod_symbol)

        # por cada pre_serie crear 
        serie_ant = None
        for serie_semanal in series:
            self.__crear_variacion_semanal(serie_semanal=serie_semanal, serie_semanal_anterior=serie_ant)
            serie_ant = serie_semanal
            
    def __crear_variacion_semanal(self, serie_semanal:SerieSemanalModel, serie_semanal_anterior:SerieSemanalModel=None):
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
            symbol=self.cod_symbol,
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


    