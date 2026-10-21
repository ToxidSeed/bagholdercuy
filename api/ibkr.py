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
    def secdef_search(
        cls,
        symbol=None,
        name=None,
        sec_type=None,
        secType=None,
        more=None,
        args=None,
        **kwargs,
    ):
        """
        POST /iserver/secdef/search
        Busca contratos/instrumentos financieros por símbolo o nombre en la plataforma de Interactive Brokers.
        """
        if args is None:
            args = {}

        combined_args = {**args, **kwargs}

        sym = combined_args.get("symbol", combined_args.get("ticker", symbol))

        if not sym:
            raise ValueError("symbol is required")

        is_name = combined_args.get("name", name)
        sec_type_val = combined_args.get(
            "secType", combined_args.get("sec_type", secType or sec_type)
        )
        more_val = combined_args.get("more", more)

        base = cls.get_base_endpoint().rstrip("/")
        endpoint = f"{base}/iserver/secdef/search"

        headers = {"Content-Type": "application/json"}
        payload = {"symbol": sym}

        if is_name is not None:
            payload["name"] = is_name
        if sec_type_val is not None:
            payload["secType"] = sec_type_val
        if more_val is not None:
            payload["more"] = more_val

        # Desactivamos verify=False por defecto ya que localmente el Gateway de IBKR suele usar certificados autofirmados (HTTP/HTTPS)
        response = requests.get(endpoint, params=payload, headers=headers, verify=False)
        return response.json()

    search = secdef_search
    iserver_secdef_search = secdef_search
