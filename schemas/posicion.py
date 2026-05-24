from pydantic import BaseModel, model_validator
from typing import List, Optional

class RecalcularPosicionesRequest(BaseModel):
    id_cuenta: int
    cod_tipo_procesamiento: str
    cod_symbol_list: Optional[List[str]] = None

    @model_validator(mode='after')
    def check_procesamiento(self):
        if self.cod_tipo_procesamiento not in ["TODOS", "SELECCIONADOS"]:
            raise ValueError('cod_tipo_procesamiento must be "TODOS" or "SELECCIONADOS"')

        if self.cod_tipo_procesamiento == "TODOS":
            if self.cod_symbol_list is not None and len(self.cod_symbol_list) > 0:
                raise ValueError('cod_symbol_list must be empty if cod_tipo_procesamiento is TODOS')
        
        if self.cod_tipo_procesamiento == "SELECCIONADOS":
            if not self.cod_symbol_list or len(self.cod_symbol_list) == 0:
                raise ValueError('cod_symbol_list is required and must not be empty if cod_tipo_procesamiento is SELECCIONADOS')

        return self
