from datetime import date

import pandas as pd

from config.extensions import db
from common.AppException import AppException
from api.ibkr import InteractiveBrokersClient
from model.symbol import SymbolModel
from model.symbol_type import SymbolTypeModel
from model.symbol_type_mapping import SymbolTypeMappingModel
from model.ibkr_contract import IbkrContractsModel
from model.seriediaria import SerieDiariaModel
from reader.seriediaria import SerieDiariaReader
from helper.semana_helper import get_fch_inicio_semana
from helper.mes_helper import get_fch_inicio_mes


class InteractiveBrokersSerieService:
    PROVIDER_NAME = "IBKR"
    DEFAULT_SEC_TYPE = "STK"
    DEFAULT_PERIOD = "1y"
    DAILY_BAR = "1d"
    DEFAULT_EXCHANGE = "SMART"

    def load(
        self,
        symbol: SymbolModel,
        fch_desde: date,
        fch_hasta: date,
        modo_carga: str = "APPEND",
    ):
        """            
        Args:
            symbol: instancia de SymbolModel
            fch_desde: fecha de inicio del periodo a cargar
            fch_hasta: fecha de fin del periodo a cargar
            modo_carga: modo de carga, APPEND, OVERWRITE, REPLACE

        Returns:
            fch_min_serie: fecha minima de la serie cargada
            fch_max_serie: fecha maxima de la serie cargada

        Flujos:
            Este metodo realiza la carga de series en SerieDiariaModel
            Flujo
            1.- con el symbol dentro de SymbolModel buscar en IbkrContractsModel.            
            2.- con el contrato obtener desde la api de interactive brokers obtener las series historicas diarias, usar api/ibkr.py - InteractiveBrokersClient - historical_market_data
            3.- para calcular el period que se requiere para historical_market_data se debe validar la fecha de inicio fch_desde y la fecha de fin fch_hasta.  
            4.- insertar las series en SerieDiariaModel.

            Flujos alternativos:
            1.1.- En caso el symbol.symbol no exista en IbkrContractsModel obtener codigo del tipo de symbol de interactive brokers, para eso: SymbolModel.id_symbol_type -> SymbolTypeModel.id_symbol_type -> SymbolTypeMappingModel.provider_code filtrado por SymbolTypeMappingModel.provider_name = 'IBKR'
            
            1.1.1.- Si no existe id_symbol_type en SymbolTypeModel lanzar una excepcion.
            1.1.2.- Si no existe id_symbol_type en SymbolTypeMappingModel lanzar una excepcion.
            1.2.- buscar el contrato usando api/ibkr.py InteractiveBrokersClient search_contract_by_symbol. la busqueda debe realizarse por SymbolModel.symbol y filtrar los resultados por SymbolTypeMappingModel.provider_code. Debe devolver 1 solo resultado.
            1.2.1.- Si el contrato no es ubicado en search_contract_by_symbol lanzar una excepcion.
            1.2.2.- Si devuelve mas de 1 resultado lanzar una excepcion.
            1.3.- Con el contrato ubicado en search_contract_by_symbol registrar en IbkrContractsModel.
            1.4.- continuar en el punto 2.
            
            Retorna (fch_min_serie, fch_max_serie) de las series cargadas, o (None, None) si no hubo datos.
            No realiza commit: la transacción la confirma el llamador.
        """
        if not symbol or not getattr(symbol, "symbol", None):
            raise AppException(
                msg="El parámetro 'symbol' es requerido y debe ser una instancia de SymbolModel con el atributo 'symbol'"
            )

        # 3.- validar fechas y calcular el period requerido para historical_market_data
        self._validate_fechas(fch_desde, fch_hasta)
        period = self._calculate_period(fch_desde, fch_hasta)

        # 1.- buscar contrato en IbkrContractsModel o resolver remotamente (1.1 - 1.3)
        contract = self._get_or_create_contract(symbol)

        # 2.- obtener series historicas diarias de IBKR
        raw_bars = self._fetch_daily_bars(contract.conid, period)
        df_series = self._parse_bars(symbol.symbol, raw_bars)

        if df_series.empty:
            return None, None

        # Filtrar al rango [fch_desde, fch_hasta] solicitado
        df_series = df_series[
            (df_series["fch_serie"] >= fch_desde) & (df_series["fch_serie"] <= fch_hasta)
        ]

        if df_series.empty:
            return None, None

        # 4.- insertar las series en SerieDiariaModel según modo_carga
        df_saved = self._save_series(symbol.symbol, df_series, modo_carga=modo_carga)

        if df_saved.empty:
            return None, None

        fch_min_serie = df_saved["fch_serie"].min()
        fch_max_serie = df_saved["fch_serie"].max()

        return fch_min_serie, fch_max_serie

    # ------------------------------------------------------------------ #
    # 1. Contrato: Búsqueda y Resolución
    # ------------------------------------------------------------------ #
    def _get_or_create_contract(self, symbol: SymbolModel) -> IbkrContractsModel:
        """Obtiene el contrato local; si no existe lo resuelve en IBKR y lo registra."""
        contract = self._find_local_contract(symbol.symbol)
        if contract is not None:
            return contract

        remote_contract = self._resolve_remote_contract(symbol)
        return self._save_contract(symbol.symbol, remote_contract)

    def _find_local_contract(self, cod_symbol: str) -> IbkrContractsModel:
        """Busca el contrato en IbkrContractsModel por coincidencia exacta del símbolo."""
        return (
            db.session.query(IbkrContractsModel)
            .filter(IbkrContractsModel.cod_symbol == cod_symbol)
            .order_by(IbkrContractsModel.fch_hr_registro)
            .first()
        )

    def _resolve_remote_contract(self, symbol: SymbolModel) -> dict:
        """Obtiene el tipo mapeado y busca en IBKR garantizando un resultado único."""
        provider_code = self._get_provider_code(symbol)
        return self._search_remote_contract(symbol.symbol, provider_code)

    # ------------------------------------------------------------------ #
    # 1.1 Mapeo de Tipo de Símbolo
    # ------------------------------------------------------------------ #
    def _get_provider_code(self, symbol: SymbolModel) -> str:
        """Obtiene el código del proveedor (IBKR) correspondiente al id_symbol_type del símbolo."""
        self._validate_symbol_type_exists(symbol.id_symbol_type, symbol.symbol)
        return self._get_mapping_code(symbol.id_symbol_type, self.PROVIDER_NAME, symbol.symbol)

    def _validate_symbol_type_exists(self, id_symbol_type: int, cod_symbol: str):
        """1.1.1.- Valida que id_symbol_type exista en SymbolTypeModel."""
        if not id_symbol_type:
            raise AppException(
                msg=f"El symbol '{cod_symbol}' no tiene asignado 'id_symbol_type'"
            )

        symbol_type = (
            db.session.query(SymbolTypeModel)
            .filter(SymbolTypeModel.id_symbol_type == id_symbol_type)
            .first()
        )
        if not symbol_type:
            raise AppException(
                msg=f"No existe id_symbol_type '{id_symbol_type}' en SymbolTypeModel para el symbol '{cod_symbol}'"
            )

    def _get_mapping_code(self, id_symbol_type: int, provider_name: str, cod_symbol: str) -> str:
        """1.1.2.- Valida que exista el mapeo en SymbolTypeMappingModel y devuelve provider_code."""
        mapping = (
            db.session.query(SymbolTypeMappingModel)
            .filter(
                SymbolTypeMappingModel.id_symbol_type == id_symbol_type,
                SymbolTypeMappingModel.provider_name == provider_name,
            )
            .first()
        )
        if not mapping or not mapping.provider_code:
            raise AppException(
                msg=f"No existe mapeo en SymbolTypeMappingModel para id_symbol_type '{id_symbol_type}' y provider_name '{provider_name}' (symbol '{cod_symbol}')"
            )

        return mapping.provider_code

    # ------------------------------------------------------------------ #
    # 1.2 Búsqueda Remota de Contrato en IBKR
    # ------------------------------------------------------------------ #
    def _search_remote_contract(self, cod_symbol: str, provider_code: str) -> dict:
        """
        Busca el contrato en IBKR filtrando por symbol y provider_code.
        1.2.1.- Si no se ubica, lanza excepción.
        1.2.2.- Si devuelve más de 1 resultado, lanza excepción.
        """
        data = InteractiveBrokersClient.search_contract_by_symbol(
            symbol=cod_symbol, sec_type=provider_code
        )
        self._validate_api_response(data, expected_type=list)

        matches = self._filter_matching_contracts(data, cod_symbol, provider_code)

        if len(matches) == 0:
            raise AppException(
                msg=f"No se encontró el contrato en IBKR para el symbol '{cod_symbol}' con secType '{provider_code}'"
            )
        if len(matches) > 1:
            raise AppException(
                msg=f"Se encontraron múltiples contratos ({len(matches)}) en IBKR para el symbol '{cod_symbol}' con secType '{provider_code}'"
            )

        return matches[0]

    def _filter_matching_contracts(self, contracts: list, cod_symbol: str, provider_code: str) -> list:
        """Filtra la lista de contratos devuelta por IBKR por coincidencia de símbolo y secType."""
        return [
            item for item in contracts
            if self._contract_matches(item, cod_symbol, provider_code)
        ]

    def _contract_matches(self, item: dict, cod_symbol: str, provider_code: str) -> bool:
        """Verifica si un contrato individual coincide con el symbol y el secType esperado."""
        if not isinstance(item, dict) or not item.get("conid"):
            return False

        item_symbol = str(item.get("symbol", "")).strip().upper()
        if item_symbol != cod_symbol.strip().upper():
            return False

        sec_type = item.get("secType")
        sections = item.get("sections")

        if sec_type is not None:
            return sec_type == provider_code

        if sections is not None:
            return any(
                isinstance(s, dict) and s.get("secType") == provider_code
                for s in sections
            )

        return True

    # ------------------------------------------------------------------ #
    # 1.3 Registro de Contrato
    # ------------------------------------------------------------------ #
    def _save_contract(self, cod_symbol: str, remote_contract: dict) -> IbkrContractsModel:
        """Registra en IbkrContractsModel el contrato obtenido de IBKR."""
        exchange = self._extract_exchange(remote_contract)
        contract = IbkrContractsModel(
            conid=int(remote_contract["conid"]),
            cod_symbol=cod_symbol,
            exchange=exchange,
        )
        db.session.add(contract)
        db.session.flush()
        return contract

    def _extract_exchange(self, remote_contract: dict) -> str:
        """Extrae el exchange del contrato o retorna DEFAULT_EXCHANGE."""
        if remote_contract.get("exchange"):
            return remote_contract["exchange"]

        sections = remote_contract.get("sections") or []
        for s in sections:
            if isinstance(s, dict) and s.get("exchange"):
                return s["exchange"]

        if remote_contract.get("description"):
            return remote_contract["description"]

        return self.DEFAULT_EXCHANGE

    # ------------------------------------------------------------------ #
    # 2. Obtención de Series Históricas
    # ------------------------------------------------------------------ #
    def _fetch_daily_bars(self, conid: int, period: str) -> list:
        """Obtiene desde IBKR las barras diarias para el conid especificado."""
        data = InteractiveBrokersClient.historical_market_data(
            conid=conid, period=period, bar=self.DAILY_BAR
        )
        self._validate_api_response(data, expected_type=dict)
        return data.get("data") or []

    def _parse_bars(self, cod_symbol: str, bars: list) -> pd.DataFrame:
        """Transforma las barras de IBKR a la estructura requerida por SerieDiariaModel."""
        if not bars:
            return pd.DataFrame()

        df = pd.DataFrame(bars).rename(
            columns={
                "t": "fch_serie",
                "o": "imp_apertura",
                "h": "imp_maximo",
                "l": "imp_minimo",
                "c": "imp_cierre",
            }
        )
        df["fch_serie"] = pd.to_datetime(df["fch_serie"], unit="ms").dt.date
        df = df.drop_duplicates(subset=["fch_serie"], keep="last").sort_values("fch_serie")

        df["cod_symbol"] = cod_symbol
        df["fch_semana"] = df["fch_serie"].apply(get_fch_inicio_semana)
        df["fch_mes"] = df["fch_serie"].apply(get_fch_inicio_mes)

        # Precios sin ajuste
        df["imp_apertura_sin_ajus"] = df["imp_apertura"]
        df["imp_maximo_sin_ajus"] = df["imp_maximo"]
        df["imp_minimo_sin_ajus"] = df["imp_minimo"]
        df["imp_cierre_sin_ajus"] = df["imp_cierre"]
        df["fch_registro"] = date.today()

        columns = [c.name for c in SerieDiariaModel.__table__.columns]
        return df[[c for c in columns if c in df.columns]]

    # ------------------------------------------------------------------ #
    # 3. Cálculo de Periodo y Validación de Fechas
    # ------------------------------------------------------------------ #
    def _validate_fechas(self, fch_desde: date, fch_hasta: date):
        """Valida que fch_desde y fch_hasta sean instancias de date y que fch_desde <= fch_hasta."""
        if not fch_desde or not isinstance(fch_desde, date):
            raise AppException(
                msg="El parámetro 'fch_desde' es requerido y debe ser una instancia de date"
            )
        if not fch_hasta or not isinstance(fch_hasta, date):
            raise AppException(
                msg="El parámetro 'fch_hasta' es requerido y debe ser una instancia de date"
            )
        if fch_desde > fch_hasta:
            raise AppException(
                msg=f"La fecha de inicio 'fch_desde' ({fch_desde}) no puede ser posterior a 'fch_hasta' ({fch_hasta})"
            )

    def _calculate_period(self, fch_desde: date, fch_hasta: date) -> str:
        """
        Calcula el periodo requerido para historical_market_data a partir de fch_desde y fch_hasta.
        Soporta valores estándar de IBKR: 1d, 1w, 1m, 3m, 6m, 1y, 2y, 3y, 15y.
        """
        dias = (fch_hasta - fch_desde).days
        if dias <= 1:
            return "1d"
        elif dias <= 7:
            return "1w"
        elif dias <= 30:
            return "1m"
        elif dias <= 90:
            return "3m"
        elif dias <= 180:
            return "6m"
        elif dias <= 365:
            return "1y"
        elif dias <= 730:
            return "2y"
        elif dias <= 1095:
            return "3y"
        else:
            return "15y"

    # ------------------------------------------------------------------ #
    # 4. Persistencia de Series
    # ------------------------------------------------------------------ #
    def _save_series(
        self,
        cod_symbol: str,
        df_series: pd.DataFrame,
        modo_carga: str = "APPEND",
    ) -> pd.DataFrame:
        """Inserta las series en SerieDiariaModel según modo_carga (APPEND, OVERWRITE, REPLACE)."""
        if df_series.empty:
            return df_series

        modo = (modo_carga or "APPEND").strip().upper()

        if modo == "OVERWRITE":
            fch_min_serie = df_series["fch_serie"].min()
            SerieDiariaModel.eliminar_x_symbol_desde_fecha(cod_symbol, fch_min_serie)
            SerieDiariaModel.insertar_pandas_dataframe(df_series)
            db.session.flush()
            return df_series

        elif modo == "REPLACE":
            SerieDiariaModel.eliminar_x_symbol(cod_symbol)
            SerieDiariaModel.insertar_pandas_dataframe(df_series)
            db.session.flush()
            return df_series

        elif modo == "APPEND":
            record_maximo = SerieDiariaReader().get_fecha_maxima_x_symbol(cod_symbol)
            fch_serie_max = record_maximo.max_fch_serie if record_maximo else None
            if fch_serie_max:
                df_series = df_series[df_series["fch_serie"] > fch_serie_max]

            if not df_series.empty:
                SerieDiariaModel.insertar_pandas_dataframe(df_series)
                db.session.flush()
            return df_series

        else:
            raise AppException(
                msg=f"Modo de carga '{modo_carga}' no reconocido. Opciones válidas: APPEND, OVERWRITE, REPLACE"
            )

    # ------------------------------------------------------------------ #
    # Utilitarios
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validate_api_response(data, expected_type):
        """Valida que la respuesta de IBKR no sea un error y corresponda al tipo esperado."""
        if isinstance(data, dict) and "error" in data:
            raise AppException(msg=f"Error de la API de IBKR: {data.get('error')}")
        if not isinstance(data, expected_type):
            raise AppException(msg=f"Respuesta inesperada de la API de IBKR: {data}")