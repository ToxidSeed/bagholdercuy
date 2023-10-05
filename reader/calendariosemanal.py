from model.CalendarioSemanal import CalendarioSemanalModel
from app import db

class CalendarioSemanalReader:
    def get_fch_inicio_semana(fch_referencia):
        stmt = db.select(CalendarioSemanalModel).where(
            CalendarioSemanalModel.fch_inicio >= fch_referencia,
            CalendarioSemanalModel.fch_fin >= fch_referencia
        )
        return db.session.execute(stmt)

    def get_por_num_semana(anyo, semana):
        stmt = db.select(CalendarioSemanalModel).where(
            CalendarioSemanalModel.anyo == anyo,
            CalendarioSemanalModel.semana == semana
        )

        result = db.session.execute(stmt)
        return result.scalars().first()

    def get_semana_x_fecha(fch_referencia):
        stmt = db.select(CalendarioSemanalModel).where(
            CalendarioSemanalModel.fch_inicio <= fch_referencia,
            CalendarioSemanalModel.fch_fin >= fch_referencia
        )
        result = db.session.execute(stmt)
        return result.scalars().first()