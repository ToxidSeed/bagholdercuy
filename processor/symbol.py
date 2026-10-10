from config.extensions import db

from sqlalchemy import delete

from model.symbol import SymbolModel

class SymbolRemover:
    def eliminar_todo():
        stmt = (
            delete(SymbolModel)
        )

        db.session.execute(stmt)