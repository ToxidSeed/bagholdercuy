from pydantic import BaseModel

class GetPosicionesAccionesParams(BaseModel):
    id_cuenta: int
