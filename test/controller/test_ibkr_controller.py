import pytest
from unittest.mock import patch
from flask import Flask
from controller.ibkr import init_module
from service.markets_data_providers.ibkr.ibkr_options_service import (
    IbkrOptionsService,
)
import requests


@pytest.fixture
def app():
    app = Flask("test_app")
    app.config["BAGHOLDER_APPNAME"] = "bagholdercuy"
    init_module(app, "/bagholdercuy/api/v2")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@patch.object(IbkrOptionsService, "get_expiration_months")
def test_expiration_dates_get_success(mock_get_exp, client):
    mock_get_exp.return_value = ["OCT26", "NOV26", "DEC26"]

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/expiration-dates?cod_symbol=AAPL"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"] == ["OCT26", "NOV26", "DEC26"]
    mock_get_exp.assert_called_once_with(cod_symbol="AAPL")


@patch.object(IbkrOptionsService, "get_expiration_months")
def test_expiration_dates_get_symbol_param_fallback(mock_get_exp, client):
    mock_get_exp.return_value = ["JAN27", "FEB27"]

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/contracts/expiration-dates?symbol=SPY"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"] == ["JAN27", "FEB27"]
    mock_get_exp.assert_called_once_with(cod_symbol="SPY")


@patch.object(IbkrOptionsService, "get_expiration_months")
def test_expiration_dates_post_json_success(mock_get_exp, client):
    mock_get_exp.return_value = ["OCT26"]

    response = client.post(
        "/bagholdercuy/api/v2/ibkr/expiration-dates",
        json={"cod_symbol": "AAPL"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"] == ["OCT26"]
    mock_get_exp.assert_called_once_with(cod_symbol="AAPL")


def test_expiration_dates_missing_symbol(client):
    response = client.get("/bagholdercuy/api/v2/ibkr/expiration-dates")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "El parámetro 'cod_symbol' es requerido" in data["message"]


@patch.object(IbkrOptionsService, "get_expiration_months")
def test_expiration_dates_value_error(mock_get_exp, client):
    mock_get_exp.side_effect = ValueError("Error de la API de IBKR: Timeout")

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/expiration-dates?cod_symbol=AAPL"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Error de la API de IBKR: Timeout" in data["message"]


@patch.object(IbkrOptionsService, "get_expiration_months")
def test_expiration_dates_connection_error(mock_get_exp, client):
    mock_get_exp.side_effect = requests.exceptions.ConnectionError(
        "Failed to connect to gateway"
    )

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/expiration-dates?cod_symbol=AAPL"
    )
    assert response.status_code == 502
    data = response.get_json()
    assert data["success"] is False
    assert "Error de comunicación con IBKR Gateway" in data["message"]


# =====================================================================
# Tests para IbkrStrikesController
# =====================================================================

@patch.object(IbkrOptionsService, "get_strikes")
def test_strikes_get_success(mock_get_strikes, client):
    mock_get_strikes.return_value = {
        "call": [180.0, 185.0],
        "put": [180.0, 185.0],
    }

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/strikes?cod_subyacente=AAPL&expiracion=OCT26"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"] == {
        "call": [180.0, 185.0],
        "put": [180.0, 185.0],
    }
    mock_get_strikes.assert_called_once_with(
        cod_subyacente="AAPL", expiracion="OCT26", exchange=None
    )


@patch.object(IbkrOptionsService, "get_strikes")
def test_strikes_get_alternate_route_and_params(mock_get_strikes, client):
    mock_get_strikes.return_value = {"call": [200.0], "put": [200.0]}

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/options/strikes?symbol=SPY&month=JAN25&exchange=SMART"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    mock_get_strikes.assert_called_once_with(
        cod_subyacente="SPY", expiracion="JAN25", exchange="SMART"
    )


