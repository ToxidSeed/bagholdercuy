from common.api.iexcloud import iexcloud
from api.marketstack import MarketStackAPI
from controller.base import Base
from common.Response import Response
from parser.cotizacion import CotizacionParser


class CotizacionManager(Base):
    def __init__(self):
        self.api = MarketStackAPI()

    def get_cotizacion(self, args={}):
        # return Response().from_raw_data({})

        cotizacion_parser = CotizacionParser()
        args = cotizacion_parser.parse_args_get_cotizacion(args=args)
        cod_symbol = args.get('cod_symbol')
        quote = self.api.get_intraday_latest(cod_symbol)
        cotizacion = {            
            "cod_symbol": quote.get("symbol"),
            "imp_cierre_anterior": quote.get("close"),
            "imp_cierre": quote.get("marketstack_last")
        }

        return Response().from_raw_data(cotizacion)

    def get_cotizacion_semana(self, args={}):
        parser = CotizacionParser()
        pass
