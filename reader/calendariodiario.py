from model.calendariodiario import CalendarioDiarioModel
from app import db

class CalendarioDiarioReader:
    def get(fch_dia):
        stmt = db.select(
            CalendarioDiarioModel
        ).where(
            CalendarioDiarioModel.fch_dia == fch_dia
        )

        result = db.session.execute(stmt)
        record = result.scalars().first()
        return record

    def get_fechas_x_semana(num_anyo_semana=None, num_semana=None, fch_semana=None, cod_semana=None):
        stmt = db.select(
            CalendarioDiarioModel
        ).where(
            CalendarioDiarioModel.num_anyo_semana == num_anyo_semana,
            CalendarioDiarioModel.num_semana == num_semana
        )

        return db.session.execute(stmt)

    def get_fechas_rango(fch_desde, fch_hasta=None):
        stmt = db.select(
            CalendarioDiarioModel
        ).where(
            CalendarioDiarioModel.fch_dia >= fch_desde
        )

        if fch_hasta is not None:
            stmt = stmt.where(
                CalendarioDiarioModel.fch_dia <= fch_hasta
            )
        
        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records  

    