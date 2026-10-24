import pytest
from unittest.mock import patch, MagicMock
from service.markets_data_providers.ibkr.ibkr_contract_service import (
    IbkrContractService,
)
from model.ibkr_contract import IbkrContractsModel

@patch("api.ibkr.InteractiveBrokersClient.all_conids")
@patch("config.extensions.db.session.query")
@patch("config.extensions.db.session.add")
@patch("config.extensions.db.session.commit")
def test_load_contracts_success(mock_commit, mock_add, mock_query, mock_all_conids):
    # Setup mock data from IBKR Gateway
    mock_all_conids.return_value = [
        {"conid": 12345, "ticker": "AAPL", "exchange": "NASDAQ"},
        {"conid": 67890, "ticker": "MSFT", "exchange": "NASDAQ"},
        {"conid": 11111, "ticker": "GOOG", "exchange": "NASDAQ"},
    ]

    # Mock DB query to say conid 12345 already exists, but others do not
    mock_query_result = MagicMock()
    mock_query.return_value = mock_query_result
    mock_query_result.filter.return_value = mock_query_result
    
    # Simula que ya existe conid 12345 en la BD
    mock_query_result.all.return_value = [(12345,)]

    service = IbkrContractService()
    inserted_count = service.load_contracts(exchange="NASDAQ")

    # Debería haber insertado sólo 67890 y 11111 (2 contratos)
    assert inserted_count == 2
    assert mock_add.call_count == 2
    mock_commit.assert_called_once()

    # Comprobar los argumentos con los que fue llamado db.session.add
    added_objects = [call[0][0] for call in mock_add.call_args_list]
    conids_added = {obj.conid for obj in added_objects}
    assert conids_added == {67890, 11111}

@patch("api.ibkr.InteractiveBrokersClient.all_conids")
def test_load_contracts_api_error(mock_all_conids):
    # Simula un error devuelto por la API de IBKR en un diccionario
    mock_all_conids.return_value = {"error": "Authentication failed"}

    service = IbkrContractService()
    with pytest.raises(ValueError, match="Error de la API de IBKR: Authentication failed"):
        service.load_contracts(exchange="NYSE")

@patch("api.ibkr.InteractiveBrokersClient.all_conids")
def test_load_contracts_invalid_format(mock_all_conids):
    # Simula respuesta con formato incorrecto
    mock_all_conids.return_value = "invalid response string"

    service = IbkrContractService()
    with pytest.raises(ValueError, match="Respuesta inesperada de la API de IBKR"):
        service.load_contracts(exchange="NYSE")


@patch("config.extensions.db.session.query")
def test_sync_contract_existing_in_db(mock_query):
    mock_contract = MagicMock(spec=IbkrContractsModel)
    mock_contract.conid = 265598
    mock_contract.cod_symbol = "AAPL"
    mock_contract.exchange = "SMART"
    mock_contract.fch_hr_registro = None

    mock_q = MagicMock()
    mock_query.return_value = mock_q
    mock_q.filter.return_value = mock_q
    mock_q.order_by.return_value = mock_q
    mock_q.first.return_value = mock_contract

    service = IbkrContractService()
    res = service.sync_contract(cod_symbol="AAPL")

    assert res["conid"] == 265598
    assert res["cod_symbol"] == "AAPL"
    assert res["exchange"] == "SMART"


@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
@patch("config.extensions.db.session.query")
@patch("config.extensions.db.session.add")
@patch("config.extensions.db.session.commit")
def test_sync_contract_fetch_from_ibkr(mock_commit, mock_add, mock_query, mock_search):
    # En BD no existe inicialmente
    mock_q = MagicMock()
    mock_query.return_value = mock_q
    mock_q.filter.return_value = mock_q
    mock_q.order_by.return_value = mock_q
    mock_q.first.return_value = None

    # IBKR API retorna contrato para NVDA
    mock_search.return_value = [
        {
            "conid": 4815747,
            "symbol": "NVDA",
            "exchange": "NASDAQ",
            "sections": [{"secType": "STK", "exchange": "SMART"}],
        }
    ]

    service = IbkrContractService()
    res = service.sync_contract(cod_symbol="NVDA")

    assert res["conid"] == 4815747
    assert res["cod_symbol"] == "NVDA"
    assert res["exchange"] == "NASDAQ"
    mock_search.assert_called_once_with(symbol="NVDA")
    mock_add.assert_called_once()
    mock_commit.assert_called_once()


@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
@patch("config.extensions.db.session.query")
def test_sync_contract_not_found_in_ibkr(mock_query, mock_search):
    mock_q = MagicMock()
    mock_query.return_value = mock_q
    mock_q.filter.return_value = mock_q
    mock_q.order_by.return_value = mock_q
    mock_q.first.return_value = None

    mock_search.return_value = []

    service = IbkrContractService()
    with pytest.raises(Exception, match="No se encontró contrato en Interactive Brokers"):
        service.sync_contract(cod_symbol="UNKNOWN")

