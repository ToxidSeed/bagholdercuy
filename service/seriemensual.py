from model.seriemensual import SerieMensualModel
from reader.seriediaria import SerieDiariaReader
from domain.mes import Mes
from datetime import date

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