from config.extensions import db
from model.tipo_transaccion import TipoTransaccionModel

class TipoTransaccionReader:
    @staticmethod
    def get_list(**filters):
        stmt = db.select(
            TipoTransaccionModel
        )

        result = db.session.execute(stmt)
        return result.scalars().all()