@patch.object(IbkrOptionsService, "get_strikes")
def test_strikes_post_json_success(mock_get_strikes, client):
    mock_get_strikes.return_value = {"call": [150.0], "put": [150.0]}

    response = client.post(
        "/bagholdercuy/api/v2/ibkr/contracts/strikes",
        json={"cod_symbol": "QQQ", "expiration": "DEC26"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    mock_get_strikes.assert_called_once_with(
        cod_subyacente="QQQ", expiracion="DEC26", exchange=None
    )


def test_strikes_missing_cod_subyacente(client):
    response = client.get("/bagholdercuy/api/v2/ibkr/strikes?expiracion=OCT26")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "El parámetro 'cod_subyacente' es requerido" in data["message"]


def test_strikes_missing_expiracion(client):
    response = client.get("/bagholdercuy/api/v2/ibkr/strikes?cod_subyacente=AAPL")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "El parámetro 'expiracion' es requerido" in data["message"]


@patch.object(IbkrOptionsService, "get_strikes")
def test_strikes_value_error(mock_get_strikes, client):
    mock_get_strikes.side_effect = ValueError(
        "No se encontró el contrato para el símbolo 'UNKNOWN'"
    )

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/strikes?cod_subyacente=UNKNOWN&expiracion=OCT26"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No se encontró el contrato para el símbolo 'UNKNOWN'" in data["message"]


@patch.object(IbkrOptionsService, "get_strikes")
def test_strikes_connection_error(mock_get_strikes, client):
    mock_get_strikes.side_effect = requests.exceptions.ConnectionError(
        "Failed to connect to gateway"
    )

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/strikes?cod_subyacente=AAPL&expiracion=OCT26"
    )
    assert response.status_code == 502
    data = response.get_json()
    assert data["success"] is False
    assert "Error de comunicación con IBKR Gateway" in data["message"]


# =====================================================================
# Tests para IbkrOptionsChainController
# =====================================================================

@patch.object(IbkrOptionsService, "get_options_chain")
def test_options_chain_get_success(mock_get_chain, client):
    mock_get_chain.return_value = {
        "calls": [{"conid": 1, "strike": 150.0}],
        "puts": [{"conid": 2, "strike": 150.0}],
        "strikes": [150.0],
        "imp_underlying": 150.5,
    }

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/options-chain?cod_subyacente=AAPL&fch_expiracion=2025-01-17&num_strikes=10"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Cadena de opciones obtenida correctamente."
    assert "calls" in data["data"]
    assert "puts" in data["data"]
    mock_get_chain.assert_called_once_with(
        cod_subyacente="AAPL", fch_expiracion="2025-01-17", num_strikes=10
    )


@patch.object(IbkrOptionsService, "get_options_chain")
def test_options_chain_get_default_optional_params(mock_get_chain, client):
    mock_get_chain.return_value = {"calls": [], "puts": []}

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/options/chain?cod_subyacente=SPY"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    mock_get_chain.assert_called_once_with(
        cod_subyacente="SPY", fch_expiracion=None, num_strikes=50
    )


def test_options_chain_rejects_alias_parameters(client):
    # 'symbol' no es aceptado, solo 'cod_subyacente'
    response = client.get(
        "/bagholdercuy/api/v2/ibkr/options/chain?symbol=SPY"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "El parámetro 'cod_subyacente' es requerido" in data["message"]


def test_options_chain_missing_cod_subyacente(client):
    response = client.get("/bagholdercuy/api/v2/ibkr/options-chain")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "El parámetro 'cod_subyacente' es requerido" in data["message"]


def test_options_chain_invalid_num_strikes(client):
    response = client.get(
        "/bagholdercuy/api/v2/ibkr/options-chain?cod_subyacente=AAPL&num_strikes=not_a_number"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "El parámetro 'num_strikes' debe ser un número entero válido" in data["message"]


@patch.object(IbkrOptionsService, "get_options_chain")
def test_options_chain_value_error(mock_get_chain, client):
    mock_get_chain.side_effect = ValueError(
        "No se encontró el contrato para el símbolo 'UNKNOWN'"
    )

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/options-chain?cod_subyacente=UNKNOWN"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No se encontró el contrato para el símbolo 'UNKNOWN'" in data["message"]


@patch.object(IbkrOptionsService, "get_options_chain")
def test_options_chain_connection_error(mock_get_chain, client):
    mock_get_chain.side_effect = requests.exceptions.ConnectionError(
        "Connection refused"
    )

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/options-chain?cod_subyacente=AAPL"
    )
    assert response.status_code == 502
    data = response.get_json()
    assert data["success"] is False
    assert "Error de comunicación con IBKR Gateway" in data["message"]


@patch.object(IbkrOptionsService, "get_options_chain")
def test_options_chain_json_decode_error(mock_get_chain, client):
    import json
    mock_get_chain.side_effect = json.decoder.JSONDecodeError(
        "Expecting value", "", 0
    )

    response = client.get(
        "/bagholdercuy/api/v2/ibkr/options-chain?cod_subyacente=AAPL"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "IBKR Gateway" in data["message"]


@patch("controller.ibkr.IbkrContractService.sync_contract")
def test_contracts_sync_success(mock_sync, client):
    mock_sync.return_value = {
        "conid": 265598,
        "cod_symbol": "AAPL",
        "exchange": "SMART",
    }

    response = client.post(
        "/bagholdercuy/api/v2/ibkr/trsrv/contracts",
        json={"cod_symbol": "AAPL"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["conid"] == 265598
    assert data["data"]["cod_symbol"] == "AAPL"
    mock_sync.assert_called_once_with(cod_symbol="AAPL", exchange=None)


def test_contracts_sync_missing_params(client):
    response = client.post(
        "/bagholdercuy/api/v2/ibkr/trsrv/contracts",
        json={},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "El parámetro 'cod_symbol' o 'exchange' es requerido" in data["message"]



