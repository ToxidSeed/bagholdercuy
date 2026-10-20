from pydantic import BaseModel, Field, model_validator
from typing import Optional, Union, List


class CotizacionGetRequest(BaseModel):
    id_symbol: Optional[Union[str, int, List[Union[int, str]]]] = Field(
        default=None,
        description="ID(s) de tb_symbol para activos no opciones. Se puede enviar un entero, lista o string separado por comas.",
    )
    id_contrato_opcion: Optional[Union[str, int, List[Union[int, str]]]] = Field(
        default=None,
        description="ID(s) de tb_contrato_opcion para opciones. Se puede enviar un entero, lista o string separado por comas.",
    )
    cod_symbol: Optional[str] = Field(
        default=None,
        description="Código o ticker(s) del símbolo a cotizar (separados por coma o único)",
    )
    provider: Optional[str] = Field(
        default="ibkr",
        description="Proveedor de datos de mercado (default: 'ibkr'). Opciones: 'ibkr', 'marketdata'",
    )

    @model_validator(mode="after")
    def validate_at_least_one(self):
        has_id_sym = self.id_symbol is not None and str(self.id_symbol).strip() != ""
        has_id_opt = (
            self.id_contrato_opcion is not None
            and str(self.id_contrato_opcion).strip() != ""
        )
        has_cod_sym = (
            self.cod_symbol is not None and str(self.cod_symbol).strip() != ""
        )
        if not (has_id_sym or has_id_opt or has_cod_sym):
            raise ValueError(
                "Debe enviar al menos uno de los parámetros: 'id_symbol', 'id_contrato_opcion' o 'cod_symbol'"
            )
        return self

    @staticmethod
    def _parse_ids(val: Optional[Union[str, int, List[Union[int, str]]]]) -> List[int]:
        if val is None:
            return []
        if isinstance(val, (list, tuple, set)):
            parsed = []
            for item in val:
                for sub in str(item).split(","):
                    sub = sub.strip()
                    if sub.isdigit():
                        parsed.append(int(sub))
            return parsed
        elif isinstance(val, int):
            return [val]
        elif isinstance(val, str):
            parsed = []
            for sub in val.split(","):
                sub = sub.strip()
                if sub.isdigit():
                    parsed.append(int(sub))
            return parsed
        return []

    def get_symbol_ids(self) -> List[int]:
        return self._parse_ids(self.id_symbol)

    def get_contrato_opcion_ids(self) -> List[int]:
        return self._parse_ids(self.id_contrato_opcion)

    def get_cod_symbols(self) -> List[str]:
        if not self.cod_symbol:
            return []
        parts = [s.strip() for s in str(self.cod_symbol).split(",") if s.strip()]
        return parts

    @property
    def is_bulk_request(self) -> bool:
        if self.id_symbol is not None and str(self.id_symbol).strip() != "":
            return True
        if (
            self.id_contrato_opcion is not None
            and str(self.id_contrato_opcion).strip() != ""
        ):
            return True
        if len(self.get_cod_symbols()) > 1:
            return True
        return False
