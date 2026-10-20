import logging
from api.marketdata import MarketDataAPI
from service.markets_data_providers.base.quote_provider_base import QuoteProviderBase

logger = logging.getLogger(__name__)


class MarketDataCotizacionService(QuoteProviderBase):
    name = "marketdata"

    def __init__(self, api: MarketDataAPI = None):
        self.api = api or MarketDataAPI()

    def get_quote(self, cod_symbol: str) -> dict:
        if not cod_symbol:
            raise ValueError("El parámetro 'cod_symbol' es requerido")

        try:
            quote = self.api.quote(cod_symbol)
        except Exception as e:
            logger.warning(
                f"Error al consultar quote en MarketDataAPI para '{cod_symbol}': {e}"
            )
            return self._empty_quote(cod_symbol)

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
            if prev_close and prev_close > 0 and change is not None:
                pct_var = round((change / prev_close) * 100, 4)
            elif changepct is not None:
                pct_var = round(changepct * 100, 4) if (abs(changepct) <= 1.0 and changepct != 0) else changepct
            else:
                pct_var = None

            return {
                "cod_symbol": cod_symbol,
                "imp_cierre": last_price,
                "imp_cierre_anterior": prev_close,
                "imp_variacion": change,
                "pct_variacion": pct_var,
                "provider": self.name,
            }

        return self._empty_quote(cod_symbol)
