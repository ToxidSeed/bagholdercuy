from model.symbol import SymbolModel
from model.ibkr_contract import IbkrContractsModel
from model.ibkr_contract_map import IbkrContractMapModel
from common.AppException import AppException

from config.extensions import db
from flask import current_app
from sqlalchemy import func


class SymbolReader:
    def __init__(self, buffer=False):
        self.__buffer = buffer
        self.__memoria = {}

    def get(self, cod_symbol=None, id_symbol=None, not_found_error=False) -> SymbolModel:

        if cod_symbol is None and id_symbol is None:
            raise AppException(msg="No se ha indicado el codigo o el id del symbol")

        if cod_symbol is not None:
            return self.__get_x_cod_symbol(cod_symbol=cod_symbol, not_found_error=not_found_error)

        if id_symbol is not None:
            return self.__get_x_id(id_symbol=id_symbol)

        return None

    def __get_x_cod_symbol(self, cod_symbol, not_found_error=False):
        if self.__buffer is True:
            symbol = self.__memoria.get(cod_symbol)
            if symbol is not None:
                return symbol

        query = db.select(
            SymbolModel
        ).where(
            SymbolModel.symbol == cod_symbol
        )

        result = db.session.execute(query)
        record = result.scalars().first()

        if record is None and not_found_error is True:
            raise AppException(msg=f"No se ha encontrado symbol para {cod_symbol}")

        if record is not None and self.__buffer is True:
            self.__memoria[cod_symbol] = record

        return record

    def __get_x_id(self, id_symbol):
        query = db.select(SymbolModel).where(SymbolModel.id_symbol == id_symbol)

        result = db.session.execute(query)
        record = result.scalars().first()
        return record

    @staticmethod
    def get_list(args=None):
        if args is None:
            args = {}
        id_symbol = args.get("id_symbol")
        cod_symbol = args.get("cod_symbol")
        name = args.get("name")

        stmt = (
            db.select(
                SymbolModel.id_symbol,
                SymbolModel.symbol,
                SymbolModel.name,
                SymbolModel.region,
                SymbolModel.exchange,
                SymbolModel.asset_type,
                SymbolModel.fec_registro,
                SymbolModel.fec_audit,
                SymbolModel.moneda_id,
                SymbolModel.id_symbol_type,
                IbkrContractMapModel.conid,
                IbkrContractsModel.exchange.label("ibkr_exchange"),
            )
            .outerjoin(
                IbkrContractMapModel,
                SymbolModel.id_symbol == IbkrContractMapModel.id_symbol,
            )
            .outerjoin(
                IbkrContractsModel,
                IbkrContractMapModel.conid == IbkrContractsModel.conid,
            )
        )

        if id_symbol is not None:
            stmt = stmt.where(SymbolModel.id_symbol == id_symbol)

        if cod_symbol is not None and str(cod_symbol).strip() != "":
            stmt = stmt.where(
                SymbolModel.symbol.ilike(f"%{str(cod_symbol).strip()}%")
            )

        if name is not None and str(name).strip() != "":
            stmt = stmt.where(
                SymbolModel.name.ilike(f"%{str(name).strip()}%")
            )

        stmt = stmt.order_by(
            SymbolModel.symbol.asc()
        )

        stmt = stmt.limit(current_app.config.get("DEFAULT_LIMIT"))

        results = db.session.execute(stmt)
        return results.all()

