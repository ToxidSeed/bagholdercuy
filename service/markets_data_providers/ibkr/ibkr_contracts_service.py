from config.extensions import db
from model.ibkr_contract import IbkrContractsModel
from api.ibkr import InteractiveBrokersClient


class IbkrContractsService:
    def load_contracts(self, exchange: str) -> int:
        """
        Coordina el flujo completo de obtención e inserción de contratos de IBKR.
        """
        if not exchange:
            raise ValueError("El parámetro 'exchange' es requerido")

        raw_data = self._fetch_raw_contracts(exchange)
        incoming_conids, contracts_map = self._parse_contracts(raw_data, exchange)

        if not incoming_conids:
            return 0

        existing_conids = self._get_existing_conids(incoming_conids)
        return self._insert_new_contracts(contracts_map, existing_conids)

    def _fetch_raw_contracts(self, exchange: str) -> list:
        """
        Llama a la API de IBKR para obtener los contratos de un exchange y valida el resultado.
        """
        data = InteractiveBrokersClient.all_conids(exchange=exchange)

        # Si el endpoint retorna error o un mensaje inesperado
        if isinstance(data, dict) and ("error" in data or "message" in data):
            error_msg = data.get("error") or data.get("message") or str(data)
            raise ValueError(f"Error de la API de IBKR: {error_msg}")

        if not isinstance(data, list):
            raise ValueError(f"Respuesta inesperada de la API de IBKR: {data}")

        return data

    def _parse_contracts(self, data: list, default_exchange: str) -> tuple:
        """
        Filtra y extrae los conids, símbolos y exchanges válidos de la respuesta de IBKR.
        """
        incoming_conids = []
        contracts_map = {}

        for item in data:
            if not isinstance(item, dict):
                continue
            conid_raw = item.get("conid")
            if conid_raw is None:
                continue
            try:
                conid = int(conid_raw)
            except (ValueError, TypeError):
                continue

            cod_symbol = item.get("ticker") or item.get("symbol")
            if not cod_symbol:
                continue

            item_exchange = item.get("exchange") or default_exchange

            incoming_conids.append(conid)
            contracts_map[conid] = {"cod_symbol": cod_symbol, "exchange": item_exchange}

        return incoming_conids, contracts_map

    def _get_existing_conids(self, conids: list) -> set:
        """
        Consulta la base de datos para determinar qué conids ya existen.
        """
        existing_conids = set()
        chunk_size = 1000
        for i in range(0, len(conids), chunk_size):
            chunk = conids[i : i + chunk_size]
            results = (
                db.session.query(IbkrContractsModel.conid)
                .filter(IbkrContractsModel.conid.in_(chunk))
                .all()
            )
            for r in results:
                existing_conids.add(r[0])
        return existing_conids

    def _insert_new_contracts(self, contracts_map: dict, existing_conids: set) -> int:
        """
        Inserta en la base de datos los contratos no existentes y confirma la transacción.
        """
        inserted_count = 0
        for conid, info in contracts_map.items():
            if conid not in existing_conids:
                new_contract = IbkrContractsModel(
                    conid=conid,
                    cod_symbol=info["cod_symbol"],
                    exchange=info["exchange"],
                )
                db.session.add(new_contract)
                inserted_count += 1

        if inserted_count > 0:
            db.session.commit()

        return inserted_count
