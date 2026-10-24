import pytest
from unittest.mock import patch
from flask import Flask

from controller.ibkr_contract_map_controller import (
    init_module,
    IbkrContractMapController,
)
from service.ibkr_contract_map_service import IbkrContractMapService
from common.AppException import AppException


@pytest.fixture
def app():
    app = Flask("test_map_controller_app")
    app.secret_key = "test-secret"
    app.config["SECRET_KEY"] = "test-secret"
    app.config["BAGHOLDER_APPNAME"] = "bagholdercuy"
    app.config["AUTH_SECRET_KEY"] = "test-secret"

    init_module(app, "/bagholdercuy/api/v2")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# =====================================================================
# Tests para IbkrContractMapController siguiendo docs/CONTROLLER.md
# =====================================================================

@patch.object(IbkrContractMapService, "sync_symbol_mapping")
def test_sync_post_success(mock_sync, client):
    mock_sync.return_value = {
        "id_ibkr_contract_map": 1,
        "id_symbol": 31,
        "id_contrato_opcion": None,
        "conid": 265598,
        "cod_symbol": "AAPL",
        "exchange": "NMS",
        "fch_registro": "2026-10-22T05:00:00",
        "fch_audit": "2026-10-22T05:00:00",
    }

    response = client.post(
        "/bagholdercuy/api/v2/ibkr-contract-map/sync",
        json={"id_symbol": 31, "cod_symbol": "AAPL"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Contrato sincronizado y mapeado correctamente."
    assert data["data"]["id_symbol"] == 31
    assert data["data"]["conid"] == 265598
    assert data["data"]["cod_symbol"] == "AAPL"
    mock_sync.assert_called_once_with(id_symbol=31, cod_symbol="AAPL", exchange=None)


def test_sync_post_validation_error_missing_identifiers(client):
    response = client.post(
        "/bagholdercuy/api/v2/ibkr-contract-map/sync",
        json={},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Debe proporcionar al menos 'id_symbol' o 'cod_symbol'" in data["message"]
    assert len(data["errors"]) > 0


@patch.object(IbkrContractMapService, "sync_symbol_mapping")
def test_sync_post_app_exception_returns_400(mock_sync, client):
    mock_sync.side_effect = AppException(
        msg="No se encontró contrato en Interactive Brokers para 'XYZ'"
    )

    response = client.post(
        "/bagholdercuy/api/v2/ibkr-contract-map/sync",
        json={"cod_symbol": "XYZ"},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No se encontró contrato en Interactive Brokers para 'XYZ'" in data["message"]


@patch.object(IbkrContractMapService, "sync_symbol_mapping")
def test_sync_post_unexpected_error_returns_500(mock_sync, client):
    mock_sync.side_effect = RuntimeError("Database connection lost")

    response = client.post(
        "/bagholdercuy/api/v2/ibkr-contract-map/sync",
        json={"id_symbol": 31},
    )
    assert response.status_code == 500
    data = response.get_json()
    assert data["success"] is False
    assert "Error no controlado" in data["message"]


@patch.object(IbkrContractMapService, "get_by_id")
def test_get_by_id_success(mock_get_id, client):
    mock_get_id.return_value = {
        "id_ibkr_contract_map": 10,
        "id_symbol": 31,
        "id_contrato_opcion": None,
        "conid": 265598,
        "cod_symbol": "AAPL",
        "exchange": "NMS",
        "fch_registro": "2026-10-22T05:00:00",
        "fch_audit": "2026-10-22T05:00:00",
    }

    response = client.get("/bagholdercuy/api/v2/ibkr-contract-map/10")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["id_ibkr_contract_map"] == 10
    assert data["data"]["conid"] == 265598
    mock_get_id.assert_called_once_with(10)


@patch.object(IbkrContractMapService, "get_by_id")
def test_get_by_id_not_found(mock_get_id, client):
    mock_get_id.return_value = None

    response = client.get("/bagholdercuy/api/v2/ibkr-contract-map/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert "no encontrado" in data["message"]


@patch.object(IbkrContractMapService, "get_by_symbol_id")
def test_get_by_symbol_id_success(mock_get_sym, client):
    mock_get_sym.return_value = {
        "id_ibkr_contract_map": 1,
        "id_symbol": 31,
        "id_contrato_opcion": None,
        "conid": 265598,
        "cod_symbol": "AAPL",
        "exchange": "NMS",
        "fch_registro": "2026-10-22T05:00:00",
        "fch_audit": "2026-10-22T05:00:00",
    }

    response = client.get("/bagholdercuy/api/v2/ibkr-contract-map?id_symbol=31")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["id_symbol"] == 31
    assert data["data"]["conid"] == 265598


@patch.object(IbkrContractMapService, "get_mappings")
def test_get_mappings_filter_list(mock_get_mappings, client):
    mock_get_mappings.return_value = [
        {
            "id_ibkr_contract_map": 1,
            "id_symbol": 31,
            "id_contrato_opcion": None,
            "conid": 265598,
            "cod_symbol": "AAPL",
            "exchange": "NMS",
            "fch_registro": "2026-10-22T05:00:00",
            "fch_audit": "2026-10-22T05:00:00",
        }
    ]

    response = client.get("/bagholdercuy/api/v2/ibkr-contract-map?cod_symbol=AAPL")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 1
    assert data["data"][0]["cod_symbol"] == "AAPL"
