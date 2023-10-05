from model.broker import BrokerModel
from common.AppException import AppException

class BrokerParser:        
    def parse_args_get_brokers(args={}):
        nombre = args.get("nombre")
        if nombre in [None,""]:
            args["nombre"] = None
        else:
            args["nombre"] = nombre.strip()
        
        flg_activo = args.get("flg_activo")
        if flg_activo is None:
            args["flg_activo"] = flg_activo
        else:
            args["flg_activo"] = int(flg_activo)        
                
        return args

    def parse_args_registrar(args={}):
        broker = BrokerModel()

        id_broker = args.get("id_broker")
        if id_broker in [None, ""]:
            broker.id_broker == id_broker
        else:
            raise AppException(msg="No se debe enviar un identificador del broker")    

        flg_activo = args.get("flg_activo")    
        if flg_activo in [None, ""]:
            raise AppException(msg="No se ha enviado el indicador de registro activo")

        broker.flg_activo = int(flg_activo)                

        nom_broker = args.get("nom_broker")
        if nom_broker in [None, ""]:
            raise AppException(msg="No se ha enviado el nombre del broker")

        broker.nom_broker = nom_broker

        return broker
    
    def parse_args_actualizar(args={}):
        broker = BrokerModel()

        id_broker = args.get("id_broker")
        if id_broker in [None, ""]:
            raise AppException(msg="No se ha enviado el identificador del broker")        
        else:
            broker.id_broker = int(id_broker)         

        flg_activo = args.get("flg_activo")    
        if flg_activo in [None, ""]:
            raise AppException(msg="No se ha enviado el indicador de registro activo")

        broker.flg_activo = int(flg_activo)    

        nom_broker = args.get("nom_broker")
        if nom_broker in [None, ""]:
            raise AppException(msg="No se ha enviado el nombre del broker")

        broker.nom_broker = nom_broker

        return broker        
        
    def parse_args_get_broker(args={}):
        id_broker = args.get("id_broker")

        if id_broker in [None, ""]:
            args["id_broker"] = None
        else:
            args["id_broker"] = int(id_broker)

        return args
                
        