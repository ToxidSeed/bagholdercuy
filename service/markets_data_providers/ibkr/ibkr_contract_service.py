from config.extensions import db
from model.ibkr_contract import IbkrContractsModel
from api.ibkr import InteractiveBrokersClient
from common.AppException import AppException



class IbkrContractService:
    MAX_PAGE_SIZE = 1000

    def get_contracts(
        self,
        conid: int = None,
        cod_symbol: str = None,
        exchange: str = None,
        page: int = 1,
        page_size: int = 100,
    ) -> dict:
        """
        Obtiene los contratos de IBKR almacenados aplicando filtros opcionales y paginación.
        - conid: coincidencia exacta.
        - cod_symbol: coincidencia por prefijo (case-insensitive según collation).
        - exchange: coincidencia exacta.
        """
        if page is None or page < 1:
            raise ValueError("El parámetro 'page' debe ser mayor o igual a 1")
        if page_size is None or page_size < 1 or page_size > self.MAX_PAGE_SIZE:
            raise ValueError(
                f"El parámetro 'page_size' debe estar entre 1 y {self.MAX_PAGE_SIZE}"
            )

        query = db.session.query(IbkrContractsModel)

        if conid is not None:
            query = query.filter(IbkrContractsModel.conid == conid)
        if cod_symbol:
            query = query.filter(IbkrContractsModel.cod_symbol.like(f"{cod_symbol}%"))
        if exchange:
            query = query.filter(IbkrContractsModel.exchange == exchange)

        total = query.count()
        records = (
            query.order_by(IbkrContractsModel.cod_symbol, IbkrContractsModel.conid)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return {
            "items": [self._to_dict(r) for r in records],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    @staticmethod
    def _to_dict(contract: IbkrContractsModel) -> dict:
        return {
            "conid": contract.conid,
            "cod_symbol": contract.cod_symbol,
            "exchange": contract.exchange,
            "fch_hr_registro": (
                contract.fch_hr_registro.isoformat()
                if contract.fch_hr_registro
                else None
            ),
        }

    def sync_contract(self, cod_symbol: str, exchange: str = None) -> dict:
        """
        Sincroniza un contrato para un cod_symbol dado:
        1. Busca en la base de datos local (tb_ibkr_contract).
        2. Si no existe, consulta la API de Interactive Brokers vía search_contract_by_symbol.
        3. Si se encuentra, lo registra en tb_ibkr_contract y confirma la transacción.
        4. Retorna el diccionario del contrato.
        """
        if not cod_symbol or not str(cod_symbol).strip():
            raise AppException(msg="El parámetro 'cod_symbol' es requerido")

        clean_symbol = str(cod_symbol).strip().upper()

        # 1. Buscar en la tabla local
        contract = (
            db.session.query(IbkrContractsModel)
            .filter(IbkrContractsModel.cod_symbol == clean_symbol)
            .order_by(IbkrContractsModel.fch_hr_registro.desc())
            .first()
        )
        if contract is not None:
            return self._to_dict(contract)

        # 2. Consultar en la API de IBKR
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

        if isinstance(remote_data, dict) and ("error" in remote_data or "message" in remote_data):
            err_msg = remote_data.get("error") or remote_data.get("message")
            raise AppException(msg=f"Interactive Brokers devolvió un error: {err_msg}")

        if not isinstance(remote_data, list) or len(remote_data) == 0:
            raise AppException(
                msg=f"No se encontró contrato en Interactive Brokers para el symbol '{clean_symbol}'"
            )

        # 3. Extraer el mejor contrato
        contract_info = self._extract_contract_info(remote_data, clean_symbol, exchange)

        # 4. Insertar o actualizar en tb_ibkr_contract
        conid = contract_info["conid"]
        con_exchange = contract_info["exchange"]

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

        db.session.commit()
        return self._to_dict(contract)

    def _extract_contract_info(
        self, remote_data: list, cod_symbol: str, preferred_exchange: str = None
    ) -> dict:
        """
        Ubica el mejor contrato que coincida con el cod_symbol y extrae conid y exchange.
        """
        valid_candidates = [
            item for item in remote_data
            if isinstance(item, dict) and item.get("conid") is not None
        ]
        if not valid_candidates:
            raise AppException(
                msg=f"No se encontró ningún contrato válido con conid para '{cod_symbol}' en IBKR"
            )

        # Priorizar coincidencia exacta de ticker
        exact_matches = [
            item for item in valid_candidates
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
            "cod_symbol": cod_symbol,
        }

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


    

