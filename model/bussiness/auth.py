import jwt
from config.extensions import db, current_app
from model.usuario import UsuarioModel
from sqlalchemy import select


class TokenHandler:
    def verificar(self, access_token):
        data = jwt.decode(access_token, current_app.config.get("AUTH_SECRET_KEY"), algorithms=["HS256"])

        query = select(
            UsuarioModel.id,
            UsuarioModel.usuario,
            UsuarioModel.nombres,
            UsuarioModel.apellidos,
            UsuarioModel.id_cuenta_default
        ).where(
            UsuarioModel.usuario == data.get('usuario')
        )

        result = db.session.execute(query)
        user = result.one()
        return user
