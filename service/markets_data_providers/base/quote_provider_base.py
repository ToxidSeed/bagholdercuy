from abc import ABC, abstractmethod
from typing import List, Dict, Any


class QuoteProviderBase(ABC):
    """
    Clase base abstracta para proveedores de cotización de mercado (quotes).
    """

    name: str = "base"

    @abstractmethod
    def get_quote(self, cod_symbol: str) -> dict:
        """
        Obtiene la cotización actual para un solo símbolo.
        """
        pass

    def get_quotes(self, items: List[Dict[str, Any]]) -> List[dict]:
        """
        Obtiene la cotización para una lista de items.
        Cada item puede tener:
        - cod_symbol: str
        - id_symbol: Optional[int]
        - id_contrato_opcion: Optional[int]
        Por defecto, itera llamando a get_quote. Los proveedores pueden sobreescribir
        este método para optimizar llamadas batch (ej. IBKR marketdata_snapshot con múltiples conids).
        """
        results = []
        for it in items:
            cod_sym = it.get("cod_symbol")
            if not cod_sym:
                continue
            quote = self.get_quote(cod_sym)
            quote["id_symbol"] = it.get("id_symbol")
            quote["id_contrato_opcion"] = it.get("id_contrato_opcion")
            results.append(quote)
        return results

    def _empty_quote(
        self,
        cod_symbol: str,
        id_symbol: int = None,
        id_contrato_opcion: int = None,
    ) -> dict:
        return {
            "id_symbol": id_symbol,
            "id_contrato_opcion": id_contrato_opcion,
            "cod_symbol": cod_symbol,
            "imp_cierre": None,
            "imp_cierre_anterior": None,
            "imp_variacion": None,
            "pct_variacion": None,
            "provider": self.name,
        }
