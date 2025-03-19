from typing import List
from app import app, db
from collections import namedtuple
from reader.seriediaria import SerieDiariaReader
from model.seriediaria import SerieDiariaModel

WRITE_MODE_AGREGAR = app.config["WRITE_MODE_AGREGAR"]
WRITE_MODE_REEMPLAZAR = app.config["WRITE_MODE_REEMPLAZAR"]

class SerieDiariaHelper:
    
    def crear_serie_diaria(self, raw_serie_diaria):
        
        imp_aper_sin_ajus, imp_max_sin_ajus, imp_min_sin_ajus, imp_cierre_sin_ajus = self.calc_imp_sin_ajustar(cod_symbol, raw_serie_diaria)        
        fch_semana = Semana.from_fecha(fch_serie).fch_semana()
        fch_mes = Mes.from_fecha(fch_serie).to_fecha_mes()

        serie_nu = SerieDiariaModel(
            cod_symbol=cod_symbol,
            fch_serie=fch_serie,
            fch_semana=fch_semana,
            fch_mes=fch_mes,
            imp_apertura=imp_apertura,
            imp_maximo=imp_maximo,
            imp_minimo=imp_minimo,
            imp_cierre=imp_cierre,
            imp_apertura_sin_ajus=imp_aper_sin_ajus,
            imp_maximo_sin_ajus=imp_max_sin_ajus,
            imp_minimo_sin_ajus=imp_min_sin_ajus,
            imp_cierre_sin_ajus=imp_cierre_sin_ajus,
            fch_registro=date.today()
        )

        db.session.add(serie_nu)   






        

class SerieAjustadaHelper:
    def get_fch_inicio_proceso(self, cod_symbol, fch_primera_serie):
        fch_inicio_proceso = None
        result = SerieDiariaReader.get_fecha_maxima_x_symbol(cod_symbol)
        max_fch_serie = result.max_fch_serie     

        if max_fch_serie is None:
            fch_inicio_proceso = fch_primera_serie            
        elif max_fch_serie >= fch_primera_serie:
            d = timedelta(days=1)
            fch_inicio_proceso = max_fch_serie + d
        elif max_fch_serie < fch_primera_serie:
            fch_inicio_proceso = fch_primera_serie
        
        return fch_inicio_proceso   

class SerieDiariaService:
    def __init__(self):
        pass

    def get_factor_acum_from_memory(self, fch_serie:date):
        # revisamos los splits
        for fch_split, fch_split_ant, factor_acum in self.splits:
            if fch_split > fch_serie and fch_serie >= fch_split_ant:
                return factor_acum        

        # Si no se encuentra no devuelve nada        
        return None

    def get_factor_acum(self, cod_symbol, fch_serie:date):
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

    def insertar_multiples_series(self, cod_symbol, series, flg_series_ajustadas=True, mode=WRITE_MODE_AGREGAR):
        if not series:
            raise Exception("No hay series que insertar")

        primera_serie = series[0]

        for serie in series:
            self.insertar_serie(serie)

    def insertar_serie(self, cod_symbol, serie, flg_importes_ajustados=True):
        imp_factor_acum = self.get_factor_acum(cod_symbol, serie.fch_serie)
        if flg_importes_ajustados == True:
            importes_sin_ajustar = self.calc_importes_sin_ajustar(cod_symbol, serie, imp_factor_acum)
            self.crear_serie(self, cod_symbbol, serie, importes_sin_ajustar)

        elif flg_importes_ajustados == False:
            pass

        else:
            print("Indicador de tipos de importes no soportado")



    def calc_importes_sin_ajustar(self, cod_symbol,  serie, imp_factor_acum):
        ImportesSinAjustar = namedtuple("ImportesSinAjustar", ["imp_aper_sin_ajus", "imp_max_sin_ajus", "imp_min_sin_ajus", "imp_cierre_sin_ajus"])
        
        fch_serie, imp_apertura, imp_cierre, imp_maximo, imp_minimo, volumen = serie
        # imp_factor = self.get_factor_acum(cod_symbol=cod_symbol, fch_serie=fch_serie)

        imp_aper_sin_ajus = imp_apertura / imp_factor_acum
        imp_max_sin_ajus = imp_maximo / imp_factor_acum
        imp_min_sin_ajus = imp_minimo / imp_factor_acum        
        imp_cierre_sin_ajus = imp_cierre / imp_factor_acum        
        
        return ImportesSinAjustar(imp_aper_sin_ajus, imp_max_sin_ajus, imp_min_sin_ajus, imp_cierre_sin_ajus)        

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

