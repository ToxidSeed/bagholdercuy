import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from controller.symbol_type import SymbolTypeController, init_module
from model.symbol_type import SymbolTypeModel


@pytest.fixture
def app():
    app = Flask("test_app")
    app.config["BAGHOLDER_APPNAME"] = "bagholdercuy"
    init_module(app, "/bagholdercuy/api/v2")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@patch("reader.symbol_type.SymbolTypeReader.get_list")
def test_get_symbol_types_success(mock_get_list, client):
    item1 = SymbolTypeModel(
        id_symbol_type=1,
        cod_symbol_type="STOCK",
        nom_symbol_type="Acciones",
    )
    item2 = SymbolTypeModel(
        id_symbol_type=2,
        cod_symbol_type="OPTION",
        nom_symbol_type="Opciones Financieras",
    )
    mock_get_list.return_value = [item1, item2]

    response = client.get("/bagholdercuy/api/v2/symbol-type/list")
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 2
    assert data["data"][0]["cod_symbol_type"] == "STOCK"
    assert data["data"][1]["cod_symbol_type"] == "OPTION"


@patch("reader.symbol_type.SymbolTypeReader.get_list")
def test_get_symbol_types_exception(mock_get_list, client):
    mock_get_list.side_effect = Exception("Database error")

    response = client.get("/bagholdercuy/api/v2/symbol-type/list")
    assert response.status_code == 500

    data = response.get_json()
    assert data["success"] is False
    assert "Database error" in data["message"]
