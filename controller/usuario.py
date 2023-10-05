from controller.base import Base
from processor.usuario import UsuarioProcessor
from reader.usuario import UsuarioReader
from reader.cuenta import CuentaReader
from parser.usuario import UsuarioParser
from common.AppException import AppException
from common.Response import Response
from app import db
from common.Formatter import Formatter

class UsuarioManager(Base):
    def registrar(self, args={}):
        try:
            usuario = UsuarioParser.parse_args_registrar(args=args)           
            UsuarioProcessor().insertar(usuario=usuario)
            db.session.commit()
            return Response(msg="Se ha registrado al usuario correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def actualizar(self, args={}):
        try:
            args = UsuarioParser.parse_args_actualizar(args=args)
            UsuarioProcessor().actualizar(args=args)
            db.session.commit()
            return Response(msg="Se ha actualizado el usuario correctamente")
        except Exception as e:
            return Response().from_exception(e)

    def get_usuarios(self, args={}):
        records = UsuarioReader.get_usuarios()
        nu_records = []

        for elem in records:
            outelem = Formatter().format(elem)
            outelem.pop("password",None)                
            nu_records.append(outelem)
        return Response().from_raw_data(nu_records)

    def get_usuario(self, args={}):
        try:
            args = UsuarioParser.parse_args_get_usuario(args=args)
            usuario = UsuarioReader.get(args.get("id_usuario"))
            cuenta_dict = None
            if usuario.id_cuenta_default is not None:
                cuenta = CuentaReader.get(usuario.id_cuenta_default)
                cuenta_dict = Formatter().format(cuenta)

            usuario_dict = Formatter().format(usuario)
            usuario_dict.pop("password", None)
            usuario_dict["cuenta_default"] = cuenta_dict
            return Response().from_raw_data(usuario_dict)
        except Exception as e:
            return Response().from_exception(e)