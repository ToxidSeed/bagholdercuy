import pytest
from datetime import date
from unittest.mock import MagicMock, patch
import pandas as pd

from common.AppException import AppException
from model.symbol import SymbolModel
from model.symbol_type import SymbolTypeModel
from model.symbol_type_mapping import SymbolTypeMappingModel
from model.ibkr_contract import IbkrContractsModel
from service.markets_data_providers.ibkr.ibkr_serie_service import InteractiveBrokersSerieService


@pytest.fixture
def service():
    return InteractiveBrokersSerieService()


@pytest.fixture
def mock_symbol():
    sym = SymbolModel()
    sym.id = 1
    sym.symbol = "AAPL"
    sym.id_symbol_type = 10
    return sym


def test_load_symbol_validation(service):
    with pytest.raises(AppException) as exc_info:
        service.load(None, date(2023, 1, 1), date(2023, 1, 5))
    assert "El parámetro 'symbol' es requerido" in exc_info.value.msg

    empty_sym = SymbolModel()
    empty_sym.symbol = ""
    with pytest.raises(AppException) as exc_info:
        service.load(empty_sym, date(2023, 1, 1), date(2023, 1, 5))
    assert "El parámetro 'symbol' es requerido" in exc_info.value.msg


def test_load_fechas_validation(service, mock_symbol):
    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, None, date(2023, 1, 5))
    assert "El parámetro 'fch_desde' es requerido y debe ser una instancia de date" in exc_info.value.msg

    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, "2023-01-01", date(2023, 1, 5))
    assert "El parámetro 'fch_desde' es requerido y debe ser una instancia de date" in exc_info.value.msg

    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, date(2023, 1, 1), None)
    assert "El parámetro 'fch_hasta' es requerido y debe ser una instancia de date" in exc_info.value.msg

    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, date(2023, 1, 1), "2023-01-05")
    assert "El parámetro 'fch_hasta' es requerido y debe ser una instancia de date" in exc_info.value.msg

    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, date(2023, 1, 10), date(2023, 1, 5))
    assert "no puede ser posterior a 'fch_hasta'" in exc_info.value.msg


def test_calculate_period(service):
    # 0 o 1 dias
    assert service._calculate_period(date(2023, 1, 1), date(2023, 1, 1)) == "1d"
    assert service._calculate_period(date(2023, 1, 1), date(2023, 1, 2)) == "1d"
    # <= 7 dias
    assert service._calculate_period(date(2023, 1, 1), date(2023, 1, 8)) == "1w"
    # <= 30 dias
    assert service._calculate_period(date(2023, 1, 1), date(2023, 1, 25)) == "1m"
    # <= 90 dias
    assert service._calculate_period(date(2023, 1, 1), date(2023, 3, 1)) == "3m"
    # <= 180 dias
    assert service._calculate_period(date(2023, 1, 1), date(2023, 6, 1)) == "6m"
    # <= 365 dias
    assert service._calculate_period(date(2023, 1, 1), date(2023, 11, 1)) == "1y"
    # <= 730 dias
    assert service._calculate_period(date(2023, 1, 1), date(2024, 11, 1)) == "2y"
    # <= 1095 dias
    assert service._calculate_period(date(2023, 1, 1), date(2025, 11, 1)) == "3y"
    # > 1095 dias
    assert service._calculate_period(date(2020, 1, 1), date(2025, 1, 1)) == "15y"


@patch("config.extensions.db.session")
@patch("api.ibkr.InteractiveBrokersClient.historical_market_data")
@patch("reader.seriediaria.SerieDiariaReader.get_fecha_maxima_x_symbol")
@patch("model.seriediaria.SerieDiariaModel.insertar_pandas_dataframe")
def test_load_success_existing_contract(
    mock_insert, mock_get_max, mock_hist_data, mock_session, service, mock_symbol
):
    # Mock contrato existente en BD
    mock_contract = IbkrContractsModel(conid=265598, cod_symbol="AAPL", exchange="SMART")
    mock_query = MagicMock()
    mock_query.filter.return_value.order_by.return_value.first.return_value = mock_contract
    mock_session.query.return_value = mock_query

    # Mock datos de IBKR (timestamp en ms: 1672617600000 = 2023-01-02, 1672704000000 = 2023-01-03)
    mock_hist_data.return_value = {
        "data": [
            {"t": 1672617600000, "o": 130.0, "h": 131.0, "l": 129.0, "c": 130.5},
            {"t": 1672704000000, "o": 130.5, "h": 132.0, "l": 130.0, "c": 131.5},
        ]
    }

    # Mock reader maximo (no hay maximo previo)
    mock_record = MagicMock()
    mock_record.max_fch_serie = None
    mock_get_max.return_value = mock_record

    fch_min, fch_max = service.load(
        symbol=mock_symbol,
        fch_desde=date(2023, 1, 1),
        fch_hasta=date(2023, 1, 5),
        modo_carga="APPEND",
    )

    assert fch_min == date(2023, 1, 2)
    assert fch_max == date(2023, 1, 3)
    mock_hist_data.assert_called_once_with(conid=265598, period="1w", bar="1d")
    mock_insert.assert_called_once()
    mock_session.flush.assert_called()


