from info.serie import SerieDiariaIntegridadInfo
from reader.seriediaria import SerieDiariaReader
from reader.stocksplit import StockSplitReader
from model.seriediaria import SerieDiariaModel
from model.stocksplit import StockSplitModel
import structure.inputfiles as inputfiles

from domain.semana import Semana
from domain.mes import Mes

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta

from collections import namedtuple

from app import app, db

WRITE_MODE_AGREGAR = app.config["WRITE_MODE_AGREGAR"]
WRITE_MODE_REEMPLAZAR = app.config["WRITE_MODE_REEMPLAZAR"]


@dataclass
class ReparacionStatus:
    cod_symbol: str = field(default="")
    msg: str = field(default="")

class SerieDiariaService:
    def __init__(self):
        self.splits = []    
        self.ctd_factores_acumulados = []

    def get_primera_serie(self, series):
        if not series:
            raise Exception("No hay series que insertar")
        
        primera_serie = series[0]
        return primera_serie

    def insertar_serie(self, cod_symbol, serie, flg_importes_ajustados):
        if flg_importes_ajustados == True:
            #split = self.get_split(cod_symbol, )
            factor_split = self.get_factor_split(cod_symbol, serie.fch_serie)
            importes_sin_ajustar = self.get_importes_sin_ajustar(cod_symbol, serie, factor_split, flg_importes_ajustados)
            importes_ajustados = self.get_importes_ajustados(serie, flg_importes_ajustados)
            self.crear_serie(cod_symbol, serie.fch_serie, importes_ajustados, importes_sin_ajustar)
        else:
            raise Exception("Todavia no esta la funcionalidad para procesar importes sin ajustar")

    def get_importes_sin_ajustar(self, cod_symbol, serie, factor_split, flg_importes_ajustados):
        importes_sin_ajustar = None
        if flg_importes_ajustados == True:
            importes_sin_ajustar = self.calc_importes_sin_ajustar(cod_symbol, serie, factor_split)            
        else:
            raise Exception("No hay calculo de importes sin ajustar")

        return importes_sin_ajustar

    def get_importes_ajustados(self, serie, flg_importes_ajustados):
        if flg_importes_ajustados == True:
            if isinstance(serie, inputfiles.CsvNasdaq):
                ImportesAjustados = namedtuple("ImportesAjustados", ["imp_apertura","imp_maximo","imp_minimo","imp_cierre"])
                importes_ajustados = ImportesAjustados(serie.imp_apertura, serie.imp_maximo, serie.imp_minimo, serie.imp_cierre)
                return importes_ajustados
            else:
                raise Exception(f"No hay soporte para otro tipo de serie, val: {type(serie).__name__}")
        else:
            raise Exception("no Hay calculo para importes sin ajustar")


    def insertar_multiples_series(self, cod_symbol, series, flg_importes_ajustados=True, mode=WRITE_MODE_AGREGAR):
                
        primera_serie = self.get_primera_serie(series)
        fch_inicio_insercion = self.get_fch_inicio_insercion(cod_symbol, primera_serie.fch_serie, mode=mode)

        if mode == WRITE_MODE_REEMPLAZAR:
            self.eliminar_series_a_reemplazar(cod_symbol, primera_serie.fch_serie)

        for serie in series:     
            if serie.fch_serie < fch_inicio_insercion:
                continue

            self.insertar_serie(cod_symbol, serie, flg_importes_ajustados)

        return fch_inicio_insercion
        

    def get_fch_inicio_insercion(self, cod_symbol, fch_primera_serie, mode):
        fch_inicio_proceso = None
        sdr = SerieDiariaReader()
        result = sdr.get_fecha_maxima_x_symbol(cod_symbol)
        max_fch_serie = result.max_fch_serie     

        if max_fch_serie is None:
            fch_inicio_proceso = fch_primera_serie            
        elif max_fch_serie >= fch_primera_serie:
            d = timedelta(days=1)
            fch_inicio_proceso = max_fch_serie + d
        elif max_fch_serie < fch_primera_serie:
            fch_inicio_proceso = fch_primera_serie
        
        return fch_inicio_proceso      

    def eliminar_series_a_reemplazar(self, cod_symbol, fch_primera_serie):        
        SerieDiariaModel.eliminar_x_symbol_desde_fecha(cod_symbol, fch_primera_serie)
        return fch_primera_serie

    def get_splits(self, cod_symbol):
        if self.splits:
            return self.splits

        self.splits = StockSplitReader.get_splits(cod_symbol)
        return self.splits

    def get_split(self, splits, fch_serie):
        splits_filtered = [stock_split for stock_split in splits if stock_split.fch_split >= fch_serie and fch_serie > stock_split.fch_split_anterior]
        if len(splits_filtered) == 0:
            return None
        elif len(splits_filtered) == 1:
            return splits_filtered[0]
        else:
            raise Exception(f"Hay mas de un split para una fecha, splits: {str(splits)}")

    def get_factor_split(self, cod_symbol, fch_serie):
        splits = self.get_splits(cod_symbol)
        stock_split = self.get_split(splits, fch_serie)
        if stock_split is None:
            return 1
        else:
            return stock_split.factor_split

    def get_factor_acum(self, cod_symbol, fch_serie:date):
        splits = self.get_splits(cod_symbol)
        if not splits:
            return 1
            
        factor_acum = self.get_factor_acum_from_memory(fch_serie=fch_serie)

        if factor_acum is not None:
            return factor_acum

        # Si no hay en memoria ir a base de datos
        split = StockSplitReader.get_split_por_fecha(cod_symbol=cod_symbol,fch_ref=fch_serie)

        # Si no hay en base de datos devolver 1 ya que no hay splits
        if split is None:
            # ponemos en memoria que no se ha encontrado en base de datos
            self.splits.append((date(9999,12,31),date(1000,1,1),1))
            return 1

        # Si se encuentra algun split obtenemos el factor acumulado
        factor_split_acum, splits = StockSplitReader.get_factor_split_acum(cod_symbol=split.cod_symbol, fch_split=split.fch_split)
        
        # añadimos lo que hemos encontrado a memoria
        self.splits.append((split.fch_split,split.fch_split_anterior,factor_split_acum))
        
        #devolvemos el split
        return factor_split_acum   

    def calc_importes_sin_ajustar(self, cod_symbol,  serie_ajustada, imp_factor_split):
        
        ImportesSinAjustar = namedtuple("ImportesSinAjustar", ["imp_aper_sin_ajus", "imp_max_sin_ajus", "imp_min_sin_ajus", "imp_cierre_sin_ajus"])            

        imp_aper_sin_ajus = serie_ajustada.imp_apertura / imp_factor_split
        imp_max_sin_ajus = serie_ajustada.imp_maximo / imp_factor_split
        imp_min_sin_ajus = serie_ajustada.imp_minimo / imp_factor_split        
        imp_cierre_sin_ajus = serie_ajustada.imp_cierre / imp_factor_split                
        importes_sin_ajustar =  ImportesSinAjustar(imp_aper_sin_ajus, imp_max_sin_ajus, imp_min_sin_ajus, imp_cierre_sin_ajus)        
        
        return importes_sin_ajustar

    def crear_serie(self, cod_symbol, fch_serie, importes_ajustados, importes_sin_ajustar):        

        fch_semana = Semana.from_fecha(fch_serie).fch_semana()
        fch_mes = Mes.from_fecha(fch_serie).to_fecha_mes()

        serie_nu = SerieDiariaModel(
            cod_symbol=cod_symbol,
            fch_serie=fch_serie,
            fch_semana=fch_semana,
            fch_mes=fch_mes,
            imp_apertura=importes_ajustados.imp_apertura,
            imp_maximo=importes_ajustados.imp_maximo,
            imp_minimo=importes_ajustados.imp_minimo,
            imp_cierre=importes_ajustados.imp_cierre,
            imp_apertura_sin_ajus=importes_sin_ajustar.imp_aper_sin_ajus,
            imp_maximo_sin_ajus=importes_sin_ajustar.imp_max_sin_ajus,
            imp_minimo_sin_ajus=importes_sin_ajustar.imp_min_sin_ajus,
            imp_cierre_sin_ajus=importes_sin_ajustar.imp_cierre_sin_ajus,
            fch_registro=date.today()
        )

        db.session.add(serie_nu)       


        

        

        
        

            
            





        

        
