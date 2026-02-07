from reader.seriediaria import SerieDiariaReader
from reader.variaciondiaria import VariacionDiariaReader
from reader.seriesemanal import SerieSemanalReader
from reader.stocksplit import StockSplitReader
from dataclasses import dataclass
from domain.semana import CodigoSemana
from domain.mes import Mes
from model.stocksplit import StockSplitModel
from datetime import date
from common.AppException import AppException

from info.serie import SerieSemanalIntegridadInfo
from info.serie import SerieDiariaIntegridadInfo

CORRECTO = "correcto"
DEFECTUOSO = "defectuoso"
PCT_TOLERANCIA = 0.5

class SerieDiariaIntegridad:
        

    # retorna una tupla con los valores
    # split: bool = Si las series tienen splits
    # split_correcto: bool = si las series tienen los splits calculados correctamente
    # fch_split_reprocesar: La fecha del split mas reciente para reprocesar hacia atras
    def eval_splits(self, cod_symbol):
        # obtenemos los splits
        splits = StockSplitReader.get_splits(cod_symbol)        

        #Si no hay splits, entonces la validacion es correcta ya que al no haber splits no hayy nada que validar
        if len(splits) == 0:
            return (False, True, None)

        # Se evalua cada split para identificar si esta calculado correctamente
        split: StockSplitModel
        for split in splits:
            flg_split_correcto, fch_split = self.eval_single_split(split=split)
            if not flg_split_correcto:
                # Si encuentra un split incorrecto se corta el proceso
                return (True, False, fch_split)

        # Si no se encuentra ningun error en el split
        return (True, True, None)    
            

    def eval_single_split(self, split: StockSplitModel):        

        # obtener la serie correspondiente al dia en que el split se hizo efectivo
        serie = SerieDiariaReader.get_serie(symbol=split.cod_symbol, fch_serie=split.fch_split)
        if serie is None:
            raise AppException(msg=f"No se ha obtenido la serie para el symbol: {split.cod_symbol}, fch_serie: {str(split.fch_split)}")

        # obtener la serie previa a la fecha del split
        serie_previa = SerieDiariaReader.get_serie_anterior_a_fecha(cod_symbol=split.cod_symbol,fch_serie=split.fch_split, incluir_fecha=False)
        if serie_previa is None:
            raise AppException(msg=f"No se ha obtenido la seria previa para los siguientes datos: symbol: {split.cod_symbol}, fch_split: {str(split.fch_split)}")

        # calculamos que en el dia del split el importe de cierre del dia anterior no tenga una diferencia significativa
        # con la serie en el dia del split
        pct_var_apertura = abs(serie.imp_apertura - serie_previa.imp_cierre) / serie_previa.imp_cierre

        # si la tolerancia calculada es mayor a la permitida dar error
        if pct_var_apertura > PCT_TOLERANCIA:            
            return (False, split.fch_split)
        else:
            return (True, None)

    # devuelve una tupla con lo siguiente:
    # flg_separacion_correcta: bool = Si la separacion entre series es menor a 4
    # fch_separacion_referencia: date = fecha de la serie previa cuya separacion es incorrecta
    def eval_num_dias_serie_anterior(self, cod_symbol):
        
        # obtenemos las series
        record = SerieDiariaReader.get_min_fch_serie_x_num_dias_separacion(cod_symbol=cod_symbol, num_dias_separacion=4)

        # Si no hay ningun registro con dias de separacion mayor a lo representado                
        if record is None:
            return (True, None)

        fch_serie = record.fch_serie
        if fch_serie is None:
            return (True, None)

        # Obtener la fecha previa que es la que se va a reprocesar
        serie_referencia = SerieDiariaReader.get_serie_anterior_a_fecha(cod_symbol=cod_symbol, fch_serie=fch_serie, incluir_fecha=False)
        return (False, serie_referencia.fch_serie)


    def evaluar(self, cod_symbol) -> SerieDiariaIntegridadInfo:
    
        # revisamos los splits
        flg_split, flg_split_correcto, fch_split_reprocesar = self.eval_splits(cod_symbol=cod_symbol)
        
        # revisamos la separacion entre series
        # num_dias_separacion_correcto, fch_separacion_referencia = self.eval_num_dias_serie_anterior(cod_symbol=cod_symbol)

        # creamos el objeto de respuesta
        info = SerieDiariaIntegridadInfo(
            cod_symbol=cod_symbol,
            split=flg_split,
            split_correcto=flg_split_correcto,
            fch_split_reprocesar=fch_split_reprocesar
        )

        return info

