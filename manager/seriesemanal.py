from config.extensions import db
from domain.semana import *
from model.seriesemanal import SerieSemanalModel
import datetime.date



class SerieSemanalRemover:
    def eliminar_x_symbol(self, cod_symbol):
        stmt = (
            db.delete(SerieSemanalModel).
            where(SerieSemanalModel.symbol == cod_symbol)
        )

        db.session.execute(stmt)

    def eliminar_desde_fecha(self, cod_symbol, fecha_semana_inicial):
        stmt = (
            db.delete(SerieSemanalModel).
            where(
                SerieSemanalModel.symbol == cod_symbol,
                SerieSemanalModel.fch_semana >= fecha_semana_inicial
            )
        )        

        db.session.execute(stmt)

class SerieSemanalCreator:
    def crear(self, cod_symbol, anyo, semana):
        # get pre series semana
        pass

    def crear_desde_pre_serie(self, pre_serie, imp_apertura, imp_maximo, imp_minimo, imp_cierre):
        ssm = SerieSemanalModel(
            symbol=pre_serie.symbol,
            fch_semana=pre_serie.fch_semana,
            anyo=pre_serie.anyo,
            semana=pre_serie.semana,
            cod_semana=Semana(pre_serie.anyo, pre_serie.semana).codigo(),
            imp_apertura=imp_apertura,
            imp_maximo=imp_maximo,
            imp_minimo=imp_minimo,
            imp_cierre=imp_cierre,
            fch_registro=date.today()
        )
        db.session.add(ssm)
        return ssm

