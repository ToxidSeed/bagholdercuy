from app import db
from api.fmp import FinancialModelingGrepAPI
from rich.pretty import pprint
from datetime import date, datetime
from model.stocksplit import StockSplitModel
from reader.symbol import SymbolReader


class StockSplitFMPService:
    def procesar(self, cod_symbol):
        # obtener el identificador del symbol
        sr = SymbolReader()
        symbol = sr.get(cod_symbol=cod_symbol)

        # obtener los splits
        api = FinancialModelingGrepAPI()
        response = api.stock_split(cod_symbol=symbol.symbol)
        
        # por cada split obtenido revisar si ya existe
        cod_symbol = response.get("symbol")
        records = response.get("historical")

        for elem in records:
            self.crear_stock_split(id_symbol=symbol.id, elem=elem)            

    def crear_stock_split(self, id_symbol, elem):

        nu_stock_split = StockSplitModel(
            id_symbol=id_symbol,
            fch_split=datetime.fromisoformat(elem.get("date")).date(),
            numerador=elem.get("numerator"),
            denominador=elem.get("denominator")
        )
        db.session.add(nu_stock_split)
        



