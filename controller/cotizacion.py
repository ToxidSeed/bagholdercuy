from api.marketdata import MarketDataAPI
from controller.base import Base
from common.Response import Response
from parser.cotizacion import CotizacionParser


class CotizacionManager(Base):
    AUTH_REQUIRED = False

    def __init__(self):
        self.api = MarketDataAPI()

    def get_cotizacion(self, args={}):
        cotizacion_parser = CotizacionParser()
        args = cotizacion_parser.parse_args_get_cotizacion(args=args)
        cod_symbol = args.get("cod_symbol")
        quote = self.api.quote(cod_symbol)

        if quote and quote.get("s") == "ok":
            last_list = quote.get("last") or []
            last_price = last_list[0] if len(last_list) > 0 else None
            change_list = quote.get("change") or []
            change = change_list[0] if len(change_list) > 0 else 0
            changepct_list = quote.get("changepct") or []
            changepct = changepct_list[0] if len(changepct_list) > 0 else 0
            prev_close = (
                round(last_price - change, 4)
                if last_price is not None and change is not None
                else None
            )

            cotizacion = {
                "cod_symbol": cod_symbol,
                "imp_cierre_anterior": prev_close,
                "imp_cierre": last_price,
                "imp_variacion": change,
                "pct_variacion": changepct,
            }
        else:
            cotizacion = {
                "cod_symbol": cod_symbol,
                "imp_cierre_anterior": None,
                "imp_cierre": None,
                "imp_variacion": None,
                "pct_variacion": None,
            }

        return Response().from_raw_data(cotizacion)

    def get_cotizacion_semana(self, args={}):
        parser = CotizacionParser()
        pass

