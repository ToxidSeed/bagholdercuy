from model.usuario import UsuarioModel
from model.bussiness.auth import TokenHandler
from common.AppException import AppException
from app import app
import jwt
from datetime import datetime

class Base:
    AUTH_REQUIRED = True

    def __init__(self, **kwargs):
        self._cuenta_default = None
                        
    def validar_token(self, access_token=None):
        if access_token in [None,""]:
            raise AppException(msg="No se ha enviado el token de acceso")

        data = jwt.decode(access_token, app.config.get("AUTH_SECRET_KEY"), algorithms=["HS256"])
        exp = data.get("exp")
        dt = datetime.fromtimestamp(exp)

        nom_usuario = data.get('usuario')
        usuario = UsuarioModel.get_user_safe(nom_usuario)

        self._cuenta_default = usuario.id_cuenta_default
        return usuario
         

    



        




