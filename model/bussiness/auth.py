import jwt
from app import app
from flask import request
from datetime import datetime
from model.usuario import UsuarioModel


class TokenHandler:    
    def verificar(self, access_token):               
        data = jwt.decode(access_token, app.config.get("AUTH_SECRET_KEY"), algorithms=["HS256"])
        exp = data.get("exp")
        dt = datetime.fromtimestamp(exp)

        user = UsuarioModel.query.filter(
            UsuarioModel.usuario == data.get('usuario')
        ).one()
        return user
        