class VariacionDiariaIntegridad:
    def __init__(self):
        self.min_fch_serie_correcto = True
        self.max_fch_serie_correcto = True
        self.cantidad_correcto = True
        self.correcto = True
        self.reprocesar = False
        self.reproceso_total = None        
        

    def eval_min_fch_serie(self, min_fch_serie_diaria, min_fch_variacion_diaria):
        self.min_fch_serie_correcto = (min_fch_serie_diaria == min_fch_variacion_diaria)
        return self.min_fch_serie_correcto

    def eval_max_fch_serie(self, max_fch_serie_diaria, max_fch_variacion_diaria):
        self.max_fch_serie_correcto = (max_fch_serie_diaria == max_fch_variacion_diaria)
        return self.max_fch_serie_correcto

    def eval_cantidad(self, cantidad_series_diarias, cantidad_variaciones_diarias):
        self.cantidad_correcto = (cantidad_series_diarias == cantidad_variaciones_diarias)
        return self.cantidad_correcto

    def evaluar(self, stats_series_diarias, stats_vars_diarias):
        evals = [
            self.eval_min_fch_serie(stats_series_diarias.min_fch_serie, stats_vars_diarias.min_fch_variacion),
            self.eval_max_fch_serie(stats_series_diarias.max_fch_serie, stats_vars_diarias.max_fch_variacion),
            self.eval_cantidad(stats_series_diarias.cantidad, stats_vars_diarias.cantidad)
        ]

        if False in evals:
            self.diagnostico = DEFECTUOSO
            self.reprocesar = True
            self.correcto = False        


class SerieSemanalIntegridad:
        
    def eval_min_cod_semana(self, min_fch_serie, min_cod_semana):
        cod_semana_obj = CodigoSemana.from_fecha(min_fch_serie)
        resp = (cod_semana_obj.value == min_cod_semana)        
        return resp

    def eval_max_cod_semana(self, max_fch_serie, max_cod_semana):
        cod_semana_obj = CodigoSemana.from_fecha(max_fch_serie)
        resp = (cod_semana_obj.value == max_cod_semana)
        return resp

    def eval_cantidad(self, min_cod_semana, max_cod_semana, cantidad):
        resp = (cantidad == Semana.diferencia(min_cod_semana, max_cod_semana))
        return resp

    def evaluar(self, stats_series_diarias, stats_series_semanales):
        info = SerieSemanalIntegridadInfo(
            min_cod_semana_correcto=self.eval_min_cod_semana(stats_series_diarias.min_fch_serie, stats_series_semanales.min_cod_semana),
            max_cod_semana_correcto=self.eval_max_cod_semana(stats_series_diarias.max_fch_serie, stats_series_semanales.max_cod_semana),
            cantidad_correcto=self.eval_cantidad(stats_series_semanales.min_cod_semana, stats_series_semanales.max_cod_semana, stats_series_diarias.cantidad)
        )

        return info

