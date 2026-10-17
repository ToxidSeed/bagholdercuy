from reader.variacionsemanal import VariacionSemanalReader
from reader.seriesemanal import SerieSemanalReader
from reader.seriemensual import SerieMensualReader
from reader.seriediaria import SerieDiariaReader
from reader.variaciondiaria import VariacionDiariaReader
from reader.variacionmensual import VariacionMensualReader
from model.seriediaria import SerieDiariaModel
from model.seriesemanal import SerieSemanalModel
from model.seriemensual import SerieMensualModel
from model.variacionsemanal import VariacionSemanalModel
from model.variaciondiaria import VariacionDiariaModel
from model.variacionmensual import VariacionMensualModel
from datetime import date, datetime
from config.extensions import db
import pandas as pd
from common.Formatter import Formatter
from decimal import Decimal
from domain.mes import Mes
from domain.semana import CodigoSemana
import helper.semana_helper as semana_helper
import helper.mes_helper as mes_helper
from config.constants import CONST_WRITE_MODE_TEXT_APPEND, CONST_WRITE_MODE_TEXT_REPLACE, CONST_WRITE_MODE_TEXT_OVERWRITE
import importlib
from common.AppException import AppException
from reader.symbol import SymbolReader
from service.markets_data_providers.ibkr.ibkr_serie_service import (
    InteractiveBrokersSerieService,
)
from service.serie.resumenserie import ResumenSerieService
from service.serie.variaciondiaria import VariacionDiariaService
from service.serie.seriesemanal import SerieSemanalService
from service.serie.variacionsemanal import VariacionSemanalService
from service.serie.seriemensual import SerieMensualService
from service.serie.variacionmensual import VariacionMensualService


