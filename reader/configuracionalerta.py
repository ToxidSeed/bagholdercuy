from app import db
from model.configuracionalerta import ConfiguracionAlertaModel

class ConfiguracionAlertaReader:
    def get_key1(self, id_monitoreo):
        query = db.select(
            ConfiguracionAlertaModel
        ).where(
            ConfiguracionAlertaModel.id_monitoreo == id_monitoreo
        )

        result = db.session.execute(query)
        return result.scalars().first()