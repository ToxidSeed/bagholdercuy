import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from service.ibkr_contract_map_service import IbkrContractMapService
from model.symbol import SymbolModel
from model.ibkr_contract import IbkrContractsModel
from model.ibkr_contract_map import IbkrContractMapModel
from schemas.ibkr_contract_map_schema import IbkrContractMapFilterRequest
from common.AppException import AppException


# =====================================================================
# Tests para IbkrContractMapService
# =====================================================================

@patch("config.extensions.db.session.commit")
@patch("model.ibkr_contract_map.IbkrContractMapModel.get_by_symbol_id")
@patch("config.extensions.db.session.query")
def test_step1_already_in_contract_map(mock_query, mock_get_by_sym, mock_commit):
    """
    Paso 1: Si id_symbol ya está en tb_ibkr_contract_map, retorna la relación
    sin buscar en tb_ibkr_contract ni llamar a la API de IBKR.
    """
    # Mock SymbolModel
    mock_sym = SymbolModel(id_symbol=31, symbol="AAPL", name="Apple Inc")
    sym_query = MagicMock()
    sym_query.filter.return_value.first.return_value = mock_sym

    # Mock contract query
    mock_contract = IbkrContractsModel(
        conid=265598, cod_symbol="AAPL", exchange="NMS"
    )
    contract_query = MagicMock()
    contract_query.filter.return_value.first.return_value = mock_contract

    def query_side_effect(model):
        if model is SymbolModel:
            return sym_query
        return contract_query

    mock_query.side_effect = query_side_effect

    # Mock mapping exists in tb_ibkr_contract_map
    mock_mapping = MagicMock()
    mock_mapping.id_ibkr_contract_map = 1
    mock_mapping.id_symbol = 31
    mock_mapping.id_contrato_opcion = None
    mock_mapping.conid = 265598
    mock_mapping.fch_registro = datetime(2026, 10, 22)
    mock_mapping.fch_audit = datetime(2026, 10, 22)
    mock_get_by_sym.return_value = mock_mapping

    service = IbkrContractMapService()
    with patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol") as mock_search:
        res = service.sync_symbol_mapping(id_symbol=31)
        mock_search.assert_not_called()

    assert res["id_symbol"] == 31
    assert res["conid"] == 265598
    assert res["cod_symbol"] == "AAPL"
    assert res["exchange"] == "NMS"
    mock_commit.assert_not_called()


@patch("config.extensions.db.session.commit")
@patch("model.ibkr_contract_map.IbkrContractMapModel.set_mapping")
@patch("model.ibkr_contract_map.IbkrContractMapModel.get_by_symbol_id")
@patch("config.extensions.db.session.query")
def test_step2_not_in_map_but_found_in_ibkr_contract(
    mock_query, mock_get_by_sym, mock_set_map, mock_commit
):
    """
    Paso 2: Si id_symbol no está en tb_ibkr_contract_map, pero el symbol sí existe
    en tb_ibkr_contract, inserta en tb_ibkr_contract_map y retorna.
    """
    mock_sym = SymbolModel(id_symbol=32, symbol="MSFT", name="Microsoft")
    sym_query = MagicMock()
    sym_query.filter.return_value.first.return_value = mock_sym

    mock_contract = IbkrContractsModel(
        conid=272093, cod_symbol="MSFT", exchange="NASDAQ"
    )
    contract_query = MagicMock()
    contract_query.filter.return_value.order_by.return_value.first.return_value = (
        mock_contract
    )

    def query_side_effect(model):
        if model is SymbolModel:
            return sym_query
        return contract_query

    mock_query.side_effect = query_side_effect

    # Not in tb_ibkr_contract_map
    mock_get_by_sym.return_value = None

    # Mock set_mapping
    new_map = MagicMock()
    new_map.id_ibkr_contract_map = 2
    new_map.id_symbol = 32
    new_map.id_contrato_opcion = None
    new_map.conid = 272093
    new_map.fch_registro = datetime(2026, 10, 22)
    new_map.fch_audit = datetime(2026, 10, 22)
    mock_set_map.return_value = new_map

    service = IbkrContractMapService()
    with patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol") as mock_search:
        res = service.sync_symbol_mapping(id_symbol=32)
        mock_search.assert_not_called()

    assert res["id_symbol"] == 32
    assert res["conid"] == 272093
    assert res["cod_symbol"] == "MSFT"
    assert res["exchange"] == "NASDAQ"
    mock_set_map.assert_called_once_with(conid=272093, id_symbol=32)
    mock_commit.assert_called_once()


