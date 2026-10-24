import logging
from typing import Optional, List, Dict, Any
from config.extensions import db
from model.symbol import SymbolModel
from model.ibkr_contract import IbkrContractsModel
from model.ibkr_contract_map import IbkrContractMapModel
from api.ibkr import InteractiveBrokersClient
from common.AppException import AppException
from schemas.ibkr_contract_map_schema import IbkrContractMapFilterRequest

logger = logging.getLogger(__name__)


class IbkrContractMapService:
    def sync_symbol_mapping(
        self,
        id_symbol: Optional[int] = None,
        cod_symbol: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> dict:
        """
        Sincroniza y mapea el contrato de IBKR para un symbol según el flujo:
        1. Si id_symbol ya está en tb_ibkr_contract_map, retorna la relación existente.
        2. Si no se encuentra en tb_ibkr_contract_map, busca en tb_ibkr_contract por symbol.
           Si existe allí, inserta en tb_ibkr_contract_map y retorna.
        3. Si no existe en tb_ibkr_contract, consulta la API de Interactive Brokers,
           inserta en tb_ibkr_contract y luego inserta en tb_ibkr_contract_map.
        """
        symbol_record = None
        if id_symbol is not None:
            symbol_record = (
                db.session.query(SymbolModel)
                .filter(SymbolModel.id_symbol == id_symbol)
                .first()
            )
            if not symbol_record:
                raise AppException(
                    msg=f"Símbolo con id_symbol {id_symbol} no encontrado."
                )
        elif cod_symbol:
            clean = str(cod_symbol).strip().upper()
            symbol_record = (
                db.session.query(SymbolModel)
                .filter(SymbolModel.symbol == clean)
                .first()
            )
            if not symbol_record:
                raise AppException(
                    msg=f"Símbolo con código '{cod_symbol}' no encontrado en tb_symbol."
                )
        else:
            raise AppException(
                msg="Debe proporcionar al menos 'id_symbol' o 'cod_symbol'."
            )

        id_sym = symbol_record.id_symbol
        clean_symbol = str(symbol_record.symbol).strip().upper()

        # 1. En la lista de symbols, verificar que el id_symbol está en la relación tb_ibkr_contract_map
        mapping = IbkrContractMapModel.get_by_symbol_id(id_sym)
        if mapping:
            contract = (
                db.session.query(IbkrContractsModel)
                .filter(IbkrContractsModel.conid == mapping.conid)
                .first()
            )
            return self._format_response(mapping, contract, clean_symbol)

        # 2. Si el id_symbol no se encuentra, buscar en tb_ibkr_contract por symbol
        contract = (
            db.session.query(IbkrContractsModel)
            .filter(IbkrContractsModel.cod_symbol == clean_symbol)
            .order_by(IbkrContractsModel.fch_hr_registro.desc())
            .first()
        )
        if contract:
            mapping = IbkrContractMapModel.set_mapping(
                conid=contract.conid,
                id_symbol=id_sym,
            )
            db.session.commit()
            return self._format_response(mapping, contract, clean_symbol)

        # 3. Si no se encuentra en tb_ibkr_contract, buscar en la API de Interactive Brokers
        try:
            remote_data = InteractiveBrokersClient.search_contract_by_symbol(
                symbol=clean_symbol
            )
        except AppException:
            raise
        except Exception as e:
            raise AppException(
                msg=f"Error al consultar en Interactive Brokers para '{clean_symbol}': {str(e)}"
            )

        if isinstance(remote_data, dict) and (
            "error" in remote_data or "message" in remote_data
        ):
            err_msg = remote_data.get("error") or remote_data.get("message")
            raise AppException(
                msg=f"Interactive Brokers devolvió un error: {err_msg}"
            )

        if not isinstance(remote_data, list) or len(remote_data) == 0:
            raise AppException(
                msg=f"No se encontró contrato en Interactive Brokers para el symbol '{clean_symbol}'"
            )

        contract_info = self._extract_contract_info(
            remote_data, clean_symbol, exchange
        )
        conid = contract_info["conid"]
        con_exchange = contract_info["exchange"]

        # Insertar o actualizar en tb_ibkr_contract
        existing_by_conid = (
            db.session.query(IbkrContractsModel)
            .filter(IbkrContractsModel.conid == conid)
            .first()
        )
        if existing_by_conid:
            existing_by_conid.cod_symbol = clean_symbol
            existing_by_conid.exchange = con_exchange
            contract = existing_by_conid
        else:
            contract = IbkrContractsModel(
                conid=conid,
                cod_symbol=clean_symbol,
                exchange=con_exchange,
            )
            db.session.add(contract)

        # Insertar en tb_ibkr_contract_map
        mapping = IbkrContractMapModel.set_mapping(
            conid=conid,
            id_symbol=id_sym,
        )
        db.session.commit()
        return self._format_response(mapping, contract, clean_symbol)

    def get_by_id(self, id_ibkr_contract_map: int) -> Optional[dict]:
        mapping = (
            db.session.query(IbkrContractMapModel)
            .filter(
                IbkrContractMapModel.id_ibkr_contract_map == id_ibkr_contract_map
            )
            .first()
        )
        if not mapping:
            return None
        contract = (
            db.session.query(IbkrContractsModel)
            .filter(IbkrContractsModel.conid == mapping.conid)
            .first()
        )
        return self._format_response(mapping, contract)

    def get_by_symbol_id(self, id_symbol: int) -> Optional[dict]:
        mapping = IbkrContractMapModel.get_by_symbol_id(id_symbol)
        if not mapping:
            return None
        contract = (
            db.session.query(IbkrContractsModel)
            .filter(IbkrContractsModel.conid == mapping.conid)
            .first()
        )
        return self._format_response(mapping, contract)

    def get_mappings(self, params: IbkrContractMapFilterRequest) -> List[dict]:
        query = db.session.query(IbkrContractMapModel)
        if params.id_symbol:
            query = query.filter(
                IbkrContractMapModel.id_symbol == params.id_symbol
            )
        if params.id_contrato_opcion:
            query = query.filter(
                IbkrContractMapModel.id_contrato_opcion
                == params.id_contrato_opcion
            )
        if params.conid:
            query = query.filter(IbkrContractMapModel.conid == params.conid)
        if params.cod_symbol:
            clean = str(params.cod_symbol).strip().upper()
            query = query.join(
                IbkrContractsModel,
                IbkrContractMapModel.conid == IbkrContractsModel.conid,
            ).filter(IbkrContractsModel.cod_symbol == clean)

        page = params.page or 1
        page_size = params.page_size or 50
        records = (
            query.order_by(IbkrContractMapModel.id_ibkr_contract_map.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        results = []
        for rec in records:
            con = (
                db.session.query(IbkrContractsModel)
                .filter(IbkrContractsModel.conid == rec.conid)
                .first()
            )
            results.append(self._format_response(rec, con))
        return results

    def _extract_contract_info(
        self, remote_data: list, cod_symbol: str, preferred_exchange: str = None
    ) -> dict:
        valid_candidates = [
            item
            for item in remote_data
            if isinstance(item, dict) and item.get("conid") is not None
        ]
        if not valid_candidates:
            raise AppException(
                msg=f"No se encontró ningún contrato válido con conid para '{cod_symbol}' en IBKR"
            )

        exact_matches = [
            item
            for item in valid_candidates
            if str(item.get("symbol", "")).strip().upper() == cod_symbol
        ]
        target = exact_matches[0] if exact_matches else valid_candidates[0]

        try:
            conid = int(target["conid"])
        except (ValueError, TypeError):
            raise AppException(
                msg=f"El conid retornado por IBKR para '{cod_symbol}' no es numérico: {target.get('conid')}"
            )

        extracted_exchange = preferred_exchange
        if not extracted_exchange and target.get("exchange"):
            extracted_exchange = target["exchange"]

        if not extracted_exchange and isinstance(target.get("sections"), list):
            for s in target["sections"]:
                if isinstance(s, dict) and s.get("exchange"):
                    extracted_exchange = s["exchange"]
                    break

        if not extracted_exchange:
            extracted_exchange = "SMART"

        return {
            "conid": conid,
            "exchange": extracted_exchange,
            "symbol": target.get("symbol", cod_symbol),
        }

    @staticmethod
    def _format_response(
        mapping: IbkrContractMapModel,
        contract: Optional[IbkrContractsModel] = None,
        cod_symbol: Optional[str] = None,
    ) -> dict:
        return {
            "id_ibkr_contract_map": mapping.id_ibkr_contract_map,
            "id_symbol": mapping.id_symbol,
            "id_contrato_opcion": mapping.id_contrato_opcion,
            "conid": mapping.conid,
            "cod_symbol": contract.cod_symbol if contract else cod_symbol,
            "exchange": contract.exchange if contract else None,
            "fch_registro": (
                mapping.fch_registro.isoformat()
                if mapping.fch_registro
                else None
            ),
            "fch_audit": (
                mapping.fch_audit.isoformat() if mapping.fch_audit else None
            ),
        }
