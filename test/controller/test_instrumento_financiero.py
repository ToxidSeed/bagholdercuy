import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from controller.instrumento_financiero import InstrumentoFinancieroController, init_module
from model.instrumento_financiero import InstrumentoFinancieroModel


@pytest.fixture
def app():
    app = Flask("test_app")
    app.config["BAGHOLDER_APPNAME"] = "bagholdercuy"
    init_module(app, "/bagholdercuy/api/v2")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@patch("reader.instrumento_financiero.InstrumentoFinancieroReader.get_list")
def test_get_instrumentos_financieros_success(mock_get_list, client):
    item1 = InstrumentoFinancieroModel(
        id_instrumento_financiero=1,
        cod_instrumento_financiero="STOCK",
        nom_instrumento_financiero="Acciones",
    )
    item2 = InstrumentoFinancieroModel(
        id_instrumento_financiero=2,
        cod_instrumento_financiero="OPTION",
        nom_instrumento_financiero="Opciones Financieras",
    )
    mock_get_list.return_value = [item1, item2]

    response = client.get("/bagholdercuy/api/v2/instrumento-financiero/list")
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 2
    assert data["data"][0]["cod_instrumento_financiero"] == "STOCK"
    assert data["data"][1]["cod_instrumento_financiero"] == "OPTION"


@patch("reader.instrumento_financiero.InstrumentoFinancieroReader.get_list")
def test_get_instrumentos_financieros_exception(mock_get_list, client):
    mock_get_list.side_effect = Exception("Database error")

    response = client.get("/bagholdercuy/api/v2/instrumento-financiero/list")
    assert response.status_code == 500

    data = response.get_json()
    assert data["success"] is False
    assert "Database error" in data["message"]
