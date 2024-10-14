from info.serie import SerieSemanalIntegridadInfo
from reader.seriediaria import SerieDiariaReader
from model.seriesemanal import SerieSemanalModel
from datetime import date
from domain.semana import Semana


class SerieSemanalReprocesador:
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


