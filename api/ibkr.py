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
        return response.json()

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
        return response.json()

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
        https://ibkrcampus.com/docs/web-api/v1/endpoints/market-data/historical-market-data
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
        return response.json()


