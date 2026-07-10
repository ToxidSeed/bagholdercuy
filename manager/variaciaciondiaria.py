from model.variaciondiaria import VariacionDiariaModel
from model.seriediaria import SerieDiariaModel
from config.extensions import db
from sqlalchemy import delete

class VariacionDiariaManager:
    def __init__(self):
        pass

    @staticmethod
    def eliminar_todo_x_symbol(cod_symbol):
        stmt = delete(VariacionDiariaModel).where(
            VariacionDiariaModel.symbol == cod_symbol
        )
        result = db.session.execute(stmt)
        return result

    def crear_variacion(self, serie: SerieDiariaModel, serie_anterior: SerieDiariaModel = None):

        imp_cierre_ant = float(serie.imp_apertura) if serie_anterior is None else float(serie_anterior.imp_cierre)
        imp_var_apertura = float(serie.imp_apertura) - imp_cierre_ant
        pct_var_apertura = imp_var_apertura/imp_cierre_ant
        imp_var_cierre = float(serie.imp_cierre) - imp_cierre_ant
        pct_var_cierre = round((imp_var_cierre/imp_cierre_ant)*100, 3)
        imp_var_maximo = float(serie.imp_maximo) - imp_cierre_ant
        pct_var_maximo = round(imp_var_maximo/imp_cierre_ant*100, 3)
        imp_var_minimo = float(serie.imp_minimo) - imp_cierre_ant
        pct_var_minimo = round(imp_var_minimo/imp_cierre_ant*100, 3)
        imp_var_maximo_minimo = float(serie.imp_maximo) - float(serie.imp_minimo)

        vdmo = VariacionDiariaModel(
            symbol=serie.cod_symbol,
            fch_serie=serie.fch_serie,
            imp_cierre_ant=imp_cierre_ant,
            imp_apertura=serie.imp_apertura,
            imp_maximo=serie.imp_maximo,
            imp_minimo=serie.imp_minimo,
            imp_cierre=serie.imp_cierre,
            imp_variacion_apertura=imp_var_apertura,
            pct_variacion_apertura=pct_var_apertura,
            imp_variacion_cierre=imp_var_cierre,
            pct_variacion_cierre=pct_var_cierre,
            imp_variacion_maximo=imp_var_maximo,
            pct_variacion_maximo=pct_var_maximo,
            imp_variacion_minimo=imp_var_minimo,
            pct_variacion_minimo=pct_var_minimo,
            imp_variacion_maximo_minimo=imp_var_maximo_minimo
        )
        db.session.add(vdmo)
        return vdmo

    

