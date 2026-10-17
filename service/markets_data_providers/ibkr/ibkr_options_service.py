import re
import time
import logging
from datetime import datetime, date
from cachetools import cached, TTLCache
from api.ibkr import InteractiveBrokersClient
from model.ibkr_contract import IbkrContractsModel

logger = logging.getLogger(__name__)

MONTH_MAP = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MAY",
    6: "JUN",
    7: "JUL",
    8: "AUG",
    9: "SEP",
    10: "OCT",
    11: "NOV",
    12: "DEC",
}

expiration_cache = TTLCache(maxsize=1000, ttl=86400)
strikes_cache = TTLCache(maxsize=1000, ttl=86400)
options_cache = TTLCache(maxsize=1000, ttl=86400)


def _expiration_cache_key(self, cod_symbol=None):
    if cod_symbol:
        return str(cod_symbol).strip().upper()
    return ""

def _strikes_cache_key(self, cod_subyacente=None, expiracion=None, exchange=None):
    if cod_subyacente and expiracion:
        return f"{str(cod_subyacente).strip().upper()}_{str(expiracion).strip().upper()}_{str(exchange).strip().upper() if exchange else 'SMART'}"
    return ""


def _options_cache_key(self, conid=None, month=None, strike=None):
    if conid and month and strike:
        return f"{str(conid).strip().upper()}_{str(month).strip().upper()}_{str(strike).strip().upper()}"
    return ""


