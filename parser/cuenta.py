from model.cuenta import CuentaModel
from common.AppException import AppException

class CuentaParser:
    def parse_args_registrar(args={}):
        cuenta = CuentaModel()

        cod_cuenta = args.get("codigo")
        if cod_cuenta in [None, ""]:
            raise AppException(msg="No se ha ingresado el codigo de cuenta")
        
        cuenta.cod_cuenta = cod_cuenta

        nom_cuenta = args.get("nombre")
        if nom_cuenta in [None, ""]:
            raise AppException(msg="No se ha ingresado el nombre de la cuenta")

        cuenta.nom_cuenta = nom_cuenta.strip()
        
        id_usuario = args.get("id_usuario")
        if id_usuario in [None, ""]:
            raise AppException(msg="No se ha ingresado el identificador del usuario")

        cuenta.usuario_id = int(id_usuario)

        id_broker = args.get("id_broker")
        if id_broker in [None, ""]:
            raise AppException(msg="No se ha ingresado el identificador del broker")

        cuenta.id_broker = int(id_broker)

        flg_activo = args.get("flg_activo")
        if flg_activo in [None, ""]:
            raise AppException(msg="No se ha ingresado el indicador de activo/inactivo")

        cuenta.flg_activo = int(flg_activo)

        return cuenta

    def parse_args_actualizar(args={}):
        cuenta = CuentaModel()

        id_cuenta = args.get("id_cuenta")
        if id_cuenta in [None,'']:
            raise AppException(msg="No se ha ingresado el identificador de la cuenta")

        cuenta.id_cuenta = int(id_cuenta)

        cod_cuenta = args.get("cod_cuenta")
        if cod_cuenta in [None, ""]:
            raise AppException(msg="No se ha ingresado el codigo de cuenta")

        cuenta.cod_cuenta = cod_cuenta

        nom_cuenta = args.get("nom_cuenta")
        if nom_cuenta in [None,""]:
            raise AppException(msg="No se ha ingresado el nombre de la cuenta")

        cuenta.nom_cuenta = nom_cuenta

        id_broker = args.get("id_broker")
        if id_broker in [None, ""]:
            raise AppException(msg="No se ha ingresado el identificador del broker")

        cuenta.id_broker = id_broker

        flg_activo = args.get("flg_activo")
        if flg_activo not in [None, ""]:
            raise AppException(msg="No se ha ingresado el indicador de activo/inactivo")

        cuenta.flg_activo = int(flg_activo)

        return cuenta

    def parse_args_get_cuentas(args={}):
        return args

    def parse_args_get_cuentas_x_usuario(args={}):

        id_usuario = args.get("id_usuario")
        if id_usuario in [None, ""]:
            raise AppException(msg="No se ha enviado el usuario")
        
        args["id_usuario"] = id_usuario

        text = args.get("text")
        if text is None:
            raise AppException(msg="No se ha enviado el texto de busqueda")
        
        args["text"] = text

        return args
        

