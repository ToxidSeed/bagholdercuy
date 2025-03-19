from model.variaciondiaria import VariacionDiariaModel
from model.seriediaria import SerieDiariaModel
from reader.seriediaria import SerieDiariaReader
from reader.variaciondiaria import VariacionDiariaReader
from app import app, db

WRITE_MODE_AGREGAR = app.config["WRITE_MODE_AGREGAR"]
WRITE_MODE_REEMPLAZAR = app.config["WRITE_MODE_REEMPLAZAR"]

class VariacionDiariaService:
    def __init__(self):
        pass

    # generará las variaciones desde el valor fch_desde    
    def generar_variaciones(self, cod_symbol, fch_primera_serie):
        fch_max_variacion = VariacionDiariaReader.get_max_fch_variacion(cod_symbol=cod_symbol)

        # Si fch_max_variacion es None se procesa todo
        if fch_max_variacion is None:
            series = self.get_series_desde_fecha(cod_symbol=cod_symbol, fch_serie=fch_primera_serie)
            self.crear_variaciones_diarias(series=series)

        else:
            # Eliminamos todos los registros de variacion incluyendo la primera serie diaria que se ha procesado
            VariacionDiariaModel.eliminar_x_symbol_desde_fecha(cod_symbol=cod_symbol, fch_desde=fch_primera_serie)

            # Obtenemos la serie anterior a la primera serie
            serie_diaria_previa = SerieDiariaReader.get_serie_anterior_a_fecha(cod_symbol, fch_primera_serie)
            self.crear_variaciones_diarias(series=series, serie_ant=serie_diaria_previa)

    def get_series_desde_fecha(self, cod_symbol, fch_serie):
        series = SerieDiariaReader.get_series_desde_fecha(symbol=cod_symbol, fch_serie=fch_serie)
        if len(series) == 0:
            raise Exception(f"No se han encontrado series diarias para symbol={cod_symbol}, fch_serie={fch_serie_inicial.isoformat()}")
        return series

    def crear_variaciones_diarias(self, series, serie_ant=None):        
        for serie_diaria in series:            
            self.crear_variacion_diaria(serie_diaria, serie_ant)
            serie_ant = serie_diaria        

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
            symbol=serie_diaria.cod_symbol,
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