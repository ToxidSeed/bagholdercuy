from domain.semana import CodigoSemana
from domain.mes import Mes
from common.AppException import AppException
from model.seriediaria import SerieDiariaModel
from datetime import date
from app import db

class SerieManager:
    def __init__(self):
        pass

    def crear_serie(self, cod_symbol, serie_):
        pass

class SimpleSerieManager:
    def __init__(self):
        pass

    def crear_serie(self, cod_symbol, serie):
        fch_serie, imp_cierre, ctd_volumen, imp_apertura, imp_maximo, imp_minimo = serie
        fch_semana = CodigoSemana(fch_serie).to_fecha_inicio_semana()
        fch_mes = Mes.from_fecha(fch_serie).to_fecha_primer_dia()

        if imp_apertura in [None, 0]:
            raise AppException(msg=f"imp apertura invalido None o 0, {str(serie)}")

        nueva_serie_diaria = SerieDiariaModel(
            symbol=cod_symbol,
            fch_serie=fch_serie,
            fch_semana=fch_semana,
            fch_mes=fch_mes,
            imp_apertura=imp_apertura,
            imp_maximo=imp_maximo,
            imp_minimo=imp_minimo,
            imp_cierre=imp_cierre,
            imp_apertura_ajus=imp_apertura,
            imp_maximo_ajus=imp_maximo,
            imp_minimo_ajus=imp_minimo,
            imp_cierre_ajus=imp_cierre,
            fch_registro=date.today()
        )

        db.session.add(nueva_serie_diaria)
        return nueva_serie_diaria
