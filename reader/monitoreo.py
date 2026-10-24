from config.extensions import db
from model.monitoreo import MonitoreoModel
from model.symbol import SymbolModel
from model.contrato_opcion import ContratoOpcionModel
from model.configuracionalerta import ConfiguracionAlertaModel
from common.AppException import AppException
from sqlalchemy import func


class MonitoreoReader:
    def get(self, id_monitoreo):
        query = db.select(MonitoreoModel).where(
            MonitoreoModel.id_monitoreo == id_monitoreo
        )

        result = db.session.execute(query)
        return result.scalars().first()

    def get_by_symbol(self, id_symbol, id_cuenta, error_si_no_existe=False):
        query = db.select(MonitoreoModel).where(
            MonitoreoModel.id_symbol == id_symbol,
            MonitoreoModel.id_cuenta == id_cuenta,
        )

        result = db.session.execute(query)
        record = result.scalars().first()
        if record is None and error_si_no_existe is True:
            raise AppException(
                msg=f"No existe el monitoreo para el id symbol {id_symbol} y el id cuenta {id_cuenta}"
            )

        return record

    def get_by_option(self, id_contrato_opcion, id_cuenta, error_si_no_existe=False):
        query = db.select(MonitoreoModel).where(
            MonitoreoModel.id_contrato_opcion == id_contrato_opcion,
            MonitoreoModel.id_cuenta == id_cuenta,
        )

        result = db.session.execute(query)
        record = result.scalars().first()
        if record is None and error_si_no_existe is True:
            raise AppException(
                msg=f"No existe el monitoreo para el contrato de opcion {id_contrato_opcion} y el id cuenta {id_cuenta}"
            )

        return record

    def get_key1(self, id_symbol, id_cuenta, error_si_no_existe=False):
        return self.get_by_symbol(
            id_symbol=id_symbol,
            id_cuenta=id_cuenta,
            error_si_no_existe=error_si_no_existe,
        )

    def get_monitoreo_activo(self, id_cuenta, opcionales={}):
        query = (
            db.select(
                MonitoreoModel.id_monitoreo,
                MonitoreoModel.id_symbol_type,
                MonitoreoModel.id_symbol,
                MonitoreoModel.id_contrato_opcion,
                MonitoreoModel.id_cuenta,
                MonitoreoModel.fch_registro,
                MonitoreoModel.flg_activo,
                func.coalesce(
                    SymbolModel.symbol, ContratoOpcionModel.cod_symbol
                ).label("cod_symbol"),
                func.coalesce(
                    SymbolModel.name,
                    ContratoOpcionModel.descripcion,
                    ContratoOpcionModel.cod_symbol,
                ).label("nom_symbol"),
                ConfiguracionAlertaModel.id_config_alerta,
            )
            .select_from(MonitoreoModel)
            .outerjoin(
                SymbolModel, MonitoreoModel.id_symbol == SymbolModel.id_symbol
            )
            .outerjoin(
                ContratoOpcionModel,
                MonitoreoModel.id_contrato_opcion
                == ContratoOpcionModel.id_contrato_opcion,
            )
            .outerjoin(
                ConfiguracionAlertaModel,
                MonitoreoModel.id_monitoreo == ConfiguracionAlertaModel.id_monitoreo,
            )
            .where(
                MonitoreoModel.id_cuenta == id_cuenta,
                MonitoreoModel.flg_activo == opcionales.get("flg_activo", 1),
            )
        )

        if "id_symbol" in opcionales and opcionales.get("id_symbol") is not None:
            query = query.where(MonitoreoModel.id_symbol == opcionales.get("id_symbol"))

        if (
            "id_contrato_opcion" in opcionales
            and opcionales.get("id_contrato_opcion") is not None
        ):
            query = query.where(
                MonitoreoModel.id_contrato_opcion == opcionales.get("id_contrato_opcion")
            )

        if (
            "id_symbol_type" in opcionales
            and opcionales.get("id_symbol_type") is not None
        ):
            query = query.where(
                MonitoreoModel.id_symbol_type == opcionales.get("id_symbol_type")
            )

        result = db.session.execute(query)
        records = result.all()
        return records



