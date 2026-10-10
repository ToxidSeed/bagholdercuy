import pytest
from datetime import date
from unittest.mock import patch, MagicMock
from flask import Flask

from controller.serie_controller import SeriesSynchronizationController, init_module
from common.AppException import AppException


@pytest.fixture
def app():
    app = Flask("test_app")
    app.config["BAGHOLDER_APPNAME"] = "bagholdercuy"
    init_module(app, "/bagholdercuy/api/v2")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@patch("controller.serie_controller.db.session.commit")
@patch("controller.serie_controller.SerieService.sincronize")
def test_synchronize_controller_success(mock_sincronize, mock_commit, client):
    mock_sincronize.return_value = (date(2023, 1, 1), date(2023, 1, 5))

    payload = {
        "market_data_provider": "IBKR",
        "cod_symbol": "AAPL",
        "fch_desde": "2023-01-01",
        "fch_hasta": "2023-01-05",
        "modo_carga": "APPEND",
    }

    response = client.post("/bagholdercuy/api/v2/series/synchronize", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["cod_symbol"] == "AAPL"
    assert data["data"]["market_data_provider"] == "IBKR"
    assert data["data"]["fch_min_serie"] == "2023-01-01"
    assert data["data"]["fch_max_serie"] == "2023-01-05"

    mock_sincronize.assert_called_once_with(
        market_data_provider="IBKR",
        cod_symbol="AAPL",
        fch_desde=date(2023, 1, 1),
        fch_hasta=date(2023, 1, 5),
        modo_carga="APPEND",
    )
    mock_commit.assert_called_once()


def test_synchronize_controller_missing_params(client):
    response = client.post("/bagholdercuy/api/v2/series/synchronize", json={
        "market_data_provider": "IBKR",
        # missing cod_symbol, fch_desde, fch_hasta, modo_carga
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "cod_symbol" in data["message"]


def test_synchronize_controller_invalid_date(client):
    response = client.post("/bagholdercuy/api/v2/series/synchronize", json={
        "market_data_provider": "IBKR",
        "cod_symbol": "AAPL",
        "fch_desde": "fecha_invalida",
        "fch_hasta": "2023-01-05",
        "modo_carga": "APPEND",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Formato inválido" in data["message"]


@patch("controller.serie_controller.db.session.rollback")
@patch("controller.serie_controller.SerieService.sincronize")
def test_synchronize_controller_service_exception(mock_sincronize, mock_rollback, client):
    mock_sincronize.side_effect = AppException(msg="No se ha encontrado symbol para INVALID")

    payload = {
        "market_data_provider": "IBKR",
        "cod_symbol": "INVALID",
        "fch_desde": "2023-01-01",
        "fch_hasta": "2023-01-05",
        "modo_carga": "APPEND",
    }

    response = client.post("/bagholdercuy/api/v2/series/synchronize", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No se ha encontrado symbol para INVALID" in data["message"]
    mock_rollback.assert_called_once()


def test_synchronize_controller_rejects_legacy_aliases(client):
    # Tests that old parameter names (proveedor, symbol) are rejected when API is strict
    payload = {
        "proveedor": "IBKR",
        "symbol": "AAPL",
        "fch_desde": "2023-01-01",
        "fch_hasta": "2023-01-05",
        "modo_carga": "APPEND",
    }

    response = client.post("/bagholdercuy/api/v2/series/synchronize", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "market_data_provider" in data["message"]


def test_synchronize_controller_invalid_modo_carga(client):
    response = client.post("/bagholdercuy/api/v2/series/synchronize", json={
        "market_data_provider": "IBKR",
        "cod_symbol": "MSFT",
        "fch_desde": "2023-01-01",
        "fch_hasta": "2023-01-05",
        "modo_carga": "INVALID_MODE",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "modo_carga" in data["message"]

