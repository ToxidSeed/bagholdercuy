from common.AppException import AppException
from datetime import datetime, date, timedelta, MINYEAR, MAXYEAR


class CodigoSemana:
    def __init__(self, value):
        self.value = self.parse(value)

    def restar(self, num_semanas):
        cod_semana_str = str(self.value)
        num_anyo_semana, num_semana = CodigoSemana.descomponer(valor=cod_semana_str)
        fch_ini_semana = date.fromisocalendar(num_anyo_semana, num_semana, 1)
        td = timedelta(weeks=num_semanas)
        fch_nueva_semana = fch_ini_semana - td
        num_anyo_resultado, num_semana_resultado, num_dia_semana_resultado = fch_nueva_semana.isocalendar()
        return CodigoSemana(
            value=CodigoSemana.componer(num_anyo_semana=num_anyo_resultado, num_semana=num_semana_resultado)
        )

    def parse(self, valor):
        # Si es nulo retorna null
        if valor in [None, ""]:
            return None

        # si es una fecha procesa la fecha
        if isinstance(valor, date):
            return self.parse_fecha(valor)

        if isinstance(valor, str):
            return self.parse_string(valor)

        if isinstance(valor, int):
            return self.parse_int(valor)

        return int(valor)

    def parse_fecha(self, fch_dia):
        num_anyo, num_semana, num_dia_semana = fch_dia.isocalendar()
        return CodigoSemana.componer(num_anyo_semana=num_anyo, num_semana=num_semana)

    def parse_string(self, valor):
        valor = valor.replace("/", "")
        if len(valor) != 6:
            raise AppException(msg=f"El codigo de semana debe tener 6 caracteres: {valor}")

        num_anyo_semana, num_semana = CodigoSemana.descomponer(valor=valor)

        if num_semana > 52 or num_semana < 0:
            raise AppException(msg=f"La semana debe tener un rango de 0-52 {num_semana}")

        if num_anyo_semana < MINYEAR or num_anyo_semana > MAXYEAR:
            raise AppException(msg=f"El anyo debe tener un rango de {MINYEAR}-{MAXYEAR}: {num_anyo_semana}")

        return CodigoSemana.componer(num_anyo_semana=num_anyo_semana, num_semana=num_semana)

    def parse_int(self, valor):
        valor = str(valor)
        return self.parse_string(valor)

    def format(self, sep="/"):
        if self.value is None:
            return ""

        str_cod_semana = str(self.value)
        return f"{str_cod_semana[:4]}{sep}{str_cod_semana[-2:]}"

    def to_fecha_inicio_semana(self):
        anyo, semana = CodigoSemana.descomponer(self.value)
        return date.fromisocalendar(anyo, semana, 1)

    def to_fecha_ultdia_semana(self):
        anyo, semana = CodigoSemana.descomponer(self.value)
        return date.fromisocalendar(anyo, semana, 7)

    def componer(num_anyo_semana, num_semana):
        return int("{0}{1}".format(str(num_anyo_semana), str(num_semana).zfill(2)))

    @staticmethod
    def descomponer(valor):
        valor = str(valor)
        num_anyo = int(valor[:4])
        num_semana = int(valor[-2:])
        return (num_anyo, num_semana)

    def separar(self):
        return CodigoSemana.descomponer(self.value)


class Semana:
    def __init__(self, anyo=None, semana=None):
        self.anyo = anyo
        self.semana = semana

    @staticmethod
    def from_fecha(fecha: date):
        num_anyo, num_semana, num_dia_semana = fecha.isocalendar()
        sem = Semana(
            num_anyo,
            num_semana
        )
        return sem

    @staticmethod
    def diferencia(cod_semana_base, cod_semana_referencia):
        fch_semana_base = Semana.from_codigo(cod_semana_base).fch_semana()
        fch_semana_ref = Semana.from_codigo(cod_semana_referencia).fch_semana()
        return abs((fch_semana_ref - fch_semana_base).days / 7)

    @staticmethod
    def from_codigo(cod_semana):
        valor = str(cod_semana)
        num_anyo = int(valor[:4])
        num_semana = int(valor[-2:])
        return Semana(anyo=num_anyo, semana=num_semana)

    def codigo(self):
        return int("{0}{1}".format(str(self.anyo), str(self.semana).zfill(2)))

    def fch_semana(self):
        return date.fromisocalendar(self.anyo, self.semana, 1)
