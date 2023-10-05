from app import db
from model.usuario import UsuarioModel

class UsuarioReader:
    def get(id_usuario):
        stmt = db.select(
            UsuarioModel
        ).where(
            UsuarioModel.id == id_usuario
        )

        result = db.session.execute(stmt)
        return result.scalars().one()

    def get_usuarios(args={}):
        stmt = db.select(
            UsuarioModel
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records
        
