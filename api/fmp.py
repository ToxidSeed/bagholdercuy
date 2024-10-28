import requests
from app import app

BASE_ENDPOINT = app.config["FINANCIAL_MODELING_GREP_ENDPOINT"]
TOKEN = app.config["FINANCIAL_MODELING_GREP_API_TOKEN"]


class FinancialModelingGrepAPI:    
    def stock_split(self, cod_symbol):
        headers = {
            'Content-Type': 'application/json'
        }
        params = {         
            "apikey":TOKEN
        }
        endpoint = f"{BASE_ENDPOINT}/historical-price-full/stock_split/{cod_symbol}"
        response = requests.get(endpoint,params=params, headers=headers)
        result = response.json()
        return result