class VariacionSemanalIntegridad:
    def __init__(self):
        self.min_cod_semana_correcto = None
        self.max_cod_semana_correcto = None
        self.cantidad_correcto = None
        self.correcto = None
        self.reprocesar = None
        self.reproceso_total = None

    def eval_min_cod_semana(self, min_fch_serie, min_cod_semana):
        semana = Semana.from_fecha(min_fch_serie)
        self.min_cod_semana_correcto = (semana.codigo() == min_cod_semana)
        return self.min_cod_semana_correcto

    def eval_max_cod_semana(self, max_fch_serie, max_cod_semana):
        semana = Semana.from_fecha(max_fch_serie)
        self.max_cod_semana_correcto = (semana.codigo() == max_cod_semana)
        return self.max_cod_semana_correcto

    def eval_cantidad(self, min_cod_semana, max_cod_semana, cantidad):
        self.cantidad_correcto = (cantidad == Semana.diferencia(min_cod_semana, max_cod_semana))
        return self.cantidad_correcto

    def evaluar(self, stats_series_diarias, stats_vars_semanales):
        info = SerieSemanalIntegridadInfo(
            min_cod_semana_correcto=self.eval_min_cod_semana(stats_series_diarias.min_fch_serie, stats_vars_semanales.min_cod_semana),
            max_cod_semana_correcto=self.eval_max_cod_semana(stats_series_diarias.max_fch_serie, stats_vars_semanales.max_cod_semana),
            cantidad_correcto=self.eval_cantidad(stats_vars_semanales.min_cod_semana, stats_vars_semanales.max_cod_semana, stats_vars_semanales.cantidad)
        )

        return info        


class SerieMensualIntegridad:
    def __init__(self):
        self.min_fch_mes_correcto = None
        self.max_fch_mes_correcto = None
        self.cantidad_correcto = None
        self.correcto = None
        self.reprocesar = None
        self.reproceso_total = None

    def eval_min_fch_mes(self, min_fch_serie_diaria, fch_ini_mes):
        self.min_fch_mes_correcto = (Mes.from_fecha(min_fch_serie_diaria).to_fecha_mes())
        return self.min_fch_mes_correcto

    def eval_max_fch_mes(self, max_fch_serie_diaria, max_fch_mes):
        self.max_fch_mes_correcto = (Mes.from_fecha(max_fch_serie_diaria).to_fecha_mes())
        return self.max_fch_mes_correcto

    def eval_cantidad(self, min_fch_mes, max_fch_mes, cantidad):
        self.cantidad_correcto = (Mes.diferencia(min_fch_mes, max_fch_mes) == cantidad)
        return self.cantidad_correcto

    def evaluar(self, stats_series_diarias, stats_series_mensuales):
        evals = [
            self.eval_min_fch_mes(stats_series_diarias.min_fch_serie, stats_series_mensuales.min_fch_mes),
            self.eval_max_fch_mes(stats_series_diarias.max_fch_serie, stats_series_mensuales.max_fch_mes),
            self.eval_cantidad(stats_series_diarias.min_fch_mes, stats_series_mensuales.max_fch_mes, stats_series_mensuales.cantidad)
        ]

        self.correcto = (False in evals)    


class VariacionMensualIntegridad:
    def __init__(self):
        self.min_fch_mes_correcto = None
        self.max_fch_mes_correcto = None
        self.cantidad_correcto = None
        self.correcto = None
        self.reprocesar = None
        self.reproceso_total = None

    def eval_min_fch_mes(self, min_fch_serie_diaria, fch_ini_mes):
        self.min_fch_mes_correcto = (Mes.from_fecha(min_fch_serie_diaria).to_fecha_mes() == fch_ini_mes)
        return self.min_fch_mes_correcto

    def eval_max_fch_mes(self, max_fch_serie_diaria, max_fch_mes):
        self.max_fch_mes_correcto = (Mes.from_fecha(max_fch_serie_diaria).to_fecha_mes() == max_fch_mes)
        return self.max_fch_mes_correcto

    def eval_cantidad(self, min_fch_mes, max_fch_mes, cantidad):
        self.cantidad_correcto = (Mes.diferencia(min_fch_mes, max_fch_mes) == cantidad)
        return self.cantidad_correcto

    def evaluar(stats_series_diarias, stats_vars_mensuales):
        evals = [
            self.eval_min_fch_mes(stats_series_diarias.min_fch_serie, stats_vars_mensuales.min_fch_mes),
            self.eval_max_fch_mes(stats_series_diarias.max_fch_mes, stats_vars_mensuales.max_fch_mes),
            self.eval_cantidad(stats_series_diarias.min_fch_mes, stats_vars_mensuales.max_fch_mes)
        ]

        self.correcto = (False in evals)



        



        
    