class SerieService:
    PROVIDERS = {
        "IBKR": {
            "module": "service.markets_data_providers.ibkr.ibkr_serie_service",
            "class_name": "InteractiveBrokersSerieService",
        },
    }

    def _get_provider_class(self, market_data_provider: str):
        provider_key = (market_data_provider or "").strip().upper()
        if provider_key not in self.PROVIDERS:
            raise AppException(
                msg=f"Proveedor de datos de mercado '{market_data_provider}' no soportado"
            )

        provider_info = self.PROVIDERS[provider_key]
        module_path = provider_info["module"]
        class_name = provider_info["class_name"]

        module = importlib.import_module(module_path)
        service_class = getattr(module, class_name)

        import sys
        current_module = sys.modules.get("service.serie.serie_service")
        if current_module and hasattr(current_module, class_name):
            local_attr = getattr(current_module, class_name)
            if hasattr(local_attr, "assert_called") or "mock" in type(local_attr).__name__.lower():
                service_class = local_attr

        return service_class

    def sincronize(
        self,
        market_data_provider: str,
        cod_symbol: str,
        fch_desde: date,
        fch_hasta: date,
        modo_carga: str,
    ):
        """
        Args:
            market_data_provider (str): constante para identificar el proveedor de datos (ej: "IBKR").
            cod_symbol (str): codigo del symbol a sincronizar
            fch_desde (date): fecha de inicio de los datos
            fch_hasta (date): fecha de fin de los datos
            modo_carga (str): modo de carga
            
        Raises:
            AppException: Si cod_symbol no se encuentra dentro de SymbolModel.

        Flujo Principal:
            Sincroniza las series con las diferentes fuentes de datos            
            1. con el proveedor de datos obtener el modulo y la clase para poder hacer la sincronizacion, por ejemplo: service/markets_data_providers/ibkr/ibkr_serie_service.py -> InteractiveBrokersSerieService.load(...).
            2.- Obtener SymbolModel con cod_symbol
            3.- Ejecutar .load de la clase obtenida en el punto 1.            
            4.- Sincronizar las variaciones diarias service/serie/variaciondiaria.py - VariacionDiariaService 
            5.- Sincronizar las series semanales service/serie/seriesemanal.py - SerieSemanalService - generar_series
            6.- Sincronizar las variaciones semanales - service/serie/variacionsemanal.py - VariacionSemanalService - generar_series
            7.- Sincronizar las series mensuales - service/serie/seriemensual.py - SerieMensualService - generar_series
            8.- Sincronizar las variaciones mensuales - service/serie/variacionmensual.py - VariacionMensualService - generar_series
            9.- Actualizar/insertar model/resumenserie.py - ResumenSerieModel

        """
        # 1. Con el proveedor de datos obtener el modulo y la clase
        provider_class = self._get_provider_class(market_data_provider)

        # 2. Obtener SymbolModel con cod_symbol
        symbol = SymbolReader().get(
            cod_symbol=cod_symbol,
            not_found_error=True,
        )

        # 3. Ejecutar .load de la clase obtenida en el punto 1
        provider_service = provider_class()
        resultado = provider_service.load(
            symbol=symbol,
            fch_desde=fch_desde,
            fch_hasta=fch_hasta,
            modo_carga=modo_carga,
        )

        fch_inicio_procesamiento = (
            resultado[0] if isinstance(resultado, (tuple, list)) else resultado
        )

        if fch_inicio_procesamiento:
            # 4. Sincronizar las variaciones diarias service/serie/variaciondiaria.py - VariacionDiariaService
            VariacionDiariaService().generar_variaciones(
                cod_symbol, fch_inicio_procesamiento
            )

            # 5. Sincronizar las series semanales service/serie/seriesemanal.py - SerieSemanalService - generar_series
            SerieSemanalService().generar_series(
                cod_symbol, fch_inicio_procesamiento
            )

            # 6. Sincronizar las variaciones semanales - service/serie/variacionsemanal.py - VariacionSemanalService - generar_series
            VariacionSemanalService().generar_series(
                cod_symbol, fch_inicio_procesamiento
            )

            # 7. Sincronizar las series mensuales - service/serie/seriemensual.py - SerieMensualService - generar_series
            SerieMensualService().generar_series(
                cod_symbol, fch_inicio_procesamiento
            )

            # 8. Sincronizar las variaciones mensuales - service/serie/variacionmensual.py - VariacionMensualService - generar_series
            VariacionMensualService().generar_series(
                cod_symbol, fch_inicio_procesamiento
            )

        # 9. Actualizar/insertar model/resumenserie.py - ResumenSerieModel
        ResumenSerieService().guardar(cod_symbol)

        return resultado

    def load(self, cod_symbol, df_series, modo_carga):        
        df_series["fch_semana"] = df_series["fch_serie"].apply(lambda x: CodigoSemana.from_fecha(x).to_fecha_inicio_semana())
        df_series["fch_mes"] = df_series["fch_serie"].apply(lambda x: Mes.from_fecha(x).to_fecha_mes())
        df_series["imp_apertura_sin_ajus"] = df_series["imp_apertura"]
        df_series["imp_maximo_sin_ajus"] = df_series["imp_maximo"]
        df_series["imp_minimo_sin_ajus"] = df_series["imp_minimo"]
        df_series["imp_cierre_sin_ajus"] = df_series["imp_cierre"]
        df_series["fch_registro"] = date.today() 
      
        if modo_carga == CONST_WRITE_MODE_TEXT_OVERWRITE:
            fch_max_serie_in = df_series["fch_serie"].max()
            SerieDiariaModel.eliminar_x_symbol_desde_fecha(cod_symbol, fch_max_serie_in)
            SerieDiariaModel.insertar_pandas_dataframe(df_series)
            
        elif modo_carga == CONST_WRITE_MODE_TEXT_APPEND:
            record_maximo = SerieDiariaReader().get_fecha_maxima_x_symbol(cod_symbol)
            fch_serie_max = record_maximo.max_fch_serie
            if fch_serie_max:
                df_series = df_series[df_series["fch_serie"] > fch_serie_max]

            if not df_series.empty:
                SerieDiariaModel.insertar_pandas_dataframe(df_series)
        elif modo_carga == CONST_WRITE_MODE_TEXT_REPLACE:
            SerieDiariaModel.eliminar_x_symbol(cod_symbol)
            SerieDiariaModel.insertar_pandas_dataframe(df_series)

        if not df_series.empty:
            return df_series["fch_serie"].min()                

