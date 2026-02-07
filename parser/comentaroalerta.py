from parser.base import BaseParser
from model.comentarioalerta import ComentarioAlertaModel
from datetime import date, datetime
from collections import namedtuple


class ComentarioAlertaParser:

    def parse_args_registrar(self, args={}):
        parser = BaseParser(args=args)

        comentario_alerta_model = ComentarioAlertaModel()
        comentario_alerta_model.id_alerta = parser.get("id_alerta", requerido=True, datatype=int)
        comentario_alerta_model.dsc_comentario = parser.get("dsc_comentario", requerido=True)
        comentario_alerta_model.fch_registro = date.today()
        comentario_alerta_model.fch_actualizacion = datetime.now()

        return comentario_alerta_model

    def parse_args_get_comentarios_x_alerta(self, args={}):
        parser = BaseParser(args=args)

        params = namedtuple("params", "id_alerta")
        return params(
            id_alerta=parser.get("id_alerta")
        )

    def parse_args_eliminar(self, args=None):
        args = {} if args is None else args
        parser = BaseParser(args=args)

        params = namedtuple("params", "id_comentario_alerta")
        return params(
            id_comentario_alerta=parser.get("id_comentario_alerta", requerido=True, datatype=int)
        )