@patch("config.extensions.db.session")
@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
@patch("api.ibkr.InteractiveBrokersClient.historical_market_data")
@patch("model.seriediaria.SerieDiariaModel.eliminar_x_symbol_desde_fecha")
@patch("model.seriediaria.SerieDiariaModel.insertar_pandas_dataframe")
def test_load_alternative_flows_contract_resolution(
    mock_insert,
    mock_eliminar,
    mock_hist_data,
    mock_search,
    mock_session,
    service,
    mock_symbol,
):
    # 1. Contrato local no existe
    mock_query_contract = MagicMock()
    mock_query_contract.filter.return_value.order_by.return_value.first.return_value = None

    # 1.1.1 SymbolTypeModel existe
    mock_symbol_type = SymbolTypeModel(id_symbol_type=10, cod_symbol_type="STOCK")
    mock_query_sym_type = MagicMock()
    mock_query_sym_type.filter.return_value.first.return_value = mock_symbol_type

    # 1.1.2 SymbolTypeMappingModel existe
    mock_mapping = SymbolTypeMappingModel(
        id_symbol_type=10, provider_name="IBKR", provider_code="STK"
    )
    mock_query_mapping = MagicMock()
    mock_query_mapping.filter.return_value.first.return_value = mock_mapping

    def side_effect_query(model):
        if model == IbkrContractsModel:
            return mock_query_contract
        elif model == SymbolTypeModel:
            return mock_query_sym_type
        elif model == SymbolTypeMappingModel:
            return mock_query_mapping
        return MagicMock()

    mock_session.query.side_effect = side_effect_query

    # 1.2 Busqueda remota en IBKR devuelve 1 resultado
    mock_search.return_value = [
        {"conid": 99999, "symbol": "AAPL", "secType": "STK", "exchange": "NASDAQ"}
    ]

    mock_hist_data.return_value = {
        "data": [
            {"t": 1672617600000, "o": 130.0, "h": 131.0, "l": 129.0, "c": 130.5},
        ]
    }

    fch_min, fch_max = service.load(
        symbol=mock_symbol,
        fch_desde=date(2023, 1, 1),
        fch_hasta=date(2023, 1, 5),
        modo_carga="OVERWRITE",
    )

    assert fch_min == date(2023, 1, 2)
    assert fch_max == date(2023, 1, 2)
    mock_search.assert_called_once_with(symbol="AAPL", sec_type="STK")
    mock_session.add.assert_called_once()
    mock_eliminar.assert_called_once_with("AAPL", date(2023, 1, 2))
    mock_insert.assert_called_once()


@patch("config.extensions.db.session")
def test_load_symbol_type_not_found_raises(mock_session, service, mock_symbol):
    mock_query_contract = MagicMock()
    mock_query_contract.filter.return_value.order_by.return_value.first.return_value = None

    mock_query_sym_type = MagicMock()
    mock_query_sym_type.filter.return_value.first.return_value = None

    def side_effect_query(model):
        if model == IbkrContractsModel:
            return mock_query_contract
        elif model == SymbolTypeModel:
            return mock_query_sym_type
        return MagicMock()

    mock_session.query.side_effect = side_effect_query

    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, date(2023, 1, 1), date(2023, 1, 5))
    assert "No existe id_symbol_type '10' en SymbolTypeModel" in exc_info.value.msg


