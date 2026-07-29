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
