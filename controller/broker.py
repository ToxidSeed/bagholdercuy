from reader.broker import BrokerReader
from controller.base import Base
from common.Response import Response
from parser.broker import BrokerParser
from processor.broker import BrokerProcessor
from app import db

class BrokerManager(Base):

    def get_brokers(self, args={}):
        try:
            args = BrokerParser.parse_args_get_brokers(args=args)
            records = BrokerReader.get_brokers(args=args)
            return Response().from_raw_data(records)
        except Exception as e:
            return Response().from_exception(e)

    def get_brokers_activos(self, args={}):
        try:
            records = BrokerReader.get_brokers_activos()
            return Response.from_raw_data(records)
        except Exception as e:
            return Response().from_exception(e)

    def get_broker(self, args={}):
        try:
            args = BrokerParser.parse_args_get_broker(args=args)
            record = BrokerReader.get(args.get("id_broker"))
            return Response().from_raw_data(record)
        except Exception as e:
            return Response().from_exception(e)        

    def registrar(self, args={}):
        try:
            broker = BrokerParser.parse_args_registrar(args=args)
            BrokerProcessor().guardar(broker=broker)            
            db.session.commit()
            return Response(msg="El broker se ha registrado correctamente")            
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)    

    def actualizar(self, args={}):
        try:
            broker = BrokerParser.parse_args_actualizar(args=args)
            BrokerProcessor().guardar(broker=broker)            
            db.session.commit()
            return Response(msg="El broker se ha actualizado correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)
    



