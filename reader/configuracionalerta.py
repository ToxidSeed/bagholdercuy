from app import db
from model.configuracionalerta import ConfiguracionAlertaModel


class ConfiguracionAlertaReader:
    def get(self, id_config_alerta) -> ConfiguracionAlertaModel:
        query = db.select(
            ConfiguracionAlertaModel
        ).where(
            ConfiguracionAlertaModel.id_config_alerta == id_config_alerta
        )

        result = db.session.execute(query)
        return result.scalars().first()

    def get_key1(self, id_monitoreo):
        query = db.select(
            ConfiguracionAlertaModel
        ).where(
            ConfiguracionAlertaModel.id_monitoreo == id_monitoreo
        )

        result = db.session.execute(query)
        return result.scalars().first()

    def get_key2(self, id_cuenta, id_symbol):
        query = db.select(
            ConfiguracionAlertaModel
        ).where(
            ConfiguracionAlertaModel.id_cuenta == id_cuenta,
            ConfiguracionAlertaModel.id_symbol == id_symbol
        )

        result = db.session.execute(query)
        return result.scalars().first()
