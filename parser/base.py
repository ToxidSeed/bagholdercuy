from common.AppException import AppException

from datetime import datetime, date
from app import app


class Param:
    def __init__(self, nombre=None, valor=None, label=None, datatype=None):
        self.nombre = nombre
        self.valor = valor
        self.label = label
        self.datatype = datatype


class Params:
    def __init__(self, args=None):
        self.args = args
        self.parsed_params = {}

    def set_params(self, args=None):
        self.args = args

    def add_parsed_param(self, param:Param):
        self.parsed_params[param.nombre] = param

    def get_valores(self, lista_campos):
        params = {}
        for campo in lista_campos:
            params[campo] = self.parsed_params[campo].valor
        return params


    @staticmethod
    def parse_id_cuenta(id_cuenta):
        if id_cuenta in [None, ""]:
            return None

        return int(id_cuenta)

    @staticmethod
    def parse_date(fecha):
        if fecha in [None, ""]:
            return None

        return date.fromisoformat(fecha)

    @staticmethod
    def parse_int(param):
        if param in [None, ""]:
            return None

        return int(param)

    @staticmethod
    def parse_boolean(param):
        if param in [None, "", "false", "False", False, 0, "0"]:
            return False
        else:
            return True

    @staticmethod
    def parse_orden_resultados(param):
        if param in [None, ""]:
            return None

        if param not in ["asc", "desc"]:
            raise AppException(msg="orden_resultados solo puede ser asc o desc")

    def parse(self, nombre_param, requerido=False, datatype=None, vacio_es_nulo=False):

        valor = self.args.get(nombre_param)
        if requerido is True:
            if valor in [None, ""]:
                raise AppException(msg=f"No se ha enviado {nombre_param}")

        valor = None if vacio_es_nulo is True and valor == '' else valor

        if datatype is not None:
            if datatype == int:
                param = Param(
                    nombre=nombre_param,
                    valor=self.parse_int(valor),
                    datatype=datatype
                )
                self.add_parsed_param(param)
                return param

            if datatype == float:
                valor = None if valor in [None, ""] else float(valor)

                param = Param(
                    nombre=nombre_param,
                    valor=valor,
                    datatype=datatype
                )
                self.add_parsed_param(param)
                return param

            if datatype == date:
                valor = None if valor in [None, ""] else date.fromisoformat(valor)

                param = Param(
                    nombre=nombre_param,
                    valor=valor,
                    datatype=datatype
                )
                self.add_parsed_param(param)
                return param

        param = Param(
            nombre=nombre_param,
            valor=valor
        )
        self.add_parsed_param(param)
        return param


class BaseParser:
    def __init__(self, args=None):
        if args is None:
            args = {}
        self.args = args
        self.params = Params(args=args)

    def convert_semana_a_fecha(self, cod_semana):
        #cod_semana yyyysem
        anyo = cod_semana[0:4]
        semana = cod_semana[4:6]

        fecha = datetime.fromisocalendar(anyo, semana, 1)
        return fecha

    def convert_mes_a_fecha(self, cod_mes):
        anyo = cod_mes[0:4]
        mes = cod_mes[4:6]
        fecha = date(anyo, mes, 1)
        return fecha

    def parse_fecha_cliente(self, fecha):
        return datetime.strptime(fecha, app.config["CLIENT_DATE_FORMAT"])

    def convert_fecha_a_semana(self, fecha: date):
        anyo, semana, dia = fecha.isocalendar()
        return f"{anyo}{str(semana).zfill(2)}"

    def convert_cod_mes_a_cod_semana(self, fecha: date):
        return f"{fecha.year}{str(fecha.month).zfill(2)}"

    @staticmethod
    def parse_id_cuenta(id_cuenta):
        if id_cuenta in [None, ""]:
            return None

        return int(id_cuenta)

    @staticmethod
    def parse_date(fecha):
        if fecha in [None,""]:
            return None

        return date.fromisoformat(fecha)

    @staticmethod
    def parse_int(param):
        if param in [None,""]:
            return None

        return int(param)
    
    @staticmethod
    def parse_boolean(param):
        if param in [None, "", "false", "False", False, 0, "0"]:
            return False
        else:
            return True
    
    @staticmethod
    def parse_orden_resultados(param):
        if param in [None,""]:
            return None
        
        if param not in ["asc","desc"]:
            raise AppException(msg="orden_resultados solo puede ser asc o desc")
        
    def get(self, nombre_param, requerido=False, datatype=None, vacio_es_nulo=False):

        valor = self.args.get(nombre_param)
        if requerido is True:            
            if valor in [None,""]:
                raise AppException(msg=f"No se ha enviado {nombre_param}")                    
            
        valor = None if vacio_es_nulo is True and valor == '' else valor
        
        if datatype is not None:
            if datatype == int:
                return self.parse_int(valor)
            
            if datatype == float:
                return float(valor)

            if datatype == date:
                fecha = datetime.strptime(valor, app.config["CLIENT_DATE_FORMAT"])
                return fecha

        return valor
