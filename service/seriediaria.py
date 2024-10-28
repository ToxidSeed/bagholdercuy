from info.serie import SerieDiariaIntegridadInfo
from reader.seriediaria import SerieDiariaModel

from dataclasses import dataclass, field


@dataclass
class ReparacionStatus:
    cod_symbol: str = field(default="")
    msg: str = field(default="")

class SerieDiariaService:
    def __init__(self):
        pass

    def reparar(self, cod_symbol, serie_integridad_info: SerieDiariaIntegridadInfo):

        # Si el split no es correcto, reprocesamos a partir de la fecha en la que se ha catalogado en integridad
        if serie_integridad_info.split_correcto is False:
            


        

        