class IbkrOptionsService:
    @cached(expiration_cache, key=_expiration_cache_key)
    def get_expiration_months(self, cod_symbol: str) -> list:
        """
        Obtiene los meses de expiración para un símbolo desde IBKR.
        args:
            cod_symbol (str): codigo del contrato a consultar en ibkr
        scenarios:
            1.- Buscar en la api api/ibkr.py - InteractiveBrokersClient.search_contract_by_symbol
            2.- filtrar los resultados dentro de la lista de sections por secType = "OPT" y devolver el elemento months en un array.            
        """
        if not cod_symbol or not str(cod_symbol).strip():
            raise ValueError("El parámetro 'cod_symbol' es requerido")

        cod_symbol = str(cod_symbol).strip()
        data = InteractiveBrokersClient.search_contract_by_symbol(symbol=cod_symbol)

        if isinstance(data, dict) and ("error" in data or "message" in data):
            error_msg = data.get("error") or data.get("message") or str(data)
            raise ValueError(f"Error de la API de IBKR: {error_msg}")

        if not isinstance(data, list):
            raise ValueError(f"Respuesta inesperada de la API de IBKR: {data}")

        expiration_months = []
        for item in data:
            if not isinstance(item, dict):
                continue

            # Dentro de la lista de sections
            sections = item.get("sections")
            if isinstance(sections, list):
                for section in sections:
                    if (
                        isinstance(section, dict)
                        and str(section.get("secType", "")).upper() == "OPT"
                    ):
                        months = section.get("months")
                        self._append_months(expiration_months, months)

        return expiration_months

    def get_expiration_dates(self, cod_symbol: str) -> list:
        """
        Método de compatibilidad hacia atrás. Delegar en get_expiration_months.
        """
        return self.get_expiration_months(cod_symbol=cod_symbol)

    def _append_months(self, target_list: list, months) -> None:
        """
        Agrega elementos de 'months' al target_list parseando strings delimitados por ';' o ','
        o listas, evitando duplicados y preservando el orden.
        """
        if not months:
            return

        if isinstance(months, str):
            items = months.replace(",", ";").split(";")
            for m in items:
                m_clean = m.strip()
                if m_clean and m_clean not in target_list:
                    target_list.append(m_clean)
        elif isinstance(months, (list, tuple)):
            for m in months:
                m_clean = str(m).strip()
                if m_clean and m_clean not in target_list:
                    target_list.append(m_clean)

    @cached(strikes_cache, key=_strikes_cache_key)
    def get_strikes(
        self, cod_subyacente: str, expiracion: str, exchange: str = None
    ) -> dict:
        """
        Function que retorna strikes desde la API de interactive brokers
        args:
            cod_subyacente (str): codigo del contrato subyacente a consultar en ibkr
            expiracion (str): mes de expiración del contrato, tiene por ejemplo el formato JAN25
            exchange (str, opcional): exchange a consultar, por defecto None (IBKR usa SMART)
        scenarios:
            1.- Buscar en la tabla IbkrContractsModel por coincidencia exacta del símbolo.
            2.- Si encuentra el contrato, obtener el conid del contrato.
            3.- con el conid del contrato consultar api/ibkr.py InteractiveBrokersClient.secdef_strikes
            4.- devolver los strikes
        """
        if not cod_subyacente or not str(cod_subyacente).strip():
            raise ValueError("El parámetro 'cod_subyacente' es requerido")

        if not expiracion or not str(expiracion).strip():
            raise ValueError("El parámetro 'expiracion' es requerido")

        cod_subyacente = str(cod_subyacente).strip()
        expiracion = str(expiracion).strip()

        contract = IbkrContractsModel.find_by_symbol(cod_symbol=cod_subyacente)
        if not contract:
            raise ValueError(
                f"No se encontró el contrato para el símbolo '{cod_subyacente}'"
            )

        conid = contract.conid
        strikes = InteractiveBrokersClient.secdef_strikes(
            conid=conid,
            month=expiracion,
            sec_type="OPT",
            exchange=exchange,
        )

        if isinstance(strikes, dict) and ("error" in strikes or "message" in strikes):
            error_msg = strikes.get("error") or strikes.get("message") or str(strikes)
            raise ValueError(f"Error de la API de IBKR: {error_msg}")

        return strikes

    def _parse_expiration_month(self, fch_expiracion) -> str:
        """
        Parsea y normaliza fch_expiracion a formato MESAÑO de IBKR (ej. JAN25).
        Acepta objetos date/datetime, strings en formatos YYYY-MM-DD, DD/MM/YYYY, etc., o directamente JAN25.
        """
        if isinstance(fch_expiracion, (datetime, date)):
            return f"{MONTH_MAP[fch_expiracion.month]}{fch_expiracion.strftime('%y')}"

        if isinstance(fch_expiracion, str):
            clean = fch_expiracion.strip().upper()
            if re.match(r"^[A-Z]{3}\d{2}$", clean):
                return clean

            for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    dt = datetime.strptime(clean, fmt)
                    return f"{MONTH_MAP[dt.month]}{dt.strftime('%y')}"
                except ValueError:
                    pass

        raise ValueError(
            f"Formato de fecha de expiración inválido: '{fch_expiracion}'"
        )

    def _parse_date(self, fch) -> date:
        """
        Parsea fch a un objeto date. Acepta objetos date/datetime, strings en formatos
        YYYY-MM-DD, YYYYMMDD, DD/MM/YYYY, etc., o formato MESAÑO (ej. JAN25 -> primer día del mes).
        """
        if isinstance(fch, datetime):
            return fch.date()
        if isinstance(fch, date):
            return fch

        if isinstance(fch, str):
            clean = fch.strip()
            digits = "".join(c for c in clean if c.isdigit())
            if len(digits) == 8:
                try:
                    return datetime.strptime(digits, "%Y%m%d").date()
                except ValueError:
                    pass

            for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(clean, fmt).date()
                except ValueError:
                    pass

            clean_upper = clean.upper()
            if re.match(r"^[A-Z]{3}\d{2}$", clean_upper):
                month_abbr = clean_upper[:3]
                year_num = int("20" + clean_upper[3:])
                inv_month = {v: k for k, v in MONTH_MAP.items()}
                m_num = inv_month.get(month_abbr, 1)
                return date(year_num, m_num, 1)

        raise ValueError(f"Formato de fecha de expiración inválido: '{fch}'")

    def _select_strikes_around_underlying(
        self, strikes: list, imp_underlying: float, num_strikes: int = 50
    ) -> list:
        """
        Selecciona los N strikes más cercanos al precio del subyacente (num_strikes // 2 por arriba y por abajo).
        Si un lado tiene menos strikes disponibles, compensa con el otro lado.
        """
        sorted_strikes = sorted(list(set(float(s) for s in strikes))) if strikes else []

        if num_strikes == 0:
            return sorted_strikes

        if num_strikes is None or num_strikes < 0:
            num_strikes = 50

        if len(sorted_strikes) <= num_strikes:
            return sorted_strikes

        half = num_strikes // 2
        strikes_below = [s for s in sorted_strikes if s <= imp_underlying]
        strikes_above = [s for s in sorted_strikes if s > imp_underlying]

        selected_below = strikes_below[-half:] if len(strikes_below) > half else strikes_below
        selected_above = strikes_above[:half] if len(strikes_above) > half else strikes_above

        remaining = num_strikes - (len(selected_below) + len(selected_above))
        if remaining > 0:
            if len(strikes_below) < half:
                extra_above = [s for s in strikes_above if s not in selected_above][:remaining]
                selected_above.extend(extra_above)
            elif len(strikes_above) < half:
                extra_below = [s for s in strikes_below if s not in selected_below][-remaining:]
                selected_below = extra_below + selected_below

        return sorted(list(set(selected_below + selected_above)))

    def _fetch_contracts_by_expiration(
        self, conid: int, month: str, strikes: list, fch_expiracion_fallback: str = None
    ) -> dict:
        """
        Consulta contratos para cada strike con _get_contracts, enriquece los datos y los agrupa
        por su fecha real de expiración (maturityDate).
        """
        contracts_by_expiration = {}
        if not conid or not month:
            return contracts_by_expiration

        for strike in strikes:
            strike_val = int(strike) if strike.is_integer() else strike
            contracts = self._get_contracts(conid=conid, month=month, strike=strike_val)
            for contract in contracts:
                if not isinstance(contract, dict):
                    continue

                enriched = dict(contract)
                if "cod_symbol" not in enriched:
                    enriched["cod_symbol"] = enriched.get("symbol") or enriched.get("ticker")
                if "imp_strike" not in enriched:
                    try:
                        enriched["imp_strike"] = float(enriched.get("strike", strike))
                    except (ValueError, TypeError):
                        enriched["imp_strike"] = strike

                raw_date = (
                    contract.get("maturityDate")
                    or contract.get("expirationDate")
                    or contract.get("fch_vencimiento")
                )
                contract_date = None
                if raw_date:
                    try:
                        contract_date = self._parse_date(raw_date)
                    except (ValueError, TypeError):
                        contract_date = None

                if "fch_vencimiento" not in enriched:
                    if contract.get("maturityDate"):
                        enriched["fch_vencimiento"] = str(contract.get("maturityDate"))
                    elif contract_date:
                        enriched["fch_vencimiento"] = contract_date.strftime("%Y%m%d")
                    else:
                        enriched["fch_vencimiento"] = str(fch_expiracion_fallback)

                enriched.setdefault("bid", None)
                enriched.setdefault("ask", None)
                enriched.setdefault("last", None)

                if contract_date:
                    contracts_by_expiration.setdefault(contract_date, []).append(enriched)
                else:
                    contracts_by_expiration.setdefault(None, []).append(enriched)

        return contracts_by_expiration

    def _resolve_target_expiration_date(
        self, available_dates: list, target_date: date
    ) -> date:
        """
        Verifica si target_date se encuentra en available_dates.
        Si no se encuentra, retorna la fecha más próxima (priorizando fechas futuras en empate).
        """
        if not available_dates:
            return target_date

        if target_date in available_dates:
            return target_date

        return min(
            available_dates,
            key=lambda d: (abs((d - target_date).days), 0 if d >= target_date else 1),
        )

    def _classify_calls_and_puts(self, contracts: list) -> tuple:
        """
        Clasifica una lista de contratos en dos listas: calls y puts según su derecho (right).
        """
        calls = []
        puts = []
        for contract in contracts:
            right = str(contract.get("right", "")).upper()
            if right in ("C", "CALL"):
                calls.append(contract)
            elif right in ("P", "PUT"):
                puts.append(contract)
            else:
                calls.append(contract)
        return calls, puts

    def _build_options_chain(
        self,
        imp_underlying: float,
        strikes: list,
        num_strikes: int = 50,
        conid: int = None,
        month: str = None,
        fch_expiracion: str = None,
    ) -> dict:
        """
        Function que construye el option chain desde la API de interactive brokers, cuyos strikes estan cerca al precio del subyacente.
        args:
            imp_underlying (float): precio del subyacente
            strikes (list): lista de strikes
            num_strikes (int, opcional): cantidad de strikes a consultar, por defecto 50
            conid (int, opcional): conid del contrato subyacente
            month (str, opcional): mes de expiración en formato MESAÑO (ej. JAN25)
            fch_expiracion (str): fecha de expiración deseada (YYYY-MM-DD), no puede ser None
        scenarios:
            1.- fch_expiracion no puede ser None, para performance y no escanear todo.
            2.- Por cada month y strike se consulta _get_contracts y se va acumulando, agrupando por la fch_expiracion real del contrato.
            3.- Una vez se tengan realmente los contratos validos verificar si fch_expiracion (parametro) se encuentra en esas fechas. Si es el caso entonces filtrar.
            4.- Si fch_expiracion no se encuentra en los contratos acumulados entonces filtrar por la fecha mas proxima.
            5.- Devolver el resultado con las listas de calls, puts, strikes y precio del subyacente.
        """
        # 1. fch_expiracion no puede ser None, para performance y no escanear todo.
        if not fch_expiracion or not str(fch_expiracion).strip():
            raise ValueError("El parámetro 'fch_expiracion' es requerido")

        target_date = self._parse_date(fch_expiracion)

        # Selección de strikes cercanos al subyacente
        selected_strikes = self._select_strikes_around_underlying(
            strikes=strikes, imp_underlying=imp_underlying, num_strikes=num_strikes
        )

        # 2. Por cada month y strike se consulta _get_contracts y se va acumulando por fecha real
        contracts_by_expiration = self._fetch_contracts_by_expiration(
            conid=conid,
            month=month,
            strikes=selected_strikes,
            fch_expiracion_fallback=fch_expiracion,
        )

        # Fechas de vencimiento obtenidas antes de filtrar
        available_dates = [d for d in contracts_by_expiration.keys() if isinstance(d, date)]
        fechas_vencimiento = sorted([d.strftime("%Y-%m-%d") for d in available_dates])

        # 3 y 4. Filtrar por fch_expiracion o por la fecha más próxima
        if available_dates:
            selected_date = self._resolve_target_expiration_date(available_dates, target_date)
            selected_contracts = contracts_by_expiration[selected_date]
        else:
            selected_date = target_date
            selected_contracts = contracts_by_expiration.get(None, [])

        calls, puts = self._classify_calls_and_puts(selected_contracts)

        real_fch_vencimiento = (
            selected_date.strftime("%Y-%m-%d")
            if isinstance(selected_date, date)
            else str(selected_date)
        )

        # 5. Devolver el resultado
        return {
            "calls": calls,
            "puts": puts,
            "strikes": selected_strikes,
            "imp_underlying": imp_underlying,
            "fch_vencimiento": real_fch_vencimiento,
            "fechas_vencimiento": fechas_vencimiento,
            "exp_dates": fechas_vencimiento,
        }

    @cached(options_cache, key=_options_cache_key)
    def _get_contracts(self, conid: int, month: str, strike: int):
        """
        args:
            conid (int): conid del contrato
            month (str): mes de expiracion de IBKR
            strike (int): strike del contrato            
        precondiciones:
            - el sec_type es OPT            
        scenarios:
            1.- con el conid, month y strike buscar en api/ibkr.py - InteractiveBrokersClient.secdef_info
            2.- devolver las coincidencias
        """
        if not conid:
            raise ValueError("El parámetro 'conid' es requerido")
        if not month or not str(month).strip():
            raise ValueError("El parámetro 'month' es requerido")
        if strike is None:
            raise ValueError("El parámetro 'strike' es requerido")

        data = InteractiveBrokersClient.secdef_info(
            conid=conid,
            month=str(month).strip(),
            strike=strike,
            sec_type="OPT",
        )

        if isinstance(data, dict) and ("error" in data or "message" in data):
            error_msg = data.get("error") or data.get("message") or str(data)
            raise ValueError(f"Error de la API de IBKR: {error_msg}")

        if not isinstance(data, list):
            return []

        return data

    def get_underlying_price(self, conid: int, cod_subyacente: str = None) -> float:
        """
        Obtiene el precio del subyacente a partir de su conid consultando InteractiveBrokersClient.marketdata_snapshot.
        args:
            conid (int): conid del contrato subyacente
            cod_subyacente (str, opcional): código del subyacente para enriquecer el mensaje de error
        """
    def _extract_price_from_snapshot(self, snapshot, conid):
        snap_item = None
        if isinstance(snapshot, list) and len(snapshot) > 0:
            for item in snapshot:
                if isinstance(item, dict) and (
                    item.get("conid") == conid or str(item.get("conid")) == str(conid)
                ):
                    snap_item = item
                    break
            if not snap_item and isinstance(snapshot[0], dict):
                snap_item = snapshot[0]
        elif isinstance(snapshot, dict):
            snap_item = snapshot

        imp_underlying = None
        if snap_item and isinstance(snap_item, dict):
            for field in ["31", "lastPrice", "markPrice", "marketPrice", "price", "84", "86"]:
                val = snap_item.get(field)
                if val is not None:
                    try:
                        clean_val = str(val).lstrip("C").strip()
                        imp_underlying = float(clean_val)
                        break
                    except (ValueError, TypeError):
                        continue
        return imp_underlying

    def get_underlying_price(
        self, conid: int, cod_subyacente: str = None, pre_flight_delay: float = 0.35
    ) -> float:
        """
        Obtiene el precio del subyacente a partir de su conid consultando InteractiveBrokersClient.marketdata_snapshot.
        Si en la primera llamada no hay precio (pre-flight requerido por IBKR), espera un breve instante y reintenta.
        args:
            conid (int): conid del contrato subyacente
            cod_subyacente (str, opcional): código del subyacente para enriquecer el mensaje de error
            pre_flight_delay (float): tiempo de espera en segundos si se requiere pre-flight (por defecto 0.35)
        """
        if not conid:
            raise ValueError("El parámetro 'conid' es requerido")

        snapshot = InteractiveBrokersClient.marketdata_snapshot(
            conids=[conid], fields=[31, 84, 86]
        )

        if isinstance(snapshot, dict) and ("error" in snapshot or "message" in snapshot):
            error_msg = snapshot.get("error") or snapshot.get("message") or str(snapshot)
            raise ValueError(f"Error de la API de IBKR: {error_msg}")

        imp_underlying = self._extract_price_from_snapshot(snapshot, conid)

        # Pre-flight automático: si el stream acaba de abrirse y no vino precio inicial
        if imp_underlying is None and pre_flight_delay > 0:
            time.sleep(pre_flight_delay)
            try:
                retry_snapshot = InteractiveBrokersClient.marketdata_snapshot(
                    conids=[conid], fields=[31, 84, 86]
                )
                imp_underlying = self._extract_price_from_snapshot(retry_snapshot, conid)
            except Exception as e:
                logger.warning(
                    f"Error en retry pre-flight de precio subyacente: {e}"
                )

        if imp_underlying is None:
            msg_symbol = f" para el símbolo '{cod_subyacente}'" if cod_subyacente else f" para el conid {conid}"
            raise ValueError(f"No se pudo obtener el precio del subyacente{msg_symbol}")

        return imp_underlying

    _get_underlying_price = get_underlying_price

    def _enrich_options_with_market_data(
        self, calls: list, puts: list, pre_flight_delay: float = 0.35
    ) -> None:
        """
        Consulta api/ibkr.py InteractiveBrokersClient.marketdata_snapshot para obtener
        bid, ask y last de cada contrato en calls y puts, y los agrega directamente
        a los diccionarios de contrato.

        Implementa el patrón pre-flight automático de IBKR IServer:
        1. Petición inicial: abre el stream en vivo en IServer para contratos nuevos
           o recupera datos de streams ya abiertos.
        2. Si existen contratos sin cotización (pre-flight recién emitido), realiza
           una breve espera (pre_flight_delay) para permitir la llegada de los ticks
           y ejecuta una segunda consulta extrayendo los datos del stream ya abierto.
        """
        all_contracts = (calls or []) + (puts or [])
        conids = [
            c.get("conid") for c in all_contracts if c.get("conid") is not None
        ]
        unique_conids = list(dict.fromkeys(conids))
        if not unique_conids:
            for contract in all_contracts:
                contract.setdefault("bid", None)
                contract.setdefault("ask", None)
                contract.setdefault("last", None)
            return

        def _parse_num(val):
            if val is None:
                return None
            try:
                clean = str(val).lstrip("C").strip()
                return float(clean)
            except (ValueError, TypeError):
                return None

        quotes_by_conid = {}

        def _fetch_batches(conid_list):
            batch_size = 50
            for i in range(0, len(conid_list), batch_size):
                batch = conid_list[i : i + batch_size]
                try:
                    snapshot = InteractiveBrokersClient.marketdata_snapshot(
                        conids=batch, fields=[31, 84, 86]
                    )
                except Exception as e:
                    logger.warning(
                        f"No se pudo obtener snapshot de mercado para opciones: {e}"
                    )
                    continue

                items = []
                if isinstance(snapshot, list):
                    items = snapshot
                elif isinstance(snapshot, dict):
                    if "conid" in snapshot:
                        items = [snapshot]
                    else:
                        logger.warning(
                            f"Respuesta inesperada al consultar snapshot de opciones: {snapshot}"
                        )

                for item in items:
                    if not isinstance(item, dict):
                        continue
                    cid = item.get("conid")
                    if cid is None:
                        continue

                    # 84: Bid, 86: Ask, 31: Last
                    bid = _parse_num(
                        item.get("84") if item.get("84") is not None else item.get("bid")
                    )
                    ask = _parse_num(
                        item.get("86") if item.get("86") is not None else item.get("ask")
                    )
                    last = _parse_num(
                        item.get("31")
                        if item.get("31") is not None
                        else (item.get("lastPrice") or item.get("last") or item.get("price"))
                    )

                    existing = quotes_by_conid.get(str(cid))
                    if existing:
                        quotes_by_conid[str(cid)] = {
                            "bid": bid if bid is not None else existing.get("bid"),
                            "ask": ask if ask is not None else existing.get("ask"),
                            "last": last if last is not None else existing.get("last"),
                        }
                    else:
                        quotes_by_conid[str(cid)] = {
                            "bid": bid,
                            "ask": ask,
                            "last": last,
                        }

        # 1. Petición inicial (actúa como pre-flight para nuevos conids)
        _fetch_batches(unique_conids)

        # 2. Detección de contratos que aún no recibieron cotización
        def _has_quote(cid):
            q = quotes_by_conid.get(str(cid))
            if not q:
                return False
            return (
                q.get("bid") is not None
                or q.get("ask") is not None
                or q.get("last") is not None
            )

        missing_conids = [cid for cid in unique_conids if not _has_quote(cid)]

        # 3. Pre-flight retry: si hay contratos pendientes, esperar brevemente y consultar de nuevo
        if missing_conids and pre_flight_delay > 0:
            time.sleep(pre_flight_delay)
            _fetch_batches(missing_conids)

        # 4. Asignar bid, ask, last a cada contrato en calls y puts
        for contract in all_contracts:
            cid_str = str(contract.get("conid"))
            quotes = quotes_by_conid.get(cid_str)
            if quotes:
                contract["bid"] = quotes.get("bid")
                contract["ask"] = quotes.get("ask")
                contract["last"] = quotes.get("last")
            else:
                contract.setdefault("bid", None)
                contract.setdefault("ask", None)
                contract.setdefault("last", None)

    def get_options_chain(
        self,
        cod_subyacente: str,
        fch_expiracion: str = None,
        num_strikes: int = 50,
    ) -> dict:
        """
        Function que retorna option chain desde la API de interactive brokers
        args:
            cod_subyacente (str): codigo del contrato subyacente a consultar en ibkr
            fch_expiracion (str, opcional): fecha de expiración del contrato, formato YYYY-MM-DD
            num_strikes (int, opcional): cantidad de strikes a consultar.
        scenarios:
            1.- Si fch_expiracion es enviado obtenere el mes en formato MESAÑO, ex JAN25, caso contrario fch_expiracion es la fecha del sistema y obtener el mes en formato MESAÑO.            
            2.- Buscar en la tabla IbkrContractsModel por coincidencia exacta del símbolo del subyacente.
            3.- Si encuentra el contrato, obtener el conid del contrato.
            4.- validar el mes de expiracion consultando get_expiration_months y ver si se encuentra en la lista de meses.
            5.- Con el conid del contrato consultar api/ibkr.py InteractiveBrokersClient.marketdata_snapshot para obtener el precio del subyacente.
            6.- Obtener los strikes.
            7.- invocar _build_options_chain con el precio del subyacente, los strikes y el mes de expiracion.
            8.- con los conids de calls y puts consultar api/ibkr.py InteractiveBrokersClient.marketdata_snapshot para obtener bid, ask y last, y agregarlos a cada contrato.
            9.- devuelve la cadena de opciones
        """
        if not cod_subyacente or not str(cod_subyacente).strip():
            raise ValueError("El parámetro 'cod_subyacente' es requerido")

        cod_subyacente = str(cod_subyacente).strip()

        # 1. Si fch_expiracion es enviado obtener el mes en formato MESAÑO, ex JAN25,
        #    caso contrario fch_expiracion es la fecha del sistema y obtener el mes en formato MESAÑO.
        has_fch_expiracion = bool(
            fch_expiracion
            and (not isinstance(fch_expiracion, str) or fch_expiracion.strip())
        )
        if has_fch_expiracion:
            month_str = self._parse_expiration_month(fch_expiracion)
        else:
            fch_expiracion = date.today().strftime("%Y-%m-%d")
            month_str = self._parse_expiration_month(fch_expiracion)

        # 2. Buscar en la tabla IbkrContractsModel por coincidencia exacta del símbolo del subyacente.
        contract = IbkrContractsModel.find_by_symbol(cod_symbol=cod_subyacente)
        if not contract:
            raise ValueError(
                f"No se encontró el contrato para el símbolo '{cod_subyacente}'"
            )

        # 3. Si encuentra el contrato, obtener el conid del contrato.
        conid = contract.conid
        if not conid:
            raise ValueError(
                f"No se encontró un conid válido para el símbolo '{cod_subyacente}'"
            )

        # 4. Validar el mes de expiración consultando get_expiration_months y ver si se encuentra en la lista de meses.
        expiration_months = self.get_expiration_months(cod_symbol=cod_subyacente)
        valid_months = [str(m).strip().upper() for m in expiration_months]
        if month_str.upper() not in valid_months:
            raise ValueError(
                f"El mes de expiración '{month_str}' no está disponible para el símbolo '{cod_subyacente}'"
            )

        # 5. Con el conid del contrato consultar api/ibkr.py InteractiveBrokersClient.marketdata_snapshot para obtener el precio del subyacente.
        imp_underlying = self.get_underlying_price(
            conid=conid, cod_subyacente=cod_subyacente
        )

        # 6. Obtener los strikes.
        strikes_dict = self.get_strikes(
            cod_subyacente=cod_subyacente, expiracion=month_str
        )
        strikes_list = []
        if isinstance(strikes_dict, dict):
            calls_s = strikes_dict.get("call") or []
            puts_s = strikes_dict.get("put") or []
            strikes_list = list(set(calls_s + puts_s))
        elif isinstance(strikes_dict, (list, tuple)):
            strikes_list = list(set(strikes_dict))

        strikes_list = sorted([float(s) for s in strikes_list])

        # 7. Invocar _build_options_chain con el precio del subyacente, los strikes y el mes de expiracion.
        options_chain = self._build_options_chain(
            imp_underlying=imp_underlying,
            strikes=strikes_list,
            num_strikes=num_strikes if num_strikes is not None else 50,
            conid=conid,
            month=month_str,
            fch_expiracion=fch_expiracion,
        )

        # 8. Buscar en InteractiveBrokersClient.marketdata_snapshot los conids y sus bid, ask, last
        #    y luego al resultado de self._build_options_chain agregarles bid, ask, last.
        calls = options_chain.get("calls", [])
        puts = options_chain.get("puts", [])
        self._enrich_options_with_market_data(calls=calls, puts=puts)

        # 9. Devuelve la cadena de opciones.
        return options_chain
        