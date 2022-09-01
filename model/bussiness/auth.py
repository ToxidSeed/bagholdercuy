import jwt
from config.general import AUTH_SECRET_KEY
from flask import request
from datetime import datetime
from model.usuario import UsuarioModel

class TokenHandler:    
    def verificar(self, access_token):               
        data = jwt.decode(access_token, AUTH_SECRET_KEY, algorithms=["HS256"])
        exp = data.get("exp")
        dt = datetime.fromtimestamp(exp)

        user = UsuarioModel.query.filter(
            UsuarioModel.usuario == data.get('usuario')
        ).one()
        return user
        


