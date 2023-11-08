from model.variaciondiaria import VariacionDiariaModel
from app import db
from sqlalchemy.sql import func

class VariacionDiariaReader:
    def get_valores_limites_entre_fechas(self, cod_symbol, fch_inicial, fch_final):
        query = db.select(
            func.max(VariacionDiariaModel.imp_maximo).label("imp_maximo"),
            func.min(VariacionDiariaModel.imp_minimo).label("imp_minimo")            
        ).where(
            VariacionDiariaModel.symbol == cod_symbol,
            VariacionDiariaModel.fch_serie >= fch_inicial,
            VariacionDiariaModel.fch_serie <= fch_final
        )

        result = db.session.execute(query)
        return result.first()