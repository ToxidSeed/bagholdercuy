import pytest
from unittest.mock import patch
from flask import Flask
from app import EntryAPI
from controller.cotizacion import CotizacionManager


@pytest.fixture
def app():
    app = Flask("test_cotizacion_app")
    app.secret_key = "test-secret"
    app.config["SECRET_KEY"] = "test-secret"
    app.config["BAGHOLDER_APPNAME"] = "bagholdercuy"
    app.config["AUTH_SECRET_KEY"] = "test-secret"
    from flask_restful import Api
    api = Api(app)
    api.add_resource(
        EntryAPI,
        "/{}/<string:module_name>/<string:class_name>/<string:method_name>".format(
            app.config["BAGHOLDER_APPNAME"]
        ),
    )
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_cotizacion_manager_success():
    manager = CotizacionManager()
    mock_quote = {
        "s": "ok",
        "symbol": ["AAPL"],
        "last": [343.46],
        "change": [1.46],
        "changepct": [0.0043],
    }
    with patch.object(manager.api, "quote", return_value=mock_quote):
        res = manager.get_cotizacion({"cod_symbol": "AAPL"})
        assert res["success"] is True
        data = res["data"]
        assert data["cod_symbol"] == "AAPL"
        assert data["imp_cierre"] == 343.46
        assert data["imp_cierre_anterior"] == 342.0
        assert data["imp_variacion"] == 1.46
        assert data["pct_variacion"] == 0.0043


def test_cotizacion_manager_api_error_handling():
    manager = CotizacionManager()
    mock_quote = {"s": "error", "errmsg": "Symbol not found"}
    with patch.object(manager.api, "quote", return_value=mock_quote):
        res = manager.get_cotizacion({"cod_symbol": "UNKNOWN"})
        assert res["success"] is True
        data = res["data"]
        assert data["cod_symbol"] == "UNKNOWN"
        assert data["imp_cierre"] is None
        assert data["imp_cierre_anterior"] is None


def test_cotizacion_endpoint_via_client(client):
    mock_quote = {
        "s": "ok",
        "symbol": ["NVDA"],
        "last": [214.13],
        "change": [-3.23],
        "changepct": [-0.0149],
    }
    with patch("api.marketdata.MarketDataAPI.quote", return_value=mock_quote):
        response = client.post(
            "/bagholdercuy/cotizacion/CotizacionManager/get_cotizacion",
            json={"cod_symbol": "NVDA"},
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["cod_symbol"] == "NVDA"
        assert json_data["data"]["imp_cierre"] == 214.13
        assert json_data["data"]["imp_cierre_anterior"] == 217.36
