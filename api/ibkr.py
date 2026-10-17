import os
import requests
from flask import current_app
from datetime import date


class InteractiveBrokersClient:
    def __init__(self):
        self._endpoint = None

    @property
    def base_endpoint(self):
        if self._endpoint is None:
            self._endpoint = self.get_base_endpoint()
        return self._endpoint

    @classmethod
    def get_base_endpoint(cls):
        endpoint = current_app.config.get("INTERACTIVE_BROKERS_ENDPOINT")
        if not endpoint:
            raise KeyError(
                "Configuración crítica faltante: 'INTERACTIVE_BROKERS_ENDPOINT' no está definida en app.config"
            )
        return endpoint

    @classmethod
    def _parse_response(cls, response, endpoint=""):
        status_code = getattr(response, "status_code", 200)
        if status_code == 401:
            raise ValueError(
                "La sesión con Interactive Brokers Gateway no está autenticada o ha expirado (HTTP 401). "
                "Por favor inicie sesión en el Gateway (https://localhost:5000)."
            )

        text = getattr(response, "text", None)
        if text is not None and not str(text).strip():
            if isinstance(status_code, int) and status_code < 400:
                return [] if any(k in endpoint for k in ("info", "contracts", "search")) else {}
            reason = getattr(response, "reason", "Error")
            raise ValueError(
                f"Interactive Brokers Gateway devolvió una respuesta vacía (HTTP {status_code} {reason}). "
                "Verifique que la sesión en el Gateway esté activa."
            )

        try:
            return response.json()
        except Exception as e:
            if isinstance(status_code, int) and status_code >= 400:
                raise ValueError(
                    f"Error de Interactive Brokers Gateway (HTTP {status_code}): {str(text)[:200]}"
                )
            raise ValueError(
                f"Respuesta no válida de Interactive Brokers Gateway: {str(e)}"
            )

    @classmethod
    def all_conids(cls, exchange=None, asset_class=None, args=None):
        """
        GET /trsrv/all-conids
        Devuelve una lista de todos los CONIDs disponibles en la plataforma de Interactive Brokers.
        """
        if args is None:
            args = {}

        exch = args.get("exchange", exchange)

        if not exch:
            raise ValueError("exchange is required")

        base = cls.get_base_endpoint().rstrip("/")
        endpoint = f"{base}/trsrv/all-conids"

        headers = {"Content-Type": "application/json"}
        params = {"exchange": exch}

        # Desactivamos verify=False por defecto ya que localmente el Gateway de IBKR suele usar certificados autofirmados (HTTP/HTTPS)
        response = requests.get(endpoint, params=params, headers=headers, verify=False)
        return cls._parse_response(response, endpoint=endpoint)

    @classmethod
    def search_contract_by_symbol(
        cls, symbol=None, name=False, sec_type=None, args=None
    ):
        """
        POST /iserver/secdef/search
        Busca contratos por símbolo o nombre en la API de Interactive Brokers.
        https://ibkrcampus.com/docs/web-api/v1/endpoints/contract/search-contract-by-symbol
        """
        if args is None:
            args = {}

        sym = args.get("symbol", symbol)
        if not sym:
            raise ValueError("symbol is required")

        nm = args.get("name", name)
        stype = args.get("secType", args.get("sec_type", sec_type))

        base = cls.get_base_endpoint().rstrip("/")
        endpoint = f"{base}/iserver/secdef/search"

        headers = {"Content-Type": "application/json"}
        payload = {"symbol": sym, "name": bool(nm)}
        if stype:
            payload["secType"] = stype

        response = requests.post(
            endpoint, json=payload, headers=headers, verify=False
        )
        return cls._parse_response(response, endpoint=endpoint)

    @classmethod
    def historical_market_data(
        cls,
        conid=None,
        period=None,
        bar=None,
        exchange=None,
        start_time=None,
        outside_rth=None,
        source=None,
        args=None,
    ):
        """
        GET /iserver/marketdata/history
        Obtiene datos históricos de mercado para un CONID específico.
        https://www.interactivebrokers.com/docs/web-api/v1/endpoints/market-data/historical-market-data
        https://www.interactivebrokers.com/docs/web-api/api-reference/trading/trading-market-data/get-md-history
        """
        if args is None:
            args = {}

        cid = args.get("conid", conid)
        if not cid:
            raise ValueError("conid is required")

        prd = args.get("period", period)
        if not prd:
            raise ValueError("period is required")

        b = args.get("bar", bar)
        exch = args.get("exchange", exchange)
        stime = args.get("startTime", args.get("start_time", start_time))
        rth = args.get("outsideRth", args.get("outside_rth", outside_rth))
        src = args.get("source", source)

        base = cls.get_base_endpoint().rstrip("/")
        endpoint = f"{base}/iserver/marketdata/history"

        headers = {"Content-Type": "application/json"}
        params = {
            "conid": cid,
            "period": prd,
        }

        if b is not None:
            params["bar"] = b
        if exch is not None:
            params["exchange"] = exch
        if stime is not None:
            params["startTime"] = stime
        if rth is not None:
            params["outsideRth"] = rth
        if src is not None:
            params["source"] = src

        response = requests.get(endpoint, params=params, headers=headers, verify=False)
        return cls._parse_response(response, endpoint=endpoint)

    @classmethod
    def marketdata_snapshot(
        cls,
        conids=None,
        fields=None,
        conid=None,
        args=None,
    ):
        """
        GET /iserver/marketdata/snapshot
        Obtiene una instantánea de datos de mercado en tiempo real (Top of Book / Level 1) para uno o varios CONIDs.
        https://ibkrcampus.com/docs/web-api/v1/endpoints/market-data/market-data#snapshot-market-data
        """
        if args is None:
            args = {}

        cids = args.get("conids", conids)
        if cids is None:
            cids = args.get("conid", conid)

        if not cids:
            raise ValueError("conids is required")

        if isinstance(cids, (list, tuple, set)):
            cids_str = ",".join(str(c) for c in cids)
        else:
            cids_str = str(cids).strip()

        flds = args.get("fields", fields)
        if flds is not None:
            if isinstance(flds, (list, tuple, set)):
                flds_str = ",".join(str(f) for f in flds)
            else:
                flds_str = str(flds).strip()
        else:
            flds_str = None

        base = cls.get_base_endpoint().rstrip("/")
        endpoint = f"{base}/iserver/marketdata/snapshot"

        headers = {"Content-Type": "application/json"}
        params = {"conids": cids_str}
        if flds_str:
            params["fields"] = flds_str

        response = requests.get(endpoint, params=params, headers=headers, verify=False)
        return cls._parse_response(response, endpoint=endpoint)
    

    @classmethod
    def secdef_strikes(
        cls,
        conid=None,
        sec_type="OPT",
        month=None,
        exchange=None,
        args=None,
    ):
        """
        GET /iserver/secdef/strikes
        Consulta los precios de ejercicio (strikes) de opciones o warrants para un CONID y mes de expiración especificados.
        https://ibkrcampus.com/docs/web-api/v1/endpoints/contract/secdef-strikes
        """
        if args is None:
            args = {}

        cid = args.get("conid", conid)
        if not cid:
            raise ValueError("conid is required")

        m = args.get("month", month)
        if not m:
            raise ValueError("month is required")

        stype = args.get("sectype", args.get("secType", args.get("sec_type", sec_type)))
        if not stype:
            stype = "OPT"

        exch = args.get("exchange", exchange)

        base = cls.get_base_endpoint().rstrip("/")
        endpoint = f"{base}/iserver/secdef/strikes"

        headers = {"Content-Type": "application/json"}
        params = {
            "conid": cid,
            "sectype": stype,
            "month": m,
        }
        if exch is not None:
            params["exchange"] = exch

        response = requests.get(endpoint, params=params, headers=headers, verify=False)
        return cls._parse_response(response, endpoint=endpoint)

    strikes = secdef_strikes

    @classmethod
    def secdef_info(
        cls,
        conid=None,
        sec_type="OPT",
        month=None,
        exchange=None,
        strike=None,
        right=None,
        issuer_id=None,
        args=None,
    ):
        """
        GET /iserver/secdef/info
        Consulta la definición y especificaciones de contrato (secdef) para derivados (opciones, futuros, warrants, etc.) o instrumentos financieros en IBKR.
        https://ibkrcampus.com/docs/web-api/v1/endpoints/contract/secdef-info
        """
        if args is None:
            args = {}

        cid = args.get("conid", conid)
        if not cid:
            raise ValueError("conid is required")

        stype = args.get("sectype", args.get("secType", args.get("sec_type", sec_type)))
        if not stype:
            stype = "OPT"

        m = args.get("month", month)
        exch = args.get("exchange", exchange)
        strk = args.get("strike", strike)
        rgt = args.get("right", right)
        iss_id = args.get("issuerId", args.get("issuer_id", issuer_id))

        base = cls.get_base_endpoint().rstrip("/")
        endpoint = f"{base}/iserver/secdef/info"

        headers = {"Content-Type": "application/json"}
        params = {
            "conid": cid,
            "sectype": stype,
        }
        if m is not None:
            params["month"] = m
        if exch is not None:
            params["exchange"] = exch
        if strk is not None:
            params["strike"] = strk
        if rgt is not None:
            if isinstance(rgt, str):
                r_upper = rgt.strip().upper()
                if r_upper in ("C", "CALL"):
                    rgt = "C"
                elif r_upper in ("P", "PUT"):
                    rgt = "P"
            params["right"] = rgt
        if iss_id is not None:
            params["issuerId"] = iss_id

        response = requests.get(endpoint, params=params, headers=headers, verify=False)
        return cls._parse_response(response, endpoint=endpoint)

    info = secdef_info