@patch("config.extensions.db.session")
def test_load_mapping_not_found_raises(mock_session, service, mock_symbol):
    mock_query_contract = MagicMock()
    mock_query_contract.filter.return_value.order_by.return_value.first.return_value = None

    mock_symbol_type = SymbolTypeModel(id_symbol_type=10)
    mock_query_sym_type = MagicMock()
    mock_query_sym_type.filter.return_value.first.return_value = mock_symbol_type

    mock_query_mapping = MagicMock()
    mock_query_mapping.filter.return_value.first.return_value = None

    def side_effect_query(model):
        if model == IbkrContractsModel:
            return mock_query_contract
        elif model == SymbolTypeModel:
            return mock_query_sym_type
        elif model == SymbolTypeMappingModel:
            return mock_query_mapping
        return MagicMock()

    mock_session.query.side_effect = side_effect_query

    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, date(2023, 1, 1), date(2023, 1, 5))
    assert "No existe mapeo en SymbolTypeMappingModel" in exc_info.value.msg


@patch("config.extensions.db.session")
@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
def test_load_contract_search_not_found_or_multiple_raises(
    mock_search, mock_session, service, mock_symbol
):
    mock_query_contract = MagicMock()
    mock_query_contract.filter.return_value.order_by.return_value.first.return_value = None
    mock_query_sym_type = MagicMock()
    mock_query_sym_type.filter.return_value.first.return_value = SymbolTypeModel(id_symbol_type=10)
    mock_query_mapping = MagicMock()
    mock_query_mapping.filter.return_value.first.return_value = SymbolTypeMappingModel(
        id_symbol_type=10, provider_name="IBKR", provider_code="STK"
    )

    def side_effect_query(model):
        if model == IbkrContractsModel:
            return mock_query_contract
        elif model == SymbolTypeModel:
            return mock_query_sym_type
        elif model == SymbolTypeMappingModel:
            return mock_query_mapping
        return MagicMock()

    mock_session.query.side_effect = side_effect_query

    # 1.2.1: 0 resultados
    mock_search.return_value = []
    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, date(2023, 1, 1), date(2023, 1, 5))
    assert "No se encontró el contrato en IBKR" in exc_info.value.msg

    # 1.2.2: multiples resultados
    mock_search.return_value = [
        {"conid": 111, "symbol": "AAPL", "secType": "STK"},
        {"conid": 222, "symbol": "AAPL", "secType": "STK"},
    ]
    with pytest.raises(AppException) as exc_info:
        service.load(mock_symbol, date(2023, 1, 1), date(2023, 1, 5))
    assert "Se encontraron múltiples contratos" in exc_info.value.msg


@patch("config.extensions.db.session")
@patch("api.ibkr.InteractiveBrokersClient.historical_market_data")
def test_load_empty_or_out_of_range_data_returns_none(
    mock_hist_data, mock_session, service, mock_symbol
):
    mock_contract = IbkrContractsModel(conid=265598, cod_symbol="AAPL", exchange="SMART")
    mock_query = MagicMock()
    mock_query.filter.return_value.order_by.return_value.first.return_value = mock_contract
    mock_session.query.return_value = mock_query

    # IBKR devuelve lista vacia
    mock_hist_data.return_value = {"data": []}
    assert service.load(mock_symbol, date(2023, 1, 1), date(2023, 1, 5)) == (None, None)

    # IBKR devuelve datos fuera del rango solicitado [2023-01-01, 2023-01-05]
    mock_hist_data.return_value = {
        "data": [
            {"t": 1673308800000, "o": 130.0, "h": 131.0, "l": 129.0, "c": 130.5},  # 2023-01-10
        ]
    }
    assert service.load(mock_symbol, date(2023, 1, 1), date(2023, 1, 5)) == (None, None)


@patch("config.extensions.db.session")
@patch("model.seriediaria.SerieDiariaModel.eliminar_x_symbol")
@patch("model.seriediaria.SerieDiariaModel.insertar_pandas_dataframe")
def test_save_series_replace_mode(mock_insert, mock_eliminar, mock_session, service):
    df = pd.DataFrame([{"fch_serie": date(2023, 1, 2), "imp_cierre": 100.0}])
    res_df = service._save_series("AAPL", df, modo_carga="REPLACE")
    mock_eliminar.assert_called_once_with("AAPL")
    mock_insert.assert_called_once()
    assert len(res_df) == 1


def test_save_series_invalid_mode_raises(service):
    df = pd.DataFrame([{"fch_serie": date(2023, 1, 2), "imp_cierre": 100.0}])
    with pytest.raises(AppException) as exc_info:
        service._save_series("AAPL", df, modo_carga="INVALID")
    assert "Modo de carga 'INVALID' no reconocido" in exc_info.value.msg
