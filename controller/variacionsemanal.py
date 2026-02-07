from controller.base import Base
from common.Response import Response
from parser.variacionsemanal import VariacionSemanalParser
from reader.calendariosemanal import CalendarioSemanalReader
from reader.variacionsemanal import VariacionSemanalReader
from datetime import date


class VariacionSemanalController(Base):

    def get_variacion_actual(self, args={}):
        parser = VariacionSemanalParser()
        params = parser.parse_args_get_variacion_actual(args=args)
        params["fch_actual"] = date.today()
        semana = CalendarioSemanalReader.get_semana_x_fecha(fch_referencia=params.get("fch_actual"))
        variacion_semanal_reader = VariacionSemanalReader()
        variacion_semanal_reader.get_variacion_x_semana(cod_symbol=params.get("cod_symbol"), cod_semana=semana.cod)

    def get_variacion_semana_actual(self, args=None):
        try:
            parser = VariacionSemanalParser()
            params = parser.parse_args_get_variacion_semana_actual(args=args)

            variacion_semanal_reader = VariacionSemanalReader()
            data = variacion_semanal_reader.get_variacion_x_semana(cod_symbol=params.get("cod_symbol"), cod_semana=params.get("cod_semana"))
            return Response().from_raw_data(rawdata=data)
        except Exception as e:
            return Response().from_exception(e)

