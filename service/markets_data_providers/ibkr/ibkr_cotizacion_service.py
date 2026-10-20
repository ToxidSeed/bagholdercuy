import time
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy import func

from api.ibkr import InteractiveBrokersClient
from model.ibkr_contract import IbkrContractsModel
from service.markets_data_providers.base.quote_provider_base import QuoteProviderBase
from common.AppException import AppException

logger = logging.getLogger(__name__)


class IbkrCotizacionService(QuoteProviderBase):
    name = "ibkr"

    def get_quote(self, cod_symbol: str) -> dict:
        if not cod_symbol:
            raise ValueError("El parámetro 'cod_symbol' es requerido")

        conid = self._resolve_conid(cod_symbol)
        if not conid:
            logger.warning(
                f"No se pudo resolver el conid de IBKR para el símbolo '{cod_symbol}'"
            )
            return self._empty_quote(cod_symbol)

        return self._fetch_snapshot(conid=conid, cod_symbol=cod_symbol)

    def get_quotes(self, items: List[Dict[str, Any]]) -> List[dict]:
        """
        Obtiene cotizaciones en lote optimizando llamadas a IBKR con marketdata_snapshot conids=[...].
        """
        if not items:
            return []

        # 1. Resolver conid para cada item (priorizando tb_ibkr_contract_map)
        item_conids = []
        conid_to_items: Dict[int, List[Dict[str, Any]]] = {}

        # Cargar mapeos en lote desde tb_ibkr_contract_map
        map_by_symbol: Dict[int, int] = {}
        map_by_option: Dict[int, int] = {}
        symbol_ids = [it["id_symbol"] for it in items if it.get("id_symbol")]
        option_ids = [
            it["id_contrato_opcion"]
            for it in items
            if it.get("id_contrato_opcion")
        ]

        if symbol_ids or option_ids:
            try:
                from model.ibkr_contract_map import IbkrContractMapModel
                from sqlalchemy import or_

                clauses = []
                if symbol_ids:
                    clauses.append(IbkrContractMapModel.id_symbol.in_(symbol_ids))
                if option_ids:
                    clauses.append(
                        IbkrContractMapModel.id_contrato_opcion.in_(option_ids)
                    )

                maps = IbkrContractMapModel.query.filter(or_(*clauses)).all()
                for m in maps:
                    if m.id_symbol:
                        map_by_symbol[m.id_symbol] = int(m.conid)
                    if m.id_contrato_opcion:
                        map_by_option[m.id_contrato_opcion] = int(m.conid)
            except Exception as e:
                logger.debug(f"Error al consultar tb_ibkr_contract_map: {e}")

        for it in items:
            cod_sym = it.get("cod_symbol")
            if not cod_sym:
                continue

            id_sym = it.get("id_symbol")
            id_opt = it.get("id_contrato_opcion")

            conid = None
            if id_opt and id_opt in map_by_option:
                conid = map_by_option[id_opt]
            elif id_sym and id_sym in map_by_symbol:
                conid = map_by_symbol[id_sym]

            # Fallback por ticker si no estaba en tb_ibkr_contract_map
            if not conid:
                conid = self._resolve_conid(cod_sym)
                if conid:
                    try:
                        from model.ibkr_contract_map import IbkrContractMapModel
                        from config.extensions import db

                        IbkrContractMapModel.set_mapping(
                            conid=conid,
                            id_symbol=id_sym,
                            id_contrato_opcion=id_opt,
                        )
                        db.session.commit()
                    except Exception as e:
                        logger.debug(f"Error al persistir mapeo dinámico: {e}")

            item_conids.append((it, conid))
            if conid:
                conid_to_items.setdefault(conid, []).append(it)

        unique_conids = list(conid_to_items.keys())
        if not unique_conids:
            return [
                self._empty_quote(
                    cod_symbol=it.get("cod_symbol", ""),
                    id_symbol=it.get("id_symbol"),
                    id_contrato_opcion=it.get("id_contrato_opcion"),
                )
                for it in items
            ]

        # 2. Consultar snapshot batch en IBKR
        fields = [31, 84, 86, 7282, 82, 83]
        snapshot_by_conid: Dict[int, dict] = {}

        try:
            snapshot = InteractiveBrokersClient.marketdata_snapshot(
                conids=unique_conids, fields=fields
            )
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error al consultar batch snapshot en IBKR: {e}", exc_info=True)
            raise AppException(
                msg="No se pudo obtener la cotización desde el proveedor de mercado."
            )

        if isinstance(snapshot, dict) and (
            "error" in snapshot or snapshot.get("statusCode", 200) >= 400
        ):
            logger.error(f"Error devuelto por IBKR marketdata_snapshot: {snapshot}")
            raise AppException(
                msg="No se pudo obtener la cotización desde el proveedor de mercado."
            )

        self._map_snapshots_by_conid(snapshot, snapshot_by_conid)

        # 3. Pre-flight retry para conids que aún no tienen precio
        pending_conids = [
            cid
            for cid in unique_conids
            if cid not in snapshot_by_conid
            or self._extract_price(
                snapshot_by_conid[cid],
                ["31", "lastPrice", "marketPrice", "price", "84", "86"],
            )
            is None
        ]

        if pending_conids:
            time.sleep(0.35)
            try:
                retry_snapshot = InteractiveBrokersClient.marketdata_snapshot(
                    conids=pending_conids, fields=fields
                )
                self._map_snapshots_by_conid(retry_snapshot, snapshot_by_conid)
            except Exception as e:
                logger.warning(f"Error en retry pre-flight batch IBKR: {e}")

        # 4. Construir resultado preservando orden e identificadores
        results = []
        for it, conid in item_conids:
            cod_sym = it.get("cod_symbol", "")
            id_sym = it.get("id_symbol")
            id_opt = it.get("id_contrato_opcion")

            if not conid or conid not in snapshot_by_conid:
                results.append(
                    self._empty_quote(
                        cod_symbol=cod_sym,
                        id_symbol=id_sym,
                        id_contrato_opcion=id_opt,
                    )
                )
                continue

            snap_item = snapshot_by_conid[conid]
            parsed = self._parse_snapshot_prices(snap_item)

            if parsed.get("imp_cierre") is None:
                results.append(
                    self._empty_quote(
                        cod_symbol=cod_sym,
                        id_symbol=id_sym,
                        id_contrato_opcion=id_opt,
                    )
                )
                continue

            results.append(
                {
                    "id_symbol": id_sym,
                    "id_contrato_opcion": id_opt,
                    "cod_symbol": cod_sym,
                    "imp_cierre": parsed["imp_cierre"],
                    "imp_cierre_anterior": parsed["imp_cierre_anterior"],
                    "imp_variacion": parsed["imp_variacion"],
                    "pct_variacion": parsed["pct_variacion"],
                    "provider": self.name,
                }
            )

        return results

    def _resolve_conid(self, cod_symbol: str) -> Optional[int]:
        sym = cod_symbol.strip().upper()

        # 1. Intentar resolver desde la tabla local de contratos de IBKR
        try:
            contract_db = IbkrContractsModel.query.filter(
                func.upper(IbkrContractsModel.cod_symbol) == sym
            ).first()
            if contract_db and contract_db.conid:
                return int(contract_db.conid)
        except Exception as e:
            logger.debug(f"Búsqueda en BD local falló para {cod_symbol}: {e}")

        # 2. Consultar vía search_contract_by_symbol en la API de IBKR
        try:
            contracts = InteractiveBrokersClient.search_contract_by_symbol(symbol=sym)
            if contracts and isinstance(contracts, list):
                for c in contracts:
                    if isinstance(c, dict):
                        c_sym = (c.get("symbol") or c.get("ticker") or "").upper()
                        if c_sym == sym and c.get("conid"):
                            return int(c["conid"])
                # Fallback al primer contrato con conid
                if (
                    contracts
                    and isinstance(contracts[0], dict)
                    and contracts[0].get("conid")
                ):
                    return int(contracts[0]["conid"])
        except Exception as e:
            logger.warning(
                f"Error en search_contract_by_symbol para {cod_symbol}: {e}"
            )

        return None

    def _fetch_snapshot(
        self, conid: int, cod_symbol: str, pre_flight_delay: float = 0.35
    ) -> dict:
        fields = [31, 84, 86, 7282, 82, 83]

        try:
            snapshot = InteractiveBrokersClient.marketdata_snapshot(
                conids=[conid], fields=fields
            )
        except AppException:
            raise
        except Exception as e:
            logger.error(
                f"Error al consultar marketdata_snapshot en IBKR para conid {conid}: {e}",
                exc_info=True,
            )
            raise AppException(
                msg="No se pudo obtener la cotización desde el proveedor de mercado."
            )

        if isinstance(snapshot, dict) and (
            "error" in snapshot or snapshot.get("statusCode", 200) >= 400
        ):
            logger.error(
                f"Error devuelto por IBKR marketdata_snapshot para conid {conid}: {snapshot}"
            )
            raise AppException(
                msg="No se pudo obtener la cotización desde el proveedor de mercado."
            )

        item = self._extract_snapshot_item(snapshot, conid)
        last_price = self._extract_price(
            item, ["31", "lastPrice", "marketPrice", "price", "84", "86"]
        )

        # Pre-flight automático: abrir tick stream si no vino precio inmediato
        if last_price is None and pre_flight_delay > 0:
            time.sleep(pre_flight_delay)
            try:
                retry_snapshot = InteractiveBrokersClient.marketdata_snapshot(
                    conids=[conid], fields=fields
                )
                item = self._extract_snapshot_item(retry_snapshot, conid)
            except Exception as e:
                logger.warning(f"Error en retry pre-flight de snapshot IBKR: {e}")

        parsed = self._parse_snapshot_prices(item)
        if not item or parsed.get("imp_cierre") is None:
            return self._empty_quote(cod_symbol)

        return {
            "cod_symbol": cod_symbol,
            "imp_cierre": parsed["imp_cierre"],
            "imp_cierre_anterior": parsed["imp_cierre_anterior"],
            "imp_variacion": parsed["imp_variacion"],
            "pct_variacion": parsed["pct_variacion"],
            "provider": self.name,
        }

    def _parse_snapshot_prices(self, item: dict) -> dict:
        last_price = self._extract_price(
            item, ["31", "lastPrice", "marketPrice", "price", "84", "86"]
        )
        prev_close = self._extract_price(
            item, ["7282", "priorClose", "previousClose", "prevClose"]
        )
        change = self._extract_price(item, ["82", "change", "netChange"])
        changepct = self._extract_price(item, ["83", "changePct", "pctChange"])

        # Derivaciones consistentes si faltan campos
        if prev_close is None and last_price is not None and change is not None:
            prev_close = round(last_price - change, 4)
        elif change is None and last_price is not None and prev_close is not None:
            change = round(last_price - prev_close, 4)

        if (
            changepct is None
            and change is not None
            and prev_close
            and prev_close > 0
        ):
            changepct = round((change / prev_close) * 100, 4)

        return {
            "imp_cierre": last_price,
            "imp_cierre_anterior": prev_close,
            "imp_variacion": change,
            "pct_variacion": changepct,
        }

    @staticmethod
    def _map_snapshots_by_conid(snapshot, out_map: Dict[int, dict]):
        if isinstance(snapshot, list):
            for it in snapshot:
                if isinstance(it, dict) and it.get("conid") is not None:
                    try:
                        cid = int(it["conid"])
                        out_map[cid] = it
                    except (ValueError, TypeError):
                        continue
        elif isinstance(snapshot, dict) and snapshot.get("conid") is not None:
            try:
                cid = int(snapshot["conid"])
                out_map[cid] = snapshot
            except (ValueError, TypeError):
                pass

    @staticmethod
    def _extract_snapshot_item(snapshot, conid: int) -> dict:
        if isinstance(snapshot, list):
            for it in snapshot:
                if isinstance(it, dict) and it.get("conid") == conid:
                    return it
            if len(snapshot) > 0 and isinstance(snapshot[0], dict):
                return snapshot[0]
        elif isinstance(snapshot, dict):
            return snapshot
        return {}

    @staticmethod
    def _extract_price(item: dict, field_keys: list) -> Optional[float]:
        if not item or not isinstance(item, dict):
            return None
        for key in field_keys:
            val = item.get(key)
            if val is not None:
                try:
                    clean = str(val).lstrip("C").strip().replace("%", "")
                    return float(clean)
                except (ValueError, TypeError):
                    continue
        return None
