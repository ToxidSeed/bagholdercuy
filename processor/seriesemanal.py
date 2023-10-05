from app import db
from reader.seriediaria import SerieDiariaReader
from datetime import date
from model.seriesemanal import SerieSemanalModel

class SerieSemanalLoader():   
    def __init__(self):
        self.symbol = None
        self.anyo = None
        self.semana = None
        self.fch_semana_inicio = None     

    def procesar(self,symbol, anyo = None, semana = None):                
        self.symbol = symbol
        self.anyo = anyo
        self.semana = semana
        
        if anyo is not None and semana is not None:
            self.fch_semana_inicio = date.fromisocalendar(anyo, semana, 1)
        
        self.__eliminar_series_semanales()
        
                #(anyo, semana_ini) = self.eliminar_serie_semanal(symbol=symbol, profundidad=profundidad)
        base = SerieDiariaReader.get_preseries_semanal(self.symbol, self.fch_semana_inicio)        
                
        fch_registro = date.today()
        for preserie_semana in base:            
            self._procesar_serie(symbol=symbol, preserie_semana=preserie_semana, fch_registro=fch_registro)

    def __eliminar_series_semanales(self):
        
        stmt = (
            db.delete(SerieSemanalModel).
            where(SerieSemanalModel.symbol == self.symbol)
        )

        if self.fch_semana_inicio is not None:
            stmt = stmt.where(
                SerieSemanalModel.fch_semana >= self.fch_semana_inicio        
            )

        db.session.execute(stmt)
    
    def _procesar_serie(self,symbol, preserie_semana, fch_registro):
        serie_apertura = SerieDiariaReader.get_serie(symbol, preserie_semana.open_date)   
        serie_cierre = SerieDiariaReader.get_serie(symbol, preserie_semana.close_date)                        

        nueva_serie_semanal = SerieSemanalModel(
            symbol = preserie_semana.symbol,
            fch_semana = preserie_semana.fch_semana,
            anyo = preserie_semana.anyo,
            semana = preserie_semana.semana,
            imp_apertura = serie_apertura.imp_apertura,
            imp_maximo = preserie_semana.high,
            imp_minimo = preserie_semana.low,
            imp_cierre = serie_cierre.imp_cierre,
            imp_apertura_ajus = serie_apertura.imp_apertura_ajus,
            imp_maximo_ajus = preserie_semana.adj_high,
            imp_minimo_ajus = preserie_semana.adj_low,
            imp_cierre_ajus = serie_cierre.imp_cierre_ajus
        )

        db.session.add(nueva_serie_semanal)