from app import db
from api.fmp import FinancialModelingGrepAPI
from rich.pretty import pprint
from datetime import date, datetime
from model.stocksplit import StockSplitModel
from reader.symbol import SymbolReader
from rich.pretty import pprint

MYSQL_MIN_DATE = app.config["MYSQL_MAX_DATE"]


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

        splits_history_asc = sorted(records, key= lambda elem: elem.get("date"))        
        pprint(splits_history_asc)

        split_ant = None
        for split in splits_history_asc:
            self.crear_stock_split(id_symbol=symbol.id, cod_symbol=cod_symbol, split=split, split_ant=split_ant)       
            split_ant = split     

    def crear_stock_split(self, id_symbol, cod_symbol, split, split_ant):

        fch_split_ant = MYSQL_MIN_DATE if split_ant is None else datetime.fromisoformat(split_ant.get("date")).date()

        nu_stock_split = StockSplitModel(
            id_symbol=id_symbol,
            cod_symbol=cod_symbol,
            fch_split=datetime.fromisoformat(split.get("date")).date(),
            numerador=split.get("numerator"),
            denominador=split.get("denominator"),
            fch_split_anterior=fch_split_ant,
            factor_split=int(split.get("numerator"))/int(split.get("denominator"))
        )
        db.session.add(nu_stock_split)
        



