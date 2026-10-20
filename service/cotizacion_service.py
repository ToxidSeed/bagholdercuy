import logging
from typing import Dict, Any, Type, Union, List

from common.AppException import AppException
from service.markets_data_providers.base.quote_provider_base import QuoteProviderBase
from service.markets_data_providers.ibkr.ibkr_cotizacion_service import (
    IbkrCotizacionService,
)
from service.markets_data_providers.marketdata.marketdata_cotizacion_service import (
    MarketDataCotizacionService,
)

logger = logging.getLogger(__name__)


class CotizacionService:
    DEFAULT_PROVIDER = "ibkr"

    def __init__(self, providers: Dict[str, Any] = None):
        """
        Inicializa el servicio de cotización con el registro de proveedores de mercado.
        """
        self._providers: Dict[str, Any] = providers or {
            "ibkr": IbkrCotizacionService,
            "interactivebrokers": IbkrCotizacionService,
            "interactive_brokers": IbkrCotizacionService,
            "marketdata": MarketDataCotizacionService,
        }

    def register_provider(
        self, name: str, provider: Union[Type[QuoteProviderBase], QuoteProviderBase]
    ):
        """
        Permite registrar dinámicamente un nuevo proveedor de datos de mercado.
        """
        self._providers[name.strip().lower()] = provider

    def get_provider(self, name: str = None):
        key = (name or self.DEFAULT_PROVIDER).strip().lower()
        provider_cls_or_inst = self._providers.get(key)
        if not provider_cls_or_inst:
            valid = ", ".join(sorted(self._providers.keys()))
            raise AppException(
                msg=f"Proveedor de datos '{key}' no soportado. Proveedores válidos: {valid}"
            )
        if callable(provider_cls_or_inst) and isinstance(provider_cls_or_inst, type):
            return provider_cls_or_inst()
        return provider_cls_or_inst

    def resolve_items_to_quote(
        self,
        symbol_ids: List[int] = None,
        contrato_ids: List[int] = None,
        cod_symbols: List[str] = None,
    ) -> List[dict]:
        """
        Resuelve los identificadores de activos (tb_symbol) y opciones (tb_contrato_opcion)
        a sus respectivos tickers cod_symbol para solicitar cotizaciones.
        """
        items: List[dict] = []

        if symbol_ids:
            from model.symbol import SymbolModel

            symbols = SymbolModel.query.filter(
                SymbolModel.id_symbol.in_(symbol_ids)
            ).all()
            sym_map = {s.id_symbol: s.symbol for s in symbols}
            for sid in symbol_ids:
                cod = sym_map.get(sid)
                if cod:
                    items.append(
                        {
                            "id_symbol": sid,
                            "id_contrato_opcion": None,
                            "cod_symbol": cod,
                        }
                    )
                else:
                    logger.warning(
                        f"id_symbol {sid} no encontrado en la base de datos"
                    )
                    items.append(
                        {
                            "id_symbol": sid,
                            "id_contrato_opcion": None,
                            "cod_symbol": str(sid),
                        }
                    )

        if contrato_ids:
            from model.contrato_opcion import ContratoOpcionModel

            contratos = ContratoOpcionModel.query.filter(
                ContratoOpcionModel.id_contrato_opcion.in_(contrato_ids)
            ).all()
            contrato_map = {c.id_contrato_opcion: c.cod_symbol for c in contratos}
            for cid in contrato_ids:
                cod = contrato_map.get(cid)
                if cod:
                    items.append(
                        {
                            "id_symbol": None,
                            "id_contrato_opcion": cid,
                            "cod_symbol": cod,
                        }
                    )
                else:
                    logger.warning(
                        f"id_contrato_opcion {cid} no encontrado en la base de datos"
                    )
                    items.append(
                        {
                            "id_symbol": None,
                            "id_contrato_opcion": cid,
                            "cod_symbol": str(cid),
                        }
                    )

        if cod_symbols:
            for sym in cod_symbols:
                items.append(
                    {
                        "id_symbol": None,
                        "id_contrato_opcion": None,
                        "cod_symbol": sym,
                    }
                )

        return items

    def get_cotizaciones(
        self, items: List[dict], provider: str = None
    ) -> List[dict]:
        """
        Obtiene cotizaciones en lote para una lista de items resueltos.
        """
        if not items:
            return []

        provider_name = (provider or self.DEFAULT_PROVIDER).strip().lower()
        provider_inst = self.get_provider(provider_name)

        try:
            quotes = provider_inst.get_quotes(items)
        except AppException:
            raise
        except Exception as e:
            logger.error(
                f"Error al obtener cotizaciones con proveedor '{provider_name}': {e}",
                exc_info=True,
            )
            raise AppException(
                msg="No se pudo obtener la cotización desde el proveedor de mercado."
            )

        return quotes

    def get_cotizacion(self, cod_symbol: str, provider: str = None) -> dict:
        """
        Obtiene la cotización de un símbolo individual usando el proveedor especificado.
        """
        if not cod_symbol or not str(cod_symbol).strip():
            raise AppException(msg="El código del símbolo es requerido")

        clean_symbol = str(cod_symbol).strip()
        provider_name = (provider or self.DEFAULT_PROVIDER).strip().lower()

        provider_inst = self.get_provider(provider_name)

        try:
            quote = provider_inst.get_quote(cod_symbol=clean_symbol)
        except AppException:
            raise
        except Exception as e:
            logger.error(
                f"Error al obtener cotización de {clean_symbol} con proveedor '{provider_name}': {e}",
                exc_info=True,
            )
            raise AppException(
                msg="No se pudo obtener la cotización desde el proveedor de mercado."
            )

        return quote
