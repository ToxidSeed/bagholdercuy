from app import db
from model.alerta import AlertaModel


class AlertaReader:
    def get_alertas_x_configuracion(self, id_config_alerta):
        query = db.select(
            AlertaModel
        ).where(
            AlertaModel.id_config_alerta == id_config_alerta
        ).order_by(
            AlertaModel.imp_alerta.desc()
        )

        result = db.session.execute(query)
        return result.scalars().all()