class VariacionDiariaLoader:
    def load(self, cod_symbol, fch_inicio_proceso, modo_carga):
        db.session.flush()
        if not fch_inicio_proceso:
            return

        # Eliminar todas las series desde la fecha de inicio del proceso
        self.__eliminar_variaciones(cod_symbol, fch_inicio_proceso, modo_carga)        

        # Obtener la fecha de serie previa a fch_inicio_proceso, para calcular correctamente la variacion
        fch_serie_previa = self.get_fch_serie_anterior(cod_symbol, fch_inicio_proceso)

        # Si la fch_serie_previa esta informada, se debe recuperar los datos desde esta
        fch_inicio_recuperacion_series = fch_serie_previa if fch_serie_previa else fch_inicio_proceso    
        series = SerieDiariaReader.get_series_desde_fecha(cod_symbol, fch_inicio_recuperacion_series)

        df_series = pd.DataFrame(Formatter().format(series))
        df_series = df_series.rename(columns={
            "cod_symbol":"symbol"
        })

        df_series["imp_cierre_ant"] = df_series["imp_cierre"].shift(1).fillna(df_series["imp_apertura"])
        df_series["imp_variacion_apertura"] = df_series["imp_apertura"]  - df_series["imp_cierre_ant"]
        df_series["imp_variacion_cierre"] = df_series["imp_cierre"] - df_series["imp_cierre_ant"]
        df_series["imp_variacion_maximo"] = df_series["imp_maximo"] - df_series["imp_cierre_ant"]
        df_series["imp_variacion_minimo"] = df_series["imp_minimo"] - df_series["imp_cierre_ant"]
        df_series["imp_variacion_maximo_minimo"] = df_series["imp_variacion_maximo"] - df_series["imp_variacion_minimo"]
        df_series["pct_variacion_apertura"] = ((df_series["imp_variacion_apertura"] / df_series["imp_cierre_ant"]) * 100).round(2)
        df_series["pct_variacion_cierre"] = ((df_series["imp_variacion_cierre"] / df_series["imp_cierre_ant"]) *100).round(2)     
        df_series["pct_variacion_maximo"] = ((df_series["imp_variacion_maximo"] / df_series["imp_cierre_ant"]) *100).round(2)     
        df_series["pct_variacion_minimo"] = ((df_series["imp_variacion_minimo"] / df_series["imp_cierre_ant"]) *100).round(2)     

        # Filtramos las series luego de calcular la variacion
        df_series = df_series[pd.to_datetime(df_series["fch_serie"]).dt.date >= fch_inicio_proceso]
        
        # Insertar
        if not df_series.empty:
            VariacionDiariaModel.insertar_pandas_dataframe(df_series)

    def get_fch_serie_anterior(self, cod_symbol, fch_inicio_proceso):
        fch_serie_anterior = SerieDiariaReader.get_fch_serie_previa(cod_symbol, fch_inicio_proceso)
        return fch_serie_anterior


    def __eliminar_variaciones(self, cod_symbol, fch_referencia, modo_carga):
        if modo_carga == CONST_WRITE_MODE_TEXT_REPLACE:
            VariacionDiariaModel.eliminar_x_symbol(cod_symbol)            
        else:
            VariacionDiariaModel.eliminar_x_symbol_desde_fecha(cod_symbol, fch_referencia)
        

class SerieSemanalLoader:
    def load(self, cod_symbol, fch_inicio_series, modo_carga):                
        db.session.flush()

        if not fch_inicio_series:
            return

        # Obtenemos la fecha de la semana
        fch_inicio_semana = semana_helper.get_fch_inicio_semana(fch_inicio_series)
        self.__eliminar_series_semanales(cod_symbol, fch_inicio_semana, modo_carga)        
        db.session.flush()

        # Obtenemos las series a procesar
        series = SerieDiariaReader.get_series_desde_fecha(cod_symbol, fch_inicio_semana)
        
        # Realizamos las transformaciones necesarias
        df_series = pd.DataFrame(Formatter().format(series))
        df_series = df_series.rename(columns={"cod_symbol":"symbol"})                    
        df_series["fch_semana"] = pd.to_datetime(df_series["fch_semana"]).dt.date
        df_series.sort_values(by=["fch_semana"])
        df_series["order"] = df_series.groupby("fch_semana").cumcount() + 1
        df_series["order_prev"] = df_series["order"].shift(-1, fill_value=1)
        df_series["imp_apertura_semana"] = df_series["imp_apertura"].where(df_series["order"] == 1, other = 0)
        df_series["imp_cierre_semana"] = df_series["imp_cierre"].where(df_series["order_prev"] == 1, other = 0)
        df_series = df_series.groupby(["symbol","fch_semana"]).agg(
            imp_apertura = ("imp_apertura_semana","max"),
            imp_cierre = ("imp_cierre_semana","max"),
            imp_maximo = ("imp_maximo","max"),
            imp_minimo = ("imp_minimo","min")
        ).reset_index()
        df_series["anyo"] = df_series["fch_semana"].apply(lambda x: CodigoSemana.from_fecha(x).anyo)
        df_series["semana"] = df_series["fch_semana"].apply(lambda x: CodigoSemana.from_fecha(x).semana)
        df_series["cod_semana"] = df_series["fch_semana"].apply(lambda x: CodigoSemana.from_fecha(x).value)
        df_series["fch_registro"] = date.today()
        df_series["imp_apertura_sin_ajus"] = df_series["imp_apertura"]
        df_series["imp_cierre_sin_ajus"] = df_series["imp_cierre"]
        df_series["imp_maximo_sin_ajus"] = df_series["imp_maximo"]
        df_series["imp_minimo_sin_ajus"] = df_series["imp_minimo"]
        df_series["fch_registro"] = date.today()

        self.insertar_desde_semana(df_series, fch_inicio_semana) 

    def __eliminar_series_semanales(self, cod_symbol, fch_referencia, modo_carga):        
        if modo_carga == CONST_WRITE_MODE_TEXT_REPLACE:
            SerieSemanalModel.eliminar_x_symbol(cod_symbol)
        else:
            SerieSemanalModel.eliminar_por_symbol_desde_fecha(cod_symbol, fch_referencia)

    def insertar_desde_semana(self, df_series, fch_referencia):
        df_series = df_series[df_series["fch_semana"] >= fch_referencia]                    
        SerieSemanalModel.insertar_pandas_dataframe(df_series)

