from config.extensions import db
from model.symbol_type import SymbolTypeModel


class SymbolTypeReader:
    @staticmethod
    def get_list(**filters):
        stmt = db.select(
            SymbolTypeModel
        )

        result = db.session.execute(stmt)
        return result.scalars().all()