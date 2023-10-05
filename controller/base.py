from config.general import MARKET_API, MARKET_API_LIST
from model.usuario import UsuarioModel
from model.bussiness.auth import TokenHandler
from common.AppException import AppException

class Base:
    AUTH_REQUIRED = True    
                        
    def validar_token(self, access_token=None):
        if access_token in [None,""]:
            raise AppException(msg="No se ha enviado el token de acceso")

        self.usuario = TokenHandler().verificar(access_token)



        




