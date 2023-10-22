from common.AppException import AppException
from datetime import datetime, date, timedelta, MINYEAR, MAXYEAR
from dateutil.relativedelta import relativedelta

class CodigoMes:
    def __init__(self, value):
        self.value = self.parse(value)

    def restar(self,  num_meses):
        fecha = self.fecha()
        rd = relativedelta(months=num_meses * -1)
        nueva_fecha = fecha + rd
        return CodigoMes(nueva_fecha)

    def parse(self, valor):
        if valor in [None,""]:
            return None
        
        if isinstance(valor, date):
            return self.parse_date(valor)

        if isinstance(valor, str):
            return self.parse_string(valor)

    def parse_string(self, valor):
        valor = valor.replace("/")

        if len(valor) != 6:
            raise AppException(msg=f"El codigo de mes debe tener 6 caracteres: {valor}")
        
        num_anyo, num_mes = CodigoMes.descomponer(valor)
        self.__mes_valido(num_mes=num_mes)

        return CodigoMes.componer(num_anyo=num_anyo, num_mes=num_mes)
    
    def parse_date(self, fecha):        
        return CodigoMes.componer(num_anyo=fecha.year, num_mes=fecha.month)
        
    def descomponer(valor):
        valor = str(valor)
        num_anyo = int(valor[:4])
        num_mes = int(valor[-2:])
        return (num_anyo, num_mes)
    
    def componer(num_anyo, num_mes):
        return int(f"{num_anyo}{str(num_mes).zfill(2)}")

    def __mes_valido(self, num_mes):
        if num_mes <= 0 and num_mes > 12:
            raise AppException(msg=f"El mes debe estar en el rango 0-12, valor: {num_mes}")

    def fecha(self):
        str_nueva_fecha = f"{str(self.value)}01"
        return datetime.strptime(str_nueva_fecha,"%Y%m%d")