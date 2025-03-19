from common.AppException import AppException
from datetime import datetime, date, timedelta, MINYEAR, MAXYEAR
from dateutil.relativedelta import relativedelta
import calendar
from app import app


class CodigoMes:
    def __init__(self, value=None):
        self.value = value

        """
        if value is not None:
            self.value = self.parse(value)
        """

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

    @staticmethod
    def from_date(fecha: date):
        cod_mes = CodigoMes.componer(num_anyo=fecha.year, num_mes=fecha.month)
        return CodigoMes(cod_mes)

    @staticmethod
    def parse_string_client(valor):
        fch_mes = datetime.strptime(valor, app.config["CLIENT_DATE_FORMAT"])
        codigo_mes = int(f"{fch_mes.year}{str(fch_mes.month).zfill(2)}")
        return CodigoMes(value=codigo_mes)

    @staticmethod
    def descomponer(valor):
        valor = str(valor)
        num_anyo = int(valor[:4])
        num_mes = int(valor[-2:])
        return (num_anyo, num_mes)

    @staticmethod
    def componer(num_anyo, num_mes):
        return int(f"{num_anyo}{str(num_mes).zfill(2)}")

    def __mes_valido(self, num_mes):
        if 0 >= num_mes > 12:
            raise AppException(msg=f"El mes debe estar en el rango 0-12, valor: {num_mes}")

    def fecha(self):
        str_nueva_fecha = f"{str(self.value)}01"
        return datetime.strptime(str_nueva_fecha, "%Y%m%d")

    def get_fecha_primer_dia(self):
        anyo, mes = CodigoMes.descomponer(self.value)
        return date(anyo, mes, 1)

    def get_fecha_ult_dia(self):
        anyo, mes = CodigoMes.descomponer(self.value)
        (primer_dia, ultimo_dia) = calendar.monthrange(anyo, mes)
        return date(anyo, mes, ultimo_dia)


class Mes:
    def __init__(self, anyo=None, mes=None):
        self.anyo = anyo
        self.mes = mes

    @staticmethod
    def from_fecha(fecha: date):
        return Mes(
            anyo=fecha.year,
            mes=fecha.month
        )

    @staticmethod
    def diferencia(fch_mes_base:date, fch_mes_ref:date):
        r = relativedelta(fch_mes_base, fch_mes_ref)
        diff = (r.years + 12) + r.months
        return diff

    def to_fecha_mes(self):
        return self.to_fecha_primer_dia()

    def to_fecha_primer_dia(self):
        return date(self.anyo, self.mes, 1)

    def to_partes(self):
        return self.anyo, self.mes

    def codigo(self):
        return int("{0}{1}".format(str(self.anyo), str(self.mes).zfill(2)))

