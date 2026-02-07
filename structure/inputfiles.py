from dataclasses import dataclass
import datetime

@dataclass(order=True)
class CsvNasdaq:
    fch_serie: datetime.date
    imp_apertura: float
    imp_maximo: float
    imp_minimo: float
    imp_cierre: float
    volumen: float

