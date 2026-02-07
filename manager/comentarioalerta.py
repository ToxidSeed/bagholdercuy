from app import db
from reader.comentarioalerta import ComentarioAlertaReader
from common.AppException import AppException


class ComentarioAlertaManager:
    def eliminar(self, id_comentario_alerta):
        reader = ComentarioAlertaReader()
        comentario_alerta = reader.get(id_comentario_alerta=id_comentario_alerta)
        if comentario_alerta is None:
            raise AppException(msg=f"No se encuentra el comentario con id {id_comentario_alerta}")

        db.session.delete(comentario_alerta)