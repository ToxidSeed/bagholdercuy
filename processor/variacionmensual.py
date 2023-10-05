from datetime import date
from model.variacionmensual import VariacionMensualModel
from reader.seriemensual import SerieMensualReader
from app import db

from datetime import timedelta

class VariacionMensualWriter:
    def __init__(self):
        self.symbol = None
        self.anyo = None
        self.mes = None
        self.fch_ini_mes = None

    def procesar(self, symbol, anyo=None, mes = None):
        self.symbol = symbol
        self.anyo = anyo
        self.mes = mes

        if anyo is not None and mes is not None:
            self.fch_ini_mes = date(year=anyo, month=mes, day=1)

        self.__eliminar()
        self.__crear()

    def __eliminar(self):
        if self.fch_ini_mes is None:
            self.__eliminar_todo()
        else:
            self.__eliminar_desde_fecha()

    def __eliminar_todo(self):  
        
        stmt = db.delete(VariacionMensualModel).where(
            VariacionMensualModel.symbol == self.symbol
        )

        db.session.execute(stmt)

    def __eliminar_desde_fecha(self):
        stmt = db.delete(VariacionMensualModel).where(
            VariacionMensualModel.symbol == self.symbol,
            VariacionMensualModel.fch_ini_mes >= self.fch_ini_mes
        )

        db.session.execute(stmt)

    def __crear(self):
        series = SerieMensualReader.get_series_desde_fecha(self.symbol, self.fch_ini_mes)

        if series is None:
            raise AppException(msg="No hay series mensuales")

        self._crear_elementos(series)


    def _crear_elementos(self, series):        

        serie_previa = None

        for serie_mensual in series:
            if serie_previa is None:
                serie_previa = self.__get_serie_previa(serie_mensual)                                        

            self.__crear_nueva_variacion_mensual(serie_mensual, serie_previa)
            serie_previa = serie_mensual
            

    def __get_serie_previa(self, serie_mensual):
        td = timedelta(days=-1)
        fch_referencia = serie_mensual.fch_ini_mes
        prev_anyo = fch_referencia.year
        prev_mes = fch_referencia.month
        prev_fch_mes = date(prev_anyo, prev_mes, 1)
        return SerieMensualReader.get_serie(serie_mensual.symbol, prev_fch_mes)

    def __crear_nueva_variacion_mensual(self, serie_mensual, serie_previa):
        
        imp_prev_cierre = float(serie_previa.imp_cierre)

        imp_variacion_cierre = float(serie_mensual.imp_cierre) - imp_prev_cierre
        pct_variacion_cierre = imp_variacion_cierre/imp_prev_cierre*100
        imp_variacion_apertura = float(serie_mensual.imp_apertura) - imp_prev_cierre
        pct_variacion_apertura = imp_variacion_apertura/imp_prev_cierre*100
        imp_variacion_maximo = float(serie_mensual.imp_maximo) - imp_prev_cierre
        pct_variacion_maximo = imp_variacion_maximo/imp_prev_cierre*100
        imp_variacion_minimo = float(serie_mensual.imp_minimo) - imp_prev_cierre
        pct_variacion_minimo = imp_variacion_minimo/imp_prev_cierre*100

        nueva_var_mensual = VariacionMensualModel(
            symbol = serie_mensual.symbol,
            fch_ini_mes = serie_mensual.fch_ini_mes,
            anyo = serie_mensual.fch_ini_mes.year,
            mes = serie_mensual.fch_ini_mes.month,
            imp_cierre_ant = imp_prev_cierre,            
            imp_apertura = serie_mensual.imp_apertura,
            imp_maximo = serie_mensual.imp_maximo,
            imp_minimo = serie_mensual.imp_minimo,
            imp_cierre = serie_mensual.imp_cierre,
            pct_variacion_cierre = pct_variacion_cierre,
            imp_variacion_cierre = imp_variacion_cierre,
            pct_variacion_apertura = pct_variacion_apertura,
            imp_variacion_apertura = imp_variacion_apertura,
            pct_variacion_maximo = pct_variacion_maximo,
            imp_variacion_maximo = imp_variacion_maximo,
            pct_variacion_minimo = pct_variacion_minimo,
            imp_variacion_minimo = imp_variacion_minimo        
        )    

        db.session.add(nueva_var_mensual)
    

    