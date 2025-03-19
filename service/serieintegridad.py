from reader.seriediaria import SerieDiariaReader
from reader.variaciondiaria import VariacionDiariaReader
from reader.seriesemanal import SerieSemanalReader
from reader.stocksplit import StockSplitReader
from model.stocksplit import StockSplitModel
from collections import namedtuple
from typing import NamedTuple

CORRECTO = "correcto"
DEFECTUOSO = "defectuoso"
PCT_TOLERANCIA = 0.5

class SerieIntegridadService:
    def __init__(self):
        self.cod_symbol = None
        self.fch_primera_serie = None
        self.fch_ultima_serie = None
        self.fch_num_series = None
        self.num_dias_desactualizado = None        
        
    def evaluar(self, cod_symbol):
        sdi = SerieDiariaIntegridad()
        resp_eval_serie_diaria = sdi.evaluar(cod_symbol=cod_symbol)
        

    

class SerieDiariaIntegridad:      
    def __init__(self):
        self.splits = None

    def evaluar(self, cod_symbol):
        # Obtenemos los splits
        self.splits = self.get_splits_acum(cod_symbol=cod_symbol)

        # Obtenemos las series diarias
        series = SerieDiariaReader.get_series_desde_fecha(cod_symbol)

        # evaluar splits para las series
        flg_split_correcto = self.eval_splits(series=series)
        
        # evaluar el desfase de las series
        flg_desfase_correcto = self.eval_desfase(series=series)    

        # 
        result_eval = all([flg_split_correcto, flg_desfase_correcto])
        return result_eval


    def eval_desfase(self, series):
        fch_serie_ant = None
        for serie_item in series:
            if fch_serie_ant is None:
                fch_serie_ant = serie_item.fch_serie
                continue

            diff_date = serie_item.fch_serie - fch_serie_ant

            # Si es lunes
            if serie_item.fch_serie.weekday() == 0:
                if diff_date.days not in [2,3]:
                    return False
            else:
                if diff_date.days != 1:
                    return False
        
        return True  


    def eval_splits(self, series):        
        obs = []

        for serie_item in series:
            split_acum = self.get_split_factor(self.splits, serie_item.fch_serie)
            if serie_item.imp_apertura * split_acum != serie_item.imp_apertura_sin_ajus:
                obs.append(f"No coinciden los valores de apertura para la fecha {serie_item.fch_serie}")
                continue

            if serie_item.imp_maximo * split_acum != serie_item.imp_maximo_sin_ajus:
                obs.append(f"No coinciden los valores maximos para la fecha {serie_item.fch_serie}")
                continue

            if serie_item.imp_minimo * split_acum != serie_item.imp_maximo_sin_ajus:
                obs.append(f"No coinciden los valores minimos para la fecha {serie_item.fch_serie}")
                continue

            if serie_item.imp_cierre * split_acum != serie_item.imp_cierre_sin_ajus:
                obs.append(f"No coinciden los valores de cierre para la fecha {serie_item.fch_serie}")
                continue
        
        if len(obs) > 0:
            return False, obs
        else:
            return True, []
            

    def get_split_factor(self, splits, fch_serie):
        for fch_split, fch_split_anterior, split_acum in splits:
            if fch_split > fch_serie >= fch_split_anterior:
                return split_acum

        return 1

    def get_splits_acum(self, cod_symbol, series):
        splits = StockSplitReader.get_splits(cod_symbol=cod_symbol)
        if len(splits) == 0:
            return None
            
        records = []
        split_acum = 1
        for split_item in split:
            split_acum = split_acum * float(split_item.numerador) / float(split_item.denominador)
            records.append((split_item.fch_split, split_item.fch_split_anterior, split_acum))
        return records  

    