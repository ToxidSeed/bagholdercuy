import jwt
from app import app, db
from flask import request
from datetime import datetime
from model.usuario import UsuarioModel
from sqlalchemy import select


class TokenHandler:    
    def verificar(self, access_token):               
        data = jwt.decode(access_token, app.config.get("AUTH_SECRET_KEY"), algorithms=["HS256"])
        exp = data.get("exp")
        dt = datetime.fromtimestamp(exp)

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
        