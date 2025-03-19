from app import app
from datetime import date
import requests


class MarketData:
    def get_options_chain(self, cod_subyacente=None, fch_expiracion: date = None):
        url = f"{app.config['MARKETDATA_ENDPOINT']}/options/chain/{cod_subyacente}/"

        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "token": app.config.get("MARKETDATA_API_TOKEN")
        }

        if fch_expiracion is not None:
            params["expiration"] = fch_expiracion.isoformat()

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        contratos = []
        for index, cod_symbol in enumerate(data.get("optionSymbol"), start=0):
            contratos.append({
                "optionSymbol": cod_symbol,
                "underlying": data["underlying"][index],
                "expiration": data["expiration"][index],
                "strike": data["strike"][index],
                "side": data["side"][index]
            })

        return contratos

