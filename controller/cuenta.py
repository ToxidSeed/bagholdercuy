from processor.cuenta import CuentaProcessor
from parser.cuenta import CuentaParser
from reader.cuenta import CuentaReader
from controller.base import Base
from common.Response import Response
from app import db

class CuentaManager(Base):
    def registrar(self, args={}):
        try:
            cuenta = CuentaParser.parse_args_registrar(args=args)
            CuentaProcessor().guardar(cuenta=cuenta)
            db.session.commit()
            return Response(msg="Se ha registrado correctamente la cuenta")
        except Exception as e:
            db.session.rollback()            
            return Response().from_exception(e)

    def actualizar(self, args={}):
        try:
            cuenta = CuentaParser.parse_args_actualizar(args=args)
            CuentaProcessor().guardar(cuenta=cuenta)
            db.session.commit()
        except Exception as e:
            return Response().from_exception(e)

    def get_cuentas(self, args={}):
        try:
            args = CuentaParser.parse_args_get_cuentas(args=args)
            records = CuentaReader.get_cuentas(args=args)
            return Response().from_raw_data(records) 
        except Exception as e:
            return Response().from_exception(e)

    def get_cuentas_x_usuario(self, args={}):
        try:
            args = CuentaParser.parse_args_get_cuentas_x_usuario(args=args)
            records = CuentaReader.get_cuentas(args=args)
            return Response().from_raw_data(records) 
        except Exception as e:
            return Response().from_exception(e)
        
        

    