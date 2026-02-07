from controller.base import Base
from reader.variaciondiaria import VariacionDiariaReader
from common.Response import Response
from dataclasses import dataclass, asdict
from collections import namedtuple, defaultdict
import pandas as pd
import numpy as np
from common.Formatter import Formatter
from schemas.ciclo_schema import CicloGetCiclosDiarios, CicloVariacionGetCiclosDiarios

CicloResponse = namedtuple("CicloResponse",["num_ciclo","flg_ciclo_positivo","num_series"])    


class CicloController(Base):
    def get_ciclos_diarios(self, args):
        params = CicloGetCiclosDiarios(**args)
        cod_symbol = args.get("cod_symbol")
        fch_desde = args.get("fch_desde")
        fch_hasta = args.get("fch_hasta")

        var_reader = VariacionDiariaReader()
        records = var_reader.get_variaciones_x_symbol(cod_symbol, fch_desde, fch_hasta)        
        ciclos = self.get_ciclos(records)
        ciclos_total, ciclos_pos, ciclos_neg = self.get_resumen_ciclos(ciclos)

        stats_pos = Formatter().format_pandas_dataframe(self.get_stats(ciclos_pos))
        stats_neg = Formatter().format_pandas_dataframe(self.get_stats(ciclos_neg))

        raw_resp = {
            "ciclos":ciclos_total,
            "ciclos_pos": ciclos_pos,
            "ciclos_neg": ciclos_neg,
            "stats_pos": stats_pos,
            "stats_neg": stats_neg
        }

        response = Response()
        response.from_raw_data(raw_resp)
        return response

    def get_stats(self, ciclos):
        df = pd.DataFrame(ciclos)
        df_stats = df.describe()
        df_stats['num_series'] = round(df_stats['num_series'],3)
        return df_stats

    def get_ciclos(self, variaciones):
        num_ciclo = 0
        ciclos = []
        flg_var_positiva_ant = None
        for variacion in variaciones:
            flg_var_positiva = True if variacion.imp_variacion_cierre >= 0 else False
            num_ciclo = num_ciclo + 1 if flg_var_positiva != flg_var_positiva_ant else num_ciclo
            cod_ciclo = f"c{num_ciclo}"
            ciclos.append((variacion, cod_ciclo, flg_var_positiva))
            flg_var_positiva_ant = flg_var_positiva

        return ciclos

    def get_resumen_ciclos(self, ciclos):
        ciclos_agrupados = defaultdict(int)
        for ciclo in ciclos:
            variacion, num_ciclo, flg_ciclo_positivo = ciclo
            key = (num_ciclo, flg_ciclo_positivo)
            ciclos_agrupados[key] += 1
        
        resumen_ciclos_positivos = []
        resumen_ciclos_negativos = []
        ciclos = []
        for key, num_series in ciclos_agrupados.items():
            num_ciclo, flg_ciclo_positivo = key
            ciclos.append(CicloResponse(num_ciclo, flg_ciclo_positivo, num_series))
            if flg_ciclo_positivo == True:
                resumen_ciclos_positivos.append(CicloResponse(num_ciclo, flg_ciclo_positivo, num_series))
            else:
                resumen_ciclos_negativos.append(CicloResponse(num_ciclo, flg_ciclo_positivo, num_series))

        return ciclos, resumen_ciclos_positivos, resumen_ciclos_negativos
    
class CicloVariacionController(Base):
    def get_ciclos_diarios(self, args):
        params = CicloVariacionGetCiclosDiarios(**args)
        cod_symbol = args.get("cod_symbol")
        fch_desde = args.get("fch_desde")
        fch_hasta = args.get("fch_hasta")

        var_reader = VariacionDiariaReader()
        records = var_reader.get_variaciones_x_symbol(cod_symbol, fch_desde, fch_hasta)
        variaciones = Formatter().format(records)
        df = pd.DataFrame(variaciones)        
        df['fch_serie'] = pd.to_datetime(df['fch_serie'], format='%Y-%m-%d')
        df = df.sort_values(by='fch_serie', ascending=True)
        df['flg_ciclo_positivo'] = np.where(df['imp_variacion_cierre'] >= 0, 1, 0)
        df['prev'] = df['flg_ciclo_positivo'].shift(1)
        df['flg_primer_dia_ciclo'] = np.where(df['flg_ciclo_positivo'] != df['prev'], 1, 0)
        df['num_ciclo'] = df['flg_primer_dia_ciclo'].cumsum()

        df_first = df.groupby('num_ciclo').first().reset_index()
        df_first = df_first[['fch_serie','imp_cierre_ant','flg_ciclo_positivo','num_ciclo']]

        df_last = df.groupby('num_ciclo').last().reset_index()
        df_last = df_last[['fch_serie','imp_cierre','flg_ciclo_positivo','num_ciclo']]

        df_result = df_first.join(df_last, how='inner', lsuffix='_first', rsuffix='_last')
        df_result['imp_var_ciclo'] = round(df_result['imp_cierre'] - df_result['imp_cierre_ant'],2)
        df_result['pct_var_ciclo'] = round(((df_result['imp_cierre'] - df_result['imp_cierre_ant'])/df_result['imp_cierre_ant'])*100,2)
        
        df_result = df_result.rename(columns={
            'fch_serie_first':'fch_serie',
            'flg_ciclo_positivo_first':'flg_ciclo_positivo',
            'num_ciclo_first':'num_ciclo',            
        })
        df_result = df_result[['flg_ciclo_positivo','num_ciclo','imp_var_ciclo','pct_var_ciclo']]
        df_ciclos_positivos = Formatter().format_pandas_dataframe(df_result[df_result['flg_ciclo_positivo']== 1])
        df_ciclos_negativos = Formatter().format_pandas_dataframe(df_result[df_result['flg_ciclo_positivo']== 0])

        resp = {
            'df_ciclos_positivos': df_ciclos_positivos,
            'df_ciclos_negativos': df_ciclos_negativos
        }

        response = Response()
        response.from_raw_data(resp)
        return response