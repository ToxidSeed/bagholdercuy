from common.api.iexcloud import iexcloud
from controller.base import Base
from common.Response import Response

class CotizacionManager(Base):
    def __init__(self):
        self.api = iexcloud()

    def get_cotizacion(self, args={}):
        symbol = args.get('symbol')
        quote = self.api.get_quote({"symbol":symbol})

        cotizacion = {
            "cod_symbol": quote.get("symbol"),
            "imp_cierre": quote.get("latestPrice")
        }

        return Response().from_raw_data(cotizacion)