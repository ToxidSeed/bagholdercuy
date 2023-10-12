import hashlib, jwt
from datetime import timedelta, datetime, timezone
from model.usuario import UsuarioModel
from common.AppException import AppException
from common.Response import Response
from common.logger import logger
from reader.cuenta import CuentaReader

from config.general import AUTH_SECRET_KEY
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from app import db
import logging


class LoginController:
    AUTH_REQUIRED = False

    def login(self, args={}):
        try:
            usuario = args.get('usuario')
            password = args.get('password')
            userdb = None
            cuenta = None
            token = ""

            passdb = hashlib.sha224("{0}{1}".format(usuario,password).encode("utf-8")).hexdigest()
        
            userdb = UsuarioModel.query.filter(
                UsuarioModel.usuario == usuario
            ).one()    

            if passdb == userdb.password:
                id_cuenta_default = userdb.id_cuenta_default
                if id_cuenta_default is None:
                    raise AppException(msg="El usuario no tiene asociada una cuenta")

                cuenta = CuentaReader.get(id_cuenta=id_cuenta_default)
                token = self._crear_token(usuario=usuario)
            else:
                raise AppException(msg="Usuario o password incorrectos")

            return Response().from_raw_data({"token":token,"id_usuario":userdb.id, "usuario":userdb.usuario,"id_cuenta_default":userdb.id_cuenta_default,
            "cod_cuenta":cuenta.cod_cuenta,
            "nom_cuenta":cuenta.nom_cuenta
            }) 
        except NoResultFound as e:
            return Response(msg="Usuario no encontrado").from_exception(e)
        except MultipleResultsFound as e:
            return Response(msg="Error con el usuario ".format(usuario)).from_exception(e)
        except Exception as e:
            return Response().from_exception(e)

    def _crear_token(self, usuario=""):
        td = timedelta(minutes=60)
        start = datetime.now(tz=timezone.utc)
        exp = start + td
        payload = {
            "usuario":usuario,            
            "exp":exp
        }        
        
        return jwt.encode(payload, AUTH_SECRET_KEY, algorithm="HS256")        

    def validar_token(self, args={}):
        try:
            token = args.get('token')
            if token is None:
                raise AppException(msg="No se ha enviado el token")

            decodificado = jwt.decode(token, AUTH_SECRET_KEY, algorithms=["HS256"])

            #exp_date = datetime.utcfromtimestamp(decodificado.get('exp'))

            #logger.debug(decodificado)
            #logger.debug(exp_date)
            #logger.debug(datetime.now(tz=timezone.utc))

            resp = Response(msg="credenciales correctas")
            #resp.elem()
            return resp
        except Exception as e:
            return Response().from_exception(e)


    def crear_admon_user(self, args=""):
        usuario = "maquco"
        password = "123456"        
        passdb = hashlib.sha224("{0}{1}".format(usuario,password).encode('utf-8')).hexdigest()
        
         
        nombres = "Miguel Angel"
        apellidos = "Quispe Conde"

        usuario_new = UsuarioModel(
            usuario=usuario,
            password=passdb,
            nombres=nombres,
            apellidos=apellidos
        )        
        db.session.add(usuario_new)
        db.session.commit()
        print('creado correcto')




