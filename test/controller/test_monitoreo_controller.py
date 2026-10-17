import pytest
from unittest.mock import patch
from flask import Flask
from controller.monitoreo import init_module, MonitoreoController
from reader.monitoreo import MonitoreoReader
from manager.monitoreo import MonitoreoManager
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


# =====================================================================
# Tests para GET /monitoreos (RESTful)
# =====================================================================

@patch.object(MonitoreoReader, "get_monitoreo_activo")
def test_monitoreo_get_success(mock_get_activo, client):
    mock_get_activo.return_value = [
        {"id_monitoreo": 1, "id_symbol": 10, "id_cuenta": 1, "cod_symbol": "AAPL"}
    ]

    response = client.get("/bagholdercuy/api/v2/monitoreos?id_cuenta=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Monitoreo activo obtenido correctamente."
    assert len(data["data"]) == 1
    assert data["data"][0]["cod_symbol"] == "AAPL"
    mock_get_activo.assert_called_once_with(id_cuenta=1, opcionales={})


@patch.object(MonitoreoReader, "get_monitoreo_activo")
def test_monitoreo_get_with_sqlalchemy_row_records(mock_get_activo, client):
    class FakeRow:
        def __init__(self, d):
            self._d = d

        @property
        def __class__(self):
            class Row:
                pass
            return Row

        def _asdict(self):
            return self._d

    mock_get_activo.return_value = [
        FakeRow({"id_monitoreo": 6, "id_symbol": 41827, "id_cuenta": 3, "cod_symbol": "NVDA"})
    ]

    response = client.get("/bagholdercuy/api/v2/monitoreos?id_cuenta=3")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"][0]["cod_symbol"] == "NVDA"



@patch.object(MonitoreoReader, "get_monitoreo_activo")
def test_monitoreo_get_with_optional_params(mock_get_activo, client):
    mock_get_activo.return_value = []

    response = client.get("/bagholdercuy/api/v2/monitoreos?id_cuenta=1&id_symbol=10")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    mock_get_activo.assert_called_once_with(id_cuenta=1, opcionales={"id_symbol": 10})


def test_monitoreo_get_missing_id_cuenta(client):
    response = client.get("/bagholdercuy/api/v2/monitoreos")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "id_cuenta" in data["message"]


def test_monitoreo_singular_not_found(client):
    # Ya no existe ruta en singular por compatibilidad
    response = client.get("/bagholdercuy/api/v2/monitoreo?id_cuenta=1")
    assert response.status_code == 404


# =====================================================================
# Tests para POST /monitoreos (RESTful)
# =====================================================================

@patch("controller.monitoreo.db.session.commit")
@patch.object(MonitoreoManager, "registrar")
def test_monitoreo_post_success(mock_registrar, mock_commit, client):
    def fake_registrar(monitoreo_nuevo):
        monitoreo_nuevo.id_monitoreo = 42
        return monitoreo_nuevo

    mock_registrar.side_effect = fake_registrar

    response = client.post(
        "/bagholdercuy/api/v2/monitoreos",
        json={"id_cuenta": 1, "id_symbol": 10},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Se ha registrado el monitoreo correctamente."
    assert data["data"]["id_monitoreo"] == 42
    assert data["data"]["id_symbol"] == 10
    assert data["data"]["id_cuenta"] == 1
    mock_commit.assert_called_once()


def test_monitoreo_post_missing_required_params(client):
    response = client.post(
        "/bagholdercuy/api/v2/monitoreos",
        json={"id_cuenta": 1},  # falta id_symbol
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "id_symbol" in data["message"]


@patch("controller.monitoreo.db.session.rollback")
@patch.object(MonitoreoManager, "registrar")
def test_monitoreo_post_manager_app_exception(mock_registrar, mock_rollback, client):
    mock_registrar.side_effect = AppException(msg="El monitoreo ya existe")

    response = client.post(
        "/bagholdercuy/api/v2/monitoreos",
        json={"id_cuenta": 1, "id_symbol": 10},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "El monitoreo ya existe"
    mock_rollback.assert_called_once()
