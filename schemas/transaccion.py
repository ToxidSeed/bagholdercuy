from pydantic import BaseModel

class TransaccionAgrupadaSearchRequest(BaseModel):
    id_cuenta: int