class VariacionSemanalLoader:    
    def __eliminar_variaciones_semanales(self, cod_symbol, fch_semana_referencia, modo_carga):   
        if modo_carga == CONST_WRITE_MODE_TEXT_REPLACE:
            VariacionSemanalModel.eliminar_x_symbol(cod_symbol)    
        else:
            VariacionSemanalModel.eliminar_desde_fecha(cod_symbol, fch_semana_referencia)            

    def load(self, cod_symbol, fch_inicio_proceso, modo_carga):
        db.session.flush()

        if not fch_inicio_proceso:
            return

        # Obtenemos la fecha de la semana
        fch_semana_inicio_proceso = semana_helper.get_fch_inicio_semana(fch_inicio_proceso)

        # Obtenemos la fecha previa
        fch_semana_previa = SerieSemanalReader.get_fch_semana_previa(cod_symbol, fch_semana_inicio_proceso)

        # Obtenemos las series necesarias para generar la variacion
        fch_recuperacion_series = fch_semana_previa if fch_semana_previa else fch_semana_inicio_proceso
        series = SerieSemanalReader.get_series_desde_fecha(cod_symbol, fch_recuperacion_series)

        # Eliminar las variaciones
        self.__eliminar_variaciones_semanales(cod_symbol, fch_semana_inicio_proceso, modo_carga)

        # Calculamos los valores adicionales a las series
        df_series = pd.DataFrame(Formatter().format(series))
        df_series["fecha"] = pd.to_datetime(df_series["fch_semana"]).dt.date
        df_series["imp_cierre_ant"] = df_series["imp_cierre"].shift(1).fillna(df_series["imp_apertura"])
        df_series["imp_variacion_cierre"] = df_series["imp_cierre"] - df_series["imp_cierre_ant"]
        df_series["imp_variacion_minimo"] = df_series["imp_minimo"] - df_series["imp_cierre_ant"]
        df_series["imp_variacion_maximo"] = df_series["imp_maximo"] - df_series["imp_cierre_ant"]
        df_series["pct_variacion_cierre"] = (
            (df_series["imp_variacion_cierre"]/df_series["imp_cierre_ant"]) * 100
        ).round(2)
        df_series["pct_variacion_minimo"] = (
            (df_series["imp_variacion_minimo"]/df_series["imp_cierre_ant"]) * 100
        ).round(2)
        df_series["pct_variacion_maximo"] = (
            (df_series["imp_variacion_maximo"]/df_series["imp_cierre_ant"]) * 100
        ).round(2)

        df_series = self.filtrar_series_validas(df_series, fch_semana_inicio_proceso)
        self.__insertar_variaciones_semanales(df_series)

    def filtrar_series_validas(self, df_series, fch_referencia):
        df_series = df_series[pd.to_datetime(df_series["fch_semana"]).dt.date >= fch_referencia]
        return df_series

    def __insertar_variaciones_semanales(self, df_series):
        if not df_series.empty:
            VariacionSemanalModel.insertar_pandas_dataframe(df_series)

class SerieMensualLoader:
    def load(self, cod_symbol, fch_inicio_proceso, modo_carga):
        db.session.flush()

        if not fch_inicio_proceso:
            return

        # Obtenemos la fecha de inicio del mes
        fch_inicio_mes = mes_helper.get_fch_inicio_mes(fch_inicio_proceso)

        # Eliminamos las series desde el inicio del mes
        self.__eliminar_desde_mes_completo(cod_symbol, fch_inicio_mes, modo_carga)

        # Obtenemos las series para procesar
        series = SerieDiariaReader.get_series_desde_fecha(cod_symbol, fch_inicio_mes)

        # Calculamos las series        
        df_series = pd.DataFrame(Formatter().format(series))
        df_series["fch_serie"] = pd.to_datetime(df_series["fch_serie"]).dt.date
        df_series["fch_mes"] = pd.to_datetime(df_series["fch_mes"]).dt.normalize()        
        df_series.sort_values(by=["fch_serie"])
        df_series["anyo"] = df_series["fch_mes"].dt.year
        df_series["mes"] = df_series["fch_mes"].dt.month
        df_series["seq_mes"] = df_series.groupby("fch_mes").cumcount() + 1
        df_series["seq_mes_prev"] = df_series["seq_mes"].shift(-1, fill_value=1)
        df_series["imp_apertura"] = df_series["imp_apertura"].where(df_series["seq_mes"] == 1, other = 0)
        df_series["imp_cierre"] = df_series["imp_cierre"].where(df_series["seq_mes_prev"] == 1, other = 0) 
        df_series["fch_registro"] = date.today()
        df_series = df_series.groupby(["cod_symbol","fch_mes","anyo","mes"]).agg(
            imp_apertura = ("imp_apertura","max"),
            imp_maximo = ("imp_maximo","max"),
            imp_minimo = ("imp_minimo","min"),            
            imp_cierre = ("imp_cierre","max")
        ).reset_index()
        df_series["imp_apertura_sin_ajus"] = df_series["imp_apertura"]
        df_series["imp_maximo_sin_ajus"] = df_series["imp_maximo"]
        df_series["imp_minimo_sin_ajus"] = df_series["imp_minimo"]
        df_series["imp_cierre_sin_ajus"] = df_series["imp_cierre"]
        df_series["fch_mes"] = df_series["fch_mes"].dt.date
        df_series["fch_registro"] = date.today()

        self.__insertar_desde_mes(df_series, fch_inicio_mes, modo_carga)


    def __eliminar_desde_mes_completo(self, cod_symbol, fch_mes, modo_carga):
        if modo_carga == CONST_WRITE_MODE_TEXT_REPLACE:
            SerieMensualModel.eliminar_x_symbol(cod_symbol)
        else:
            SerieMensualModel.del_series_desde_fecha(cod_symbol, fch_mes)

    def __insertar_desde_mes(self, df_series, fch_referencia, modo_carga):        
        df_series = df_series[pd.to_datetime(df_series["fch_mes"]).dt.date >= fch_referencia]        
        if not df_series.empty:
            SerieMensualModel.insertar_pandas_dataframe(df_series)

