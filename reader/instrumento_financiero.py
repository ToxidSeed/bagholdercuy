from app import db
from model.instrumento_financiero import InstrumentoFinancieroModel

class InstrumentoFinancieroReader:
    @staticmethod
    def get_list(**filters):
        stmt = db.select(
            InstrumentoFinancieroModel
        )

        result = db.session.execute(stmt)
        return result.scalars().all()