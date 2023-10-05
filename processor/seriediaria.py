from model.seriediaria import SerieDiariaModel
from app import db
from datetime import date

class SerieDiariaWriter:
    def __init__(self):
        self.symbol = None
        self.fch_ini_serie = None
        self.series = None

    def cargar(self, symbol, series=[], fch_ini_serie=None):
        self.symbol = symbol
        self.fch_ini_serie = fch_ini_serie
        self.series = series
        
        self.__eliminar()
        self.__crear_series()        

    def __eliminar(self):
        stmt = db.delete(
            SerieDiariaModel
        ).where(
            SerieDiariaModel.symbol == self.symbol
        )

        if self.fch_ini_serie is not None:
            stmt = stmt.where(
                SerieDiariaModel.fch_serie >= self.fch_ini_serie
            )
        
        db.session.execute(stmt)    

    def __crear_series(self):        
        for serie in self.series:
            fch_serie = date.fromisoformat(serie.get('date'))
            
            if self.fch_ini_serie is None:
                self.__crear_nueva_serie(serie)
                continue

            if fch_serie >= self.fch_ini_serie:
                self.__crear_nueva_serie(serie)
                continue

    def __crear_nueva_serie(self, serie):

        fch_serie = date.fromisoformat(serie.get('date'))
        anyo, semana, dia = fch_serie.isocalendar()
        fch_semana = date.fromisocalendar(anyo, semana, 1)
        fch_mes = date(fch_serie.year, fch_serie.month, 1)

        nueva_serie_diaria = SerieDiariaModel(
            symbol = serie.get('symbol'),
            fch_serie = serie.get('date'),
            fch_semana = fch_semana,
            fch_mes = fch_mes,
            imp_apertura = serie.get("uOpen"),
            imp_maximo = serie.get("uHigh"),
            imp_minimo = serie.get('uLow'),
            imp_cierre = serie.get('uClose'),
            imp_apertura_ajus = serie.get('open'),
            imp_maximo_ajus = serie.get('high'),
            imp_minimo_ajus = serie.get('low'),
            imp_cierre_ajus = serie.get('close'),
            fch_registro = date.today()
        )

        db.session.add(nueva_serie_diaria)

