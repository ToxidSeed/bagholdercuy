import pytest
from unittest.mock import patch, MagicMock
from service.markets_data_providers.ibkr.ibkr_contracts_service import (
    IbkrContractsService,
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

    service = IbkrContractsService()
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

    service = IbkrContractsService()
    with pytest.raises(
        ValueError, match="Error de la API de IBKR: Authentication failed"
    ):
        service.load_contracts(exchange="NYSE")


@patch("api.ibkr.InteractiveBrokersClient.all_conids")
def test_load_contracts_invalid_format(mock_all_conids):
    # Simula respuesta con formato incorrecto
    mock_all_conids.return_value = "invalid response string"

    service = IbkrContractsService()
    with pytest.raises(ValueError, match="Respuesta inesperada de la API de IBKR"):
        service.load_contracts(exchange="NYSE")


def test_ibkr_contracts_get_response_schema():
    from schemas.responses.ibkr import ibkr_contracts_schema
    from datetime import datetime

    contract = IbkrContractsModel(
        conid=12345,
        cod_symbol="AAPL",
        exchange="NASDAQ",
        fch_hr_registro=datetime(2026, 8, 22, 12, 0, 0),
    )

    response_data = {
        "success": True,
        "message": "Se han obtenido correctamente 1 contratos para el exchange NASDAQ.",
        "data": {
            "contracts": [contract],
            "count": 1,
            "exchange": "NASDAQ",
        },
    }

    serialized = ibkr_contracts_schema.dump(response_data["data"]["contracts"])

    assert len(serialized) == 1
    serialized_contract = serialized[0]
    assert serialized_contract["conid"] == 12345
    assert serialized_contract["cod_symbol"] == "AAPL"
    assert serialized_contract["exchange"] == "NASDAQ"
    # Marshmallow DateTime dumps to ISO format by default
    assert "2026-08-22T12:00:00" in serialized_contract["fch_hr_registro"]