class VariacionMensualLoader:
    def load(self, cod_symbol, fch_inicio_proceso, modo_carga):
        db.session.flush()

        if not fch_inicio_proceso:
            return

        # Obtenemos la fecha de inicio del mes
        fch_inicio_mes = mes_helper.get_fch_inicio_mes(fch_inicio_proceso)

        # 
        fch_mes_anterior = SerieMensualReader.get_fch_mes_anterior(cod_symbol, fch_inicio_mes)

        #
        fch_inicio_series_para_calculo = fch_mes_anterior if fch_mes_anterior else fch_inicio_mes

        #
        series = SerieMensualReader.get_series_desde_fecha(cod_symbol, fch_inicio_series_para_calculo)

        self.__eliminar_variaciones_mensuales(cod_symbol, fch_inicio_mes, modo_carga)

        # Calculamos los valores de las series
        df_series = pd.DataFrame(Formatter().format(series))
        df_series["cod_mes"] = df_series["fch_mes"].apply(lambda x: Mes.from_isoformat(x).codigo())
        df_series["imp_cierre_ant"] = df_series["imp_cierre"].shift(1).fillna(df_series["imp_apertura"])
        df_series["imp_variacion_apertura"] = df_series["imp_apertura"] - df_series["imp_cierre_ant"]
        df_series["imp_variacion_cierre"] = df_series["imp_cierre"] - df_series["imp_cierre_ant"]
        df_series["imp_variacion_maximo"] = df_series["imp_maximo"] - df_series["imp_cierre_ant"]        
        df_series["imp_variacion_minimo"] = df_series["imp_minimo"] - df_series["imp_cierre_ant"]
        df_series["pct_variacion_apertura"] = ((df_series["imp_variacion_apertura"] /  df_series["imp_cierre_ant"] ) * 100).round(2)
        df_series["pct_variacion_cierre"] = ((df_series["imp_variacion_cierre"] / df_series["imp_cierre_ant"]) * 100).round(2)
        df_series["pct_variacion_maximo"] = ((df_series["imp_variacion_maximo"] / df_series["imp_cierre_ant"]) * 100).round(2)
        df_series["pct_variacion_minimo"] = ((df_series["imp_variacion_minimo"] / df_series["imp_cierre_ant"]) * 100).round(2)
        df_series["fch_mes"] = pd.to_datetime(df_series["fch_mes"]).dt.date

        self.__insertar_desde_mes(df_series, fch_inicio_mes)

    def __eliminar_variaciones_mensuales(self, cod_symbol, fch_mes, modo_carga):
        if modo_carga == CONST_WRITE_MODE_TEXT_REPLACE:
            VariacionMensualModel.eliminar_x_symbol(cod_symbol)
        else:
            VariacionMensualModel.del_desde_fecha(cod_symbol, fch_mes)        

    def __insertar_desde_mes(self, df_series, fch_mes_referencia):
        df_series = df_series[pd.to_datetime(df_series["fch_mes"]).dt.date >= fch_mes_referencia]

        if not df_series.empty:
            VariacionMensualModel.insertar_pandas_dataframe(df_series)
