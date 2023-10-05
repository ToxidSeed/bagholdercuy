from common.AppException import AppException
from model.usuario import UsuarioModel
from parser.base import BaseParser
import hashlib

class UsuarioParser:    
    def parse_args_registrar(args={}):
        id_usuario = args.get("id_usuario")
        if id_usuario not in [None,""]:
            raise AppException(msg="No se debe enviar un identificador de usuario")

        codigo = args.get("codigo")
        if codigo in [None, ""]:
            raise AppException(msg="No se ha enviado el 'codigo'")

        password = args.get("password")
        if password in [None, ""]:
            raise AppException(msg="No se ha enviado el password")

        nombres = args.get("nombres")
        if nombres in [None, ""]:
            raise AppException(msg="No se ha enviado 'Nombres'")

        apellidos = args.get("apellidos")
        if apellidos in [None, ""]:
            raise AppException(msg="No se ha enviado 'Apellidos'")

        id_cuenta_default = args.get("id_cuenta_default")
        if id_cuenta_default in [None, ""]:
            id_cuenta_default = None

        usuario = UsuarioModel()
        usuario.id = None
        usuario.usuario = codigo
        usuario.nombres = nombres
        usuario.apellidos = apellidos
        usuario.moneda_id = "USD"
        usuario.id_cuenta_default = id_cuenta_default
        usuario.password = hashlib.sha224("{0}{1}".format(codigo,password).encode("utf-8")).hexdigest()
    
        return usuario

    def parse_args_actualizar(self, args={}):        

        id_usuario = args.get("id_usuario")
        if id_usuario in [None, ""]:
            raise AppException(msg="No se ha indicado el identificador del usuario")

        args["id_usuario"] = int(id_usuario)

        if "codigo" in args:
            args["codigo"] = args.get("codigo").strip()
        
        if "nombres" in args:
            args["nombres"] = args.get("nombres").strip()

        if "apellidos" in args:
            args["apellidos"] = args.get("apellidos").strip()
        
        if "id_cuenta_default" in args:
            id_cuenta_default = args.get("id_cuenta_default")
            if id_cuenta_default == "":
                args["id_cuenta_default"] = None

        return args

    def parse_args_get_usuario(args={}):
        id_usuario = args.get("id_usuario")
        if id_usuario in [None,""]:
            raise AppException(msg="No se ha enviado el id_usuario")
        
        args["id_usuario"] = int(id_usuario)
        return args