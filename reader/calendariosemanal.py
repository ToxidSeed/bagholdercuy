from model.CalendarioSemanal import CalendarioSemanalModel
from app import db

class CalendarioSemanalReader:
    def get_fch_inicio_semana(fch_referencia):
        stmt = db.select(CalendarioSemanalModel).where(
            CalendarioSemanalModel.fch_inicio >= fch_referencia,
            CalendarioSemanalModel.fch_fin <= fch_referencia
        )
        return db.session.execute(stmt)
