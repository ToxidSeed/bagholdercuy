from controller.base import Base
from common.AppException import AppException
from common.Response import Response
from parser.comentaroalerta import ComentarioAlertaParser
from reader.comentarioalerta import ComentarioAlertaReader
from manager.comentarioalerta import ComentarioAlertaManager
from app import db


class ComentarioAlertaController(Base):

    def registrar(self, args={}):
        try:
            comentario_alerta = ComentarioAlertaParser().parse_args_registrar(args=args)
            db.session.add(comentario_alerta)
            db.session.commit()
            return Response(msg="Se ha registrado correctamente el comentario")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def get_comentarios_x_alerta(self, args={}):
        parser = ComentarioAlertaParser()
        params = parser.parse_args_get_comentarios_x_alerta(args=args)
        records = ComentarioAlertaReader().get_comentarios_x_alerta(params.id_alerta)
        return Response().from_raw_data(records)

    def eliminar(self, args={}):
        try:
            parser = ComentarioAlertaParser()
            params = parser.parse_args_eliminar(args=args)
            ComentarioAlertaManager().eliminar(params.id_comentario_alerta)
            db.session.commit()
            return Response(msg="Se ha eliminado correctamente")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