@patch("config.extensions.db.session.add")
@patch("config.extensions.db.session.commit")
@patch("model.ibkr_contract_map.IbkrContractMapModel.set_mapping")
@patch("model.ibkr_contract_map.IbkrContractMapModel.get_by_symbol_id")
@patch("config.extensions.db.session.query")
def test_step3_not_in_contract_nor_map_calls_api_and_saves_both(
    mock_query, mock_get_by_sym, mock_set_map, mock_commit, mock_add
):
    """
    Paso 3: Si no se encuentra en tb_ibkr_contract_map ni en tb_ibkr_contract,
    consulta la API de Interactive Brokers, inserta en tb_ibkr_contract y en tb_ibkr_contract_map.
    """
    mock_sym = SymbolModel(id_symbol=33, symbol="NVDA", name="NVIDIA")
    sym_query = MagicMock()
    sym_query.filter.return_value.first.return_value = mock_sym

    # Contract not found in tb_ibkr_contract
    contract_query = MagicMock()
    contract_query.filter.return_value.order_by.return_value.first.return_value = (
        None
    )
    contract_query.filter.return_value.first.return_value = None

    def query_side_effect(model):
        if model is SymbolModel:
            return sym_query
        return contract_query

    mock_query.side_effect = query_side_effect
    mock_get_by_sym.return_value = None

    new_map = MagicMock()
    new_map.id_ibkr_contract_map = 3
    new_map.id_symbol = 33
    new_map.id_contrato_opcion = None
    new_map.conid = 4815747
    new_map.fch_registro = datetime(2026, 10, 22)
    new_map.fch_audit = datetime(2026, 10, 22)
    mock_set_map.return_value = new_map

    mock_api_data = [
        {
            "conid": 4815747,
            "symbol": "NVDA",
            "exchange": "NASDAQ",
        }
    ]

    service = IbkrContractMapService()
    with patch(
        "api.ibkr.InteractiveBrokersClient.search_contract_by_symbol",
        return_value=mock_api_data,
    ) as mock_search:
        res = service.sync_symbol_mapping(id_symbol=33)
        mock_search.assert_called_once_with(symbol="NVDA")

    assert res["id_symbol"] == 33
    assert res["conid"] == 4815747
    assert res["cod_symbol"] == "NVDA"
    assert res["exchange"] == "NASDAQ"
    mock_add.assert_called_once()
    mock_set_map.assert_called_once_with(conid=4815747, id_symbol=33)
    mock_commit.assert_called_once()


@patch("config.extensions.db.session.query")
def test_sync_symbol_not_found_raises_app_exception(mock_query):
    sym_query = MagicMock()
    sym_query.filter.return_value.first.return_value = None
    mock_query.return_value = sym_query

    service = IbkrContractMapService()
    with pytest.raises(AppException) as exc:
        service.sync_symbol_mapping(id_symbol=999999)
    assert "Símbolo con id_symbol 999999 no encontrado" in str(exc.value)


@patch("model.ibkr_contract_map.IbkrContractMapModel.get_by_symbol_id")
@patch("config.extensions.db.session.query")
def test_sync_api_no_contract_found_raises_app_exception(
    mock_query, mock_get_by_sym
):
    mock_sym = SymbolModel(id_symbol=33, symbol="XYZ", name="XYZ Corp")
    sym_query = MagicMock()
    sym_query.filter.return_value.first.return_value = mock_sym

    contract_query = MagicMock()
    contract_query.filter.return_value.order_by.return_value.first.return_value = (
        None
    )

    def query_side_effect(model):
        if model is SymbolModel:
            return sym_query
        return contract_query

    mock_query.side_effect = query_side_effect
    mock_get_by_sym.return_value = None

    service = IbkrContractMapService()
    with patch(
        "api.ibkr.InteractiveBrokersClient.search_contract_by_symbol",
        return_value=[],
    ):
        with pytest.raises(AppException) as exc:
            service.sync_symbol_mapping(id_symbol=33)
        assert "No se encontró contrato en Interactive Brokers" in str(
            exc.value
        )
