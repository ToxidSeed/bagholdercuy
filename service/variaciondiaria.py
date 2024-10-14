from model.variaciondiaria import VariacionDiariaModel
from model.seriediaria import SerieDiariaModel
from reader.seriediaria import SerieDiariaReader
from app import db

class VariacionDiariaProcesador:
    def __init__(self, cod_symbol, flg_reprocesar=False, flg_reprocesar_todo=False):
        self.cod_symbol = cod_symbol
        self.flg_reprocesar = flg_reprocesar
        self.flg_reprocesar_todo = flg_reprocesar_todo

    def procesar(self):
        if self.flg_reprocesar:
            VariacionDiariaModel.eliminar_x_symbol(cod_symbol=self.cod_symbol)
        
        # obtener las series diarias
        series = SerieDiariaReader.get_series_desde_fecha(symbol=self.cod_symbol)
        
        serie_ant = None
        for serie_diaria in series:            
            self.crear_variacion_diaria(serie_diaria, serie_ant)
            serie_ant = serie_diaria

        #return 
        return len(series)
    
    def crear_variacion_diaria(self, serie_diaria: SerieDiariaModel, serie_diaria_ant: SerieDiariaModel=None):

        imp_cierre_ant = 0
        imp_variacion_cierre = 0
        pct_variacion_cierre = 0
        imp_variacion_apertura = 0
        pct_variacion_apertura = 0
        imp_variacion_maximo = 0
        pct_variacion_maximo = 0
        imp_variacion_minimo = 0
        pct_variacion_minimo = 0
        imp_variacion_maximo_minimo = 0

        if serie_diaria_ant:
            if serie_diaria_ant.fch_serie >= serie_diaria.fch_serie:
                raise Exception("La fecha de la serie anterior es mayor a la fecha de la serie que se está procesando")

            imp_cierre_ant = float(serie_diaria_ant.imp_cierre)
            imp_variacion_cierre = float(serie_diaria.imp_cierre) - imp_cierre_ant
            pct_variacion_cierre = ((float(serie_diaria.imp_cierre) - imp_cierre_ant)/imp_cierre_ant)*100
            imp_variacion_apertura = float(serie_diaria.imp_apertura) - imp_cierre_ant
            pct_variacion_apertura = ((float(serie_diaria.imp_apertura) - imp_cierre_ant)/imp_cierre_ant)*100
            imp_variacion_maximo = float(serie_diaria.imp_maximo) - imp_cierre_ant
            pct_variacion_maximo = ((float(serie_diaria.imp_maximo) - imp_cierre_ant)/imp_cierre_ant)*100
            imp_variacion_minimo = float(serie_diaria.imp_minimo) - imp_cierre_ant
            pct_variacion_minimo = ((float(serie_diaria.imp_minimo) - imp_cierre_ant)/imp_cierre_ant)*100
            imp_variacion_maximo_minimo = float(serie_diaria.imp_maximo) - float(serie_diaria_ant.imp_minimo)


        new_serie = VariacionDiariaModel(
            symbol=serie_diaria.symbol,
            fch_serie=serie_diaria.fch_serie,
            imp_cierre_ant=imp_cierre_ant,
            imp_apertura=serie_diaria.imp_apertura,
            imp_maximo=serie_diaria.imp_maximo,
            imp_minimo=serie_diaria.imp_minimo,
            imp_cierre=serie_diaria.imp_cierre,
            pct_variacion_cierre=pct_variacion_cierre, 
            imp_variacion_cierre=imp_variacion_cierre,
            pct_variacion_apertura=pct_variacion_apertura,
            imp_variacion_apertura=imp_variacion_apertura,
            pct_variacion_maximo=pct_variacion_maximo,
            imp_variacion_maximo=imp_variacion_maximo,
            pct_variacion_minimo=pct_variacion_minimo,
            imp_variacion_minimo=imp_variacion_minimo,
            imp_variacion_maximo_minimo=imp_variacion_maximo_minimo
        )

        db.session.add(new_serie)
        return new_serie