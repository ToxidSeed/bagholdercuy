from app import db
from model.indicador_apcierre import IndicadorApcierreModel

class IndicadorApcierreReader:
    @staticmethod
    def get_list(**filters):
        stmt = db.select(IndicadorApcierreModel)
        result = db.session.execute(stmt)
        return result.scalars().all()
