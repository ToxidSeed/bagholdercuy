from app import db
from model.comentarioalerta import ComentarioAlertaModel


class ComentarioAlertaReader:

    def get(self, id_comentario_alerta):
        query = db.select(
            ComentarioAlertaModel
        ).where(
            ComentarioAlertaModel.id_comentario_alerta == id_comentario_alerta
        )
        result = db.session.execute(query)
        return result.scalars().first()

    def get_comentarios_x_alerta(self, id_alerta):
        query = db.select(
            ComentarioAlertaModel
        ).where(
            ComentarioAlertaModel.id_alerta == id_alerta
        )

        result = db.session.execute(query)
        return result.scalars().all()