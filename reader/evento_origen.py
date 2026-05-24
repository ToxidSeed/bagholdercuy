from app import db
from model.evento_origen import EventoOrigenModel

class EventoOrigenReader:
    @staticmethod
    def get_list(**filters):
        stmt = db.select(EventoOrigenModel)
        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_by_code(code: str):
        stmt = db.select(EventoOrigenModel).where(EventoOrigenModel.cod_evento == code)
        result = db.session.execute(stmt)
        return result.scalar_one_or_none()
