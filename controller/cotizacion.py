from common.api.iexcloud import iexcloud
from controller.base import Base
from common.Response import Response

class CotizacionManager(Base):
    def __init__(self):
        self.api = iexcloud()

    def get_cotizacion(self, args={}):
        cod_symbol = args.get('cod_symbol')
        quote = self.api.get_quote({"symbol":cod_symbol})

        cotizacion = {
            "cod_symbol": quote.get("symbol"),
            "imp_cierre": quote.get("latestPrice")
        }

        return Response().from_raw_data(cotizacion)