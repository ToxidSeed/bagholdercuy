from app import db
from model.CurrencyPairModel import CurrencyPairModel
from common.Response import Response

class CurrencyPairManager:
    def __init__(self):
        pass

class PairFinder:
    def __init__(self):
        pass

    def get_list_by_text(self, args={}):
        text = args["search_text"]
        pairs = CurrencyPairModel.query.filter(
            CurrencyPairModel.pair_name.ilike("%{0}%".format(text))
        ).all()

        return Response().from_raw_data(pairs)



