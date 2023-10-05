from app import db
from model.variaciondiaria import VariacionDiariaModel

from reader.seriediaria import SerieDiariaReader
from model.seriediaria import SerieDiariaModel

class VariacionDiariaLoader:
    def __init__(self):
        self.symbol = None
        self.fch_ini_serie = None

    def procesar(self, symbol, fch_ini_serie=None):
        self.symbol = symbol
        self.fch_ini_serie = fch_ini_serie
        self.__eliminar()
        self.__crear()

    def __eliminar(self):
        if self.fch_ini_serie is None:
            self.__eliminar_todo()
        else:
            self.__eliminar_desde_fecha()

    def __eliminar_todo(self):
        stmt = db.delete(
            VariacionDiariaModel
        )

        db.session.execute(stmt)
    
    def __eliminar_desde_fecha(self):
        stmt = db.delete(
            VariacionDiariaModel
        ).where(
            VariacionDiariaModel.symbol == self.symbol,
            VariacionDiariaModel.fch_serie >= self.fch_ini_serie
        )

        db.session.execute(stmt)

    def __crear(self):
        series = SerieDiariaReader.get_series_desde_fecha(self.symbol, self.fch_ini_serie)

        if series is None:
            raise AppException(msg="No hay series diarias")

        self.__crear_elementos(series)

    def __crear_elementos(self, series):
        serie_diaria_previa = None

        for serie_diaria in series:
            if serie_diaria_previa is None:
                serie_diaria_previa = self.__get_serie_previa(serie_diaria)

            self.__crear_nueva_variacion_diaria(serie_diaria, serie_diaria_previa)
            serie_diaria_previa = serie_diaria

    def __get_serie_previa(self, serie_diaria:SerieDiariaModel):
        fch_serie_previa = SerieDiariaReader.get_fch_serie_previa(serie_diaria.symbol, serie_diaria.fch_serie)
        serie_previa = SerieDiariaReader.get_serie(serie_diaria.symbol, fch_serie_previa)
        return serie_previa

    def __crear_nueva_variacion_diaria(self, serie_diaria:VariacionDiariaModel, serie_diaria_previa:VariacionDiariaModel=None):\
        
        imp_cierre = float(serie_diaria.imp_cierre)

        if serie_diaria_previa is None:
            imp_cierre_ant = 0
            imp_variacion_cierre = imp_cierre
            pct_variacion_cierre = 100
            imp_variacion_apertura = float(serie_diaria.imp_apertura)
            pct_variacion_apertura = 100
            imp_variacion_maximo = float(serie_diaria.imp_maximo)
            pct_variacion_maximo = 100
            imp_variacion_minimo = 0
            pct_variacion_minimo = 0
        else:        
            imp_cierre_ant = float(serie_diaria_previa.imp_cierre)            
            imp_variacion_cierre = imp_cierre - imp_cierre_ant
            pct_variacion_cierre = (imp_cierre - imp_cierre_ant)/imp_cierre_ant*100        
            imp_variacion_apertura = float(serie_diaria.imp_apertura) - imp_cierre_ant
            pct_variacion_apertura = imp_variacion_apertura/imp_cierre_ant*100
            imp_variacion_maximo = float(serie_diaria.imp_maximo) - imp_cierre_ant
            pct_variacion_maximo = imp_variacion_maximo/imp_cierre_ant*100
            imp_variacion_minimo = float(serie_diaria.imp_minimo) - imp_cierre_ant    
            pct_variacion_minimo = imp_variacion_minimo/imp_cierre_ant*100
        
        var_diaria_nuevo = VariacionDiariaModel(
            symbol = serie_diaria.symbol,
            fch_serie = serie_diaria.fch_serie,
            imp_cierre_ant = imp_cierre_ant,
            imp_apertura = serie_diaria.imp_apertura,
            imp_maximo = serie_diaria.imp_maximo,
            imp_minimo = serie_diaria.imp_minimo,
            imp_cierre = serie_diaria.imp_cierre,
            pct_variacion_cierre = pct_variacion_cierre,
            imp_variacion_cierre = imp_variacion_cierre,
            imp_variacion_apertura = imp_variacion_apertura,
            pct_variacion_apertura = pct_variacion_apertura,
            imp_variacion_maximo = imp_variacion_maximo,
            pct_variacion_maximo = pct_variacion_maximo,
            imp_variacion_minimo = imp_variacion_minimo,
            pct_variacion_minimo = imp_variacion_minimo
        )

        db.session.add(var_diaria_nuevo)