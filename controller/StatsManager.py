from app import app, db
from model.StockData import StockData
from common.Response import Response
import common.Converter as Converter


class Change:
    def __init__(self):
        pass

    def close(self, args):
        symbol = 'CCL'

        quotes = db.session.query(
            StockData
        ).filter(
            StockData.frequency == "weekly",
            StockData.symbol == symbol,
            StockData.price_date >= '2020-01-01'
        ).order_by(StockData.price_date).all()

        weekly_data = []
        for elem in quotes:
            close_pct = round(((elem.close - elem.open)/elem.open)*100,3)
            weekly_elem = {
                "price_date":elem.price_date.strftime('%Y-%m-%d'),
                "close_pct":float(close_pct)
            }
            weekly_data.append(weekly_elem)

        return Response(input_data=weekly_data).get()

