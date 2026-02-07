from parser.base import BaseParser
from datetime import date, datetime
from common.AppException import AppException
from domain.semana import CodigoSemana
from domain.mes import CodigoMes, Mes


DIAS = "DIAS"
SEMANAS = "SEMANAS"
MESES = "MESES"


class MetricaParser(BaseParser):
    def __init__(self, args=None):
        super().__init__(args=args)

    def parse_args_get_metricas_diarias_de_cierres_positivos(self, args=None):
        #inicializando
        self.params.set_params(args=args)

        param_cod_symbol = self.params.parse("cod_symbol", requerido=True)
        cod_tipo_periodo = self.params.parse("cod_tipo_periodo", requerido=True)

        if cod_tipo_periodo.valor.upper() not in [DIAS, SEMANAS, MESES]:
            raise AppException(msg=f"El tipo de periodo {cod_tipo_periodo.valor} no es valido")

        param_valor_inicial_periodo = self.params.parse("fch_desde", requerido=True, datatype=date)
        param_valor_final_periodo = self.params.parse("fch_hasta", requerido=True, datatype=date)

        fch_desde = param_valor_inicial_periodo.valor
        fch_hasta = param_valor_final_periodo.valor
        if cod_tipo_periodo.valor.upper() == SEMANAS:
            fch_desde = self.convert_semana_a_fecha(param_valor_inicial_periodo.valor)
            fch_hasta = self.convert_semana_a_fecha(param_valor_final_periodo.valor)

        if cod_tipo_periodo.valor.upper() == MESES:
            fch_desde = self.convert_mes_a_fecha(param_valor_inicial_periodo.valor)
            fch_hasta = self.convert_mes_a_fecha(param_valor_final_periodo.valor)

        if fch_desde > fch_hasta:
            raise AppException(msg="La fecha desde debe ser menor o igual a la fecha hasta")

        params = {
            "cod_symbol": param_cod_symbol.valor,
            "fch_desde":fch_desde,
            "fch_hasta": fch_hasta
        }

        return params


    def parse_args_get_metricas_diarias_de_cierres_negativos(self, args={}):
        self.params.set_params(args=args)

        param_cod_symbol = self.params.parse("cod_symbol", requerido=True)
        param_cod_tipo_periodo = self.params.parse("cod_tipo_periodo", requerido=True)

        param_valor_inicial_periodo = self.params.parse("fch_desde", requerido=True, datatype=date)
        param_valor_final_periodo = self.params.parse("fch_hasta", requerido=True, datatype=date)

        fch_desde = None
        fch_hasta = None

        if param_cod_tipo_periodo.valor.upper() == DIAS:
            fch_desde = param_valor_inicial_periodo.valor
            fch_hasta = param_valor_final_periodo.valor

        if param_cod_tipo_periodo.valor.upper() == SEMANAS:
            fch_desde = self.convert_semana_a_fecha(param_valor_inicial_periodo.valor)
            fch_hasta = self.convert_semana_a_fecha(param_valor_final_periodo.valor)

        if param_cod_tipo_periodo.valor.upper() == MESES:
            fch_desde = self.convert_mes_a_fecha(param_valor_inicial_periodo.valor)
            fch_hasta = self.convert_mes_a_fecha(param_valor_final_periodo.valor)

        if (fch_desde or fch_hasta) in [None, ""]:
            raise AppException(msg="No se ha enviado un rango valido para procesar las metricas")

        if fch_desde > fch_hasta:
            raise AppException(msg="La fecha desde debe ser menor o igual a la fecha hasta")

        params = {
            "cod_symbol": param_cod_symbol.valor,
            "fch_desde": fch_desde,
            "fch_hasta": fch_hasta
        }

        return params

    def parse_args_get_metricas_semanales_de_cierres_positivos(self, args={}):
        self.params.set_params(args=args)

        param_cod_symbol = self.params.parse("cod_symbol", requerido=True)
        param_cod_tipo_periodo = self.params.parse("cod_tipo_periodo", requerido=True)

        param_valor_inicial_periodo = self.params.parse("fch_desde", requerido=True)
        param_valor_final_periodo = self.params.parse("fch_hasta", requerido=True)

        cod_semana_inicial = None
        cod_semana_final = None

        if param_cod_tipo_periodo.valor.upper() == DIAS:
            cod_semana_inicial = self.convert_fecha_a_semana(date.fromisoformat(param_valor_inicial_periodo.valor))
            cod_semana_final = self.convert_fecha_a_semana(date.fromisoformat(param_valor_final_periodo.valor))

        if param_cod_tipo_periodo.valor.upper() == SEMANAS:
            cod_semana_inicial = CodigoSemana(param_valor_inicial_periodo).value
            cod_semana_final = CodigoSemana(param_valor_final_periodo).value

        if param_cod_tipo_periodo.valor.upper() == MESES:
            cod_semana_inicial = CodigoSemana(CodigoMes(param_valor_inicial_periodo).get_fecha_primer_dia()).value
            cod_semana_final = CodigoSemana(CodigoMes(param_valor_final_periodo).get_fecha_ult_dia()).value

        if cod_semana_inicial > cod_semana_final:
            raise AppException(msg="La semana inicial debe ser menor o igual a la semana final")

        params = {
            "cod_symbol": param_cod_symbol.valor,
            "cod_semana_desde": cod_semana_inicial,
            "cod_semana_hasta": cod_semana_final
        }
        return params

    def parse_args_get_metricas_semanales_de_cierres_negativos(self, args={}):
        self.params.set_params(args=args)
        param_cod_symbol = self.params.parse("cod_symbol", requerido=True)
        param_cod_tipo_periodo = self.params.parse("cod_tipo_periodo", requerido=True)

        param_valor_inicial_periodo = self.params.parse("fch_desde", requerido=True)
        param_valor_final_periodo = self.params.parse("fch_hasta", requerido=True)

        cod_semana_inicial = None
        cod_semana_final = None

        if param_cod_tipo_periodo.valor.upper() == DIAS:
            cod_semana_inicial = CodigoSemana.from_fecha(date.fromisoformat(param_valor_inicial_periodo.valor)).value
            cod_semana_final = CodigoSemana.from_fecha(date.fromisoformat(param_valor_final_periodo.valor)).value

        if param_cod_tipo_periodo.valor.upper() == SEMANAS:
            cod_semana_inicial = CodigoSemana.from_fecha(param_valor_inicial_periodo.valor).value
            cod_semana_final = CodigoSemana.from_fecha(param_valor_final_periodo.valor).value

        if param_cod_tipo_periodo.valor.upper() == MESES:
            cod_semana_inicial = CodigoSemana.from_fecha(CodigoMes(param_valor_inicial_periodo.valor).get_fecha_primer_dia()).value
            cod_semana_final = CodigoSemana.from_fecha(CodigoMes(param_valor_final_periodo.valor).get_fecha_ult_dia()).value

        if cod_semana_inicial > cod_semana_final:
            raise AppException(msg="La semana inicial debe ser menor o igual a la semana final")

        params = {
            "cod_symbol": param_cod_symbol.valor,
            "cod_semana_desde": cod_semana_inicial,
            "cod_semana_hasta": cod_semana_final
        }
        return params

    def parse_args_get_metricas_mensuales_de_cierres_positivos(self, args={}):
        self.params.set_params(args=args)

        param_cod_symbol = self.params.parse("cod_symbol", requerido=True)
        param_cod_tipo_periodo = self.params.parse("cod_tipo_periodo", requerido=True)

        param_valor_inicial_periodo = self.params.parse("fch_desde", requerido=True)
        param_valor_final_periodo = self.params.parse("fch_hasta", requerido=True)

        cod_mes_inicial = None
        cod_mes_final = None

        if param_cod_tipo_periodo.valor.upper() == DIAS:
            cod_mes_inicial = Mes.from_isoformat(param_valor_inicial_periodo.valor).codigo()
            cod_mes_final = Mes.from_isoformat(param_valor_final_periodo.valor).codigo()

        if param_cod_tipo_periodo.valor.upper() == SEMANAS:
            fch_semana_inicial = CodigoSemana(param_valor_inicial_periodo.valor).to_fecha_inicio_semana()
            cod_mes_inicial = CodigoMes.from_date(fch_semana_inicial).value

            fch_semana_final = CodigoSemana(param_valor_final_periodo.valor).to_fecha_ultdia_semana()
            cod_mes_final = CodigoMes.from_date(fch_semana_final).value

        if param_cod_tipo_periodo.valor.upper() == MESES:
            cod_mes_inicial = CodigoMes(param_valor_inicial_periodo.valor).value
            cod_mes_final = CodigoMes(param_valor_final_periodo.valor).value

        if cod_mes_inicial > cod_mes_final:
            raise AppException(msg="El mes inicial no puede ser mayor al mes final")

        params = {
            "cod_symbol": param_cod_symbol.valor,
            "cod_mes_desde": cod_mes_inicial,
            "cod_mes_hasta": cod_mes_final
        }
        return params

    def parse_args_get_metricas_mensuales_de_cierres_negativos(self, args={}):
        self.params.set_params(args=args)

        param_cod_symbol = self.params.parse("cod_symbol", requerido=True)
        param_cod_tipo_periodo = self.params.parse("cod_tipo_periodo", requerido=True)

        param_valor_inicial_periodo = self.params.parse("valor_inicial_periodo", requerido=True)
        param_valor_final_periodo = self.params.parse("valor_final_periodo", requerido=True)

        cod_mes_inicial = None
        cod_mes_final = None

        if param_cod_tipo_periodo.valor.upper() == DIAS:
            cod_mes_inicial = CodigoMes.parse_string_client(param_valor_inicial_periodo.valor).value
            cod_mes_final = CodigoMes.parse_string_client(param_valor_final_periodo.valor).value

        if param_cod_tipo_periodo.valor.upper() == SEMANAS:
            fch_semana_inicial = CodigoSemana(param_valor_inicial_periodo.valor).to_fecha_inicio_semana()
            cod_mes_inicial = CodigoMes.from_date(fch_semana_inicial).value

            fch_semana_final = CodigoSemana(param_valor_final_periodo.valor).to_fecha_ultdia_semana()
            cod_mes_final = CodigoMes.from_date(fch_semana_final).value

        if param_cod_tipo_periodo.valor.upper() == MESES:
            cod_mes_inicial = CodigoMes(param_valor_inicial_periodo.valor).value
            cod_mes_final = CodigoMes(param_valor_final_periodo.valor).value

        if cod_mes_inicial > cod_mes_final:
            raise AppException(msg="El mes inicial no puede ser mayor al mes final")

        params = {
            "cod_symbol": param_cod_symbol.valor,
            "cod_mes_desde": cod_mes_inicial,
            "cod_mes_hasta": cod_mes_final
        }
        return params



    def parse_args_get_variaciones_x_symbol(self, args={}):
        parser = BaseParser(args=args)
        params = {
            "cod_symbol": parser.get("cod_symbol", requerido=True),
            "fch_desde": parser.get("fch_desde", requerido=True, datatype=date),
            "fch_hasta": parser.get("fch_hasta", requerido=True, datatype=date)
        }
        return params

    def parse_args_get_metricas_semanal(self, args={}):
        parser = BaseParser(args=args)
        params = {
            "cod_symbol": parser.get("cod_symbol", requerido=True)
        }

        nom_semana_desde = parser.get("nom_semana_desde", requerido=True)
        num_semana_desde, num_anyo_semana_desde = tuple(nom_semana_desde.split("/"))
        params["cod_semana_desde"] = f"{num_anyo_semana_desde}{num_semana_desde}"

        nom_semana_hasta = parser.get("nom_semana_hasta", requerido=True)
        num_semana_hasta, num_anyo_semana_hasta = tuple(nom_semana_hasta.split("/"))
        params["cod_semana_hasta"] = f"{num_semana_hasta}{num_anyo_semana_hasta}"
        return params
