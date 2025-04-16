import pandas as pd

from controller.base import Base
from parser.metrica import MetricaParser
from reader.variaciondiaria import VariacionDiariaReader
from reader.variacionsemanal import VariacionSemanalReader
from reader.variacionmensual import VariacionMensualReader


from common.Response import Response
from common.Formatter import Formatter


class MetricaController(Base):
    def get_metricas_diarias_de_cierres_positivos(self, args={}):
        parser = MetricaParser()
        params = parser.parse_args_get_metricas_diarias_de_cierres_positivos(args=args)

        reader = VariacionDiariaReader()
        df = reader.get_variaciones_x_symbol(cod_symbol=params.get("cod_symbol"), fch_desde=params.get("fch_desde"), fch_hasta=params.get("fch_hasta"), pandas=True)
        df_cierre_positivo = df[(df.imp_variacion_cierre >= 0.00)]
        df_cierre_positivo["imp_var_max_min"] = df["imp_maximo"] - df["imp_minimo"]
        df_cierre_positivo["imp_var_max_cierre"] = df["imp_cierre"] - df["imp_maximo"]

        df_stats = df_cierre_positivo.describe()
        df_stats = df_stats[(df_stats.index != 'count')]
        records = Formatter().format_pandas_dataframe(df=df_stats)

        response = Response()
        response.add_extradata("count", df_cierre_positivo.shape[0])
        response.add_extradata("total", df.shape[0])
        response.from_raw_data(rawdata=records)
        return response

    def get_metricas_diarias_de_cierres_negativos(self, args={}):
        parser = MetricaParser()
        params = parser.parse_args_get_metricas_diarias_de_cierres_negativos(args=args)
        reader = VariacionDiariaReader()
        df = reader.get_variaciones_x_symbol(cod_symbol=params.get("cod_symbol"), fch_desde=params.get("fch_desde"),
                                             fch_hasta=params.get("fch_hasta"), pandas=True)
        df_cierre_negativo = df[(df.imp_variacion_cierre < 0.00)]

        df_cierre_negativo["imp_var_min_max"] = df_cierre_negativo["imp_maximo"] - df_cierre_negativo["imp_minimo"]
        df_cierre_negativo["imp_var_min_cierre"] = df_cierre_negativo["imp_cierre"] - df_cierre_negativo["imp_minimo"]

        df_stats = df_cierre_negativo.describe()
        df_stats = df_stats[(df_stats.index != 'count')]
        records = Formatter().format_pandas_dataframe(df=df_stats)

        response = Response()
        response.add_extradata("count", df_cierre_negativo.shape[0])
        response.add_extradata("total", df.shape[0])
        response.from_raw_data(rawdata=records)
        return response

    def get_metricas_semanales_de_cierres_positivos(self, args={}):
        parser = MetricaParser()
        params = parser.parse_args_get_metricas_semanales_de_cierres_positivos(args=args)
        reader = VariacionSemanalReader()

        df = reader.get_variaciones_x_symbol(cod_symbol=params.get("cod_symbol"), cod_semana_desde=params.get("cod_semana_desde"), cod_semana_hasta=params.get("cod_semana_hasta"), pandas=True)
        df_var_positiva = df[(df.imp_variacion_cierre >= 0.00)]

        df_var_positiva["imp_var_max_min"] = df_var_positiva["imp_maximo"] - df_var_positiva["imp_minimo"]
        df_var_positiva["imp_var_max_cierre"] = df_var_positiva["imp_cierre"] - df_var_positiva["imp_maximo"]

        df_stats = df_var_positiva.describe()
        df_stats = df_stats[(df_stats.index != "count")]
        registros = Formatter().format_pandas_dataframe(df=df_stats)

        response = Response()
        response.add_extradata("count", df_var_positiva.shape[0])
        response.add_extradata("total", df.shape[0])
        response.from_raw_data(rawdata=registros)
        return response

    def get_metricas_semanales_de_cierres_negativos(self, args={}):
        parser = MetricaParser()
        params = parser.parse_args_get_metricas_semanales_de_cierres_negativos(args=args)
        reader = VariacionSemanalReader()
        df = reader.get_variaciones_x_symbol(cod_symbol=params.get("cod_symbol"),
                                             cod_semana_desde=params.get("cod_semana_desde"),
                                             cod_semana_hasta=params.get("cod_semana_hasta"), pandas=True)

        df_var = df[(df.imp_variacion_cierre < 0.00)]

        df_var["imp_var_min_max"] = df_var["imp_maximo"] - df_var["imp_minimo"]
        df_var["imp_var_min_cierre"] = df_var["imp_cierre"] - df_var["imp_minimo"]

        df_stats = df_var.describe()
        df_stats = df_stats[(df_stats.index != "count")]
        registros = Formatter().format_pandas_dataframe(df=df_stats)

        response = Response()
        response.add_extradata("count", df_var.shape[0])
        response.add_extradata("total", df.shape[0])
        response.from_raw_data(rawdata=registros)
        return response

    def get_metricas_mensuales_de_cierres_positivos(self, args={}):
        parser = MetricaParser()
        params = parser.parse_args_get_metricas_mensuales_de_cierres_positivos(args=args)

        variacion_reader = VariacionMensualReader()
        df = variacion_reader.get_variaciones_x_symbol(
            cod_symbol=params.get("cod_symbol"),
            cod_mes_desde=params.get("cod_mes_desde"),
            cod_mes_hasta=params.get("cod_mes_hasta"),
            pandas=True
        )

        df_var = df[(df.imp_variacion_cierre >= 0.00)]

        df_var["imp_var_max_min"] = df_var["imp_maximo"] - df_var["imp_minimo"]
        df_var["imp_var_max_cierre"] = df_var["imp_cierre"] - df_var["imp_maximo"]

        df_stats = df_var.describe()
        df_stats = df_stats[(df_stats.index != "count")]
        registros = Formatter().format_pandas_dataframe(df=df_stats)
        response = Response()

        total = df.shape[0]
        count = df_var.shape[0]

        response.add_extradata("count", count)
        response.add_extradata("total", total)
        response.from_raw_data(rawdata=registros)
        return response

    def get_metricas_mensuales_de_cierres_negativos(self, args={}):
        parser = MetricaParser()
        params = parser.parse_args_get_metricas_mensuales_de_cierres_positivos(args=args)

        variacion_reader = VariacionMensualReader()
        df = variacion_reader.get_variaciones_x_symbol(
            cod_symbol=params.get("cod_symbol"),
            cod_mes_desde=params.get("cod_mes_desde"),
            cod_mes_hasta=params.get("cod_mes_hasta"),
            pandas=True
        )

        df_var = df[(df.imp_variacion_cierre < 0.00)]

        df_var["imp_var_min_max"] = df_var["imp_maximo"] - df_var["imp_minimo"]
        df_var["imp_var_min_cierre"] = df_var["imp_cierre"] - df_var["imp_minimo"]

        df_stats = df_var.describe()
        df_stats = df_stats[(df_stats.index != "count")]

        count = df_var.shape[0]
        total = df.shape[0]

        row_zeros = pd.DataFrame(data={'imp_cierre_ant':[0], 'imp_apertura':[0], 'imp_maximo':[0],
                                       'imp_minimo': [0], 'imp_cierre': [0], 'imp_variacion_cierre':[0],
                                       'imp_variacion_apertura':[0], 'imp_variacion_maximo':[0],'imp_variacion_minimo':[0],
                                       'imp_var_min_max':[0], 'imp_var_min_cierre':[0]})

        df_stats.fillna(0, inplace=True)

        registros = Formatter().format_pandas_dataframe(df=df_stats)
        response = Response()

        response.add_extradata("count", count)
        response.add_extradata("total", total)
        response.from_raw_data(rawdata=registros)
        return response

    def get_variaciones_x_symbol(self, args={}):
        parser = MetricaParser()
        params = parser.parse_args_get_variaciones_x_symbol(args=args)
        reader = VariacionDiariaReader()

        df = reader.get_variaciones_x_symbol(cod_symbol=params.get("cod_symbol"), fch_desde=params.get("fch_desde"), fch_hasta=params.get("fch_hasta"), pandas=True)

        df_var_positiva = df[(df.imp_variacion_cierre >= 0.00)]
        df_stats_var_positiva = df_var_positiva.describe()
        df_stats_var_positiva = df_stats_var_positiva[(df_stats_var_positiva.index != "count")]
        registros_variacion_positiva = Formatter().format_pandas_dataframe(df=df_stats_var_positiva)

        df_var_negativa = df[(df.imp_variacion_cierre < 0.00)]
        df_stats_var_negativa = df_var_negativa.describe()
        df_stats_var_negativa = df_stats_var_negativa[(df_stats_var_negativa.index != "count")]
        registros_variacion_negativa = Formatter().format_pandas_dataframe(df=df_stats_var_negativa)

        data = {
            "cod_symbol": params.get("cod_symbol"),
            "stats_variaciones_positivas": {
                "registros": registros_variacion_positiva,
                "count": df_var_positiva.shape[0]
            },
            "stats_variaciones_negativas": {
                "registros": registros_variacion_negativa,
                "count": df_var_negativa.shape[0]
            }
        }

        return Response().from_raw_data(rawdata=data)



