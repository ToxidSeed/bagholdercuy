import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from controller.cotizacion_controller import init_module, CotizacionController
from service.cotizacion_service import CotizacionService
from service.markets_data_providers.ibkr.ibkr_cotizacion_service import (
    IbkrCotizacionService,
)
from service.markets_data_providers.base.quote_provider_base import QuoteProviderBase
from common.AppException import AppException


@pytest.fixture
def app():
    app = Flask("test_cotizacion_app")
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
# Tests para CotizacionController (RESTful v2 siguiendo docs/CONTROLLER.md)
# =====================================================================

@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.search_contract_by_symbol")
@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.marketdata_snapshot")
def test_cotizacion_controller_get_ibkr_default(mock_snapshot, mock_search, client):
    mock_search.return_value = [{"conid": 265598, "symbol": "AAPL"}]
    mock_snapshot.return_value = [
        {"conid": 265598, "31": 220.5, "7282": 218.0, "82": 2.5, "83": 1.15}
    ]

    response = client.get("/bagholdercuy/api/v2/cotizaciones?cod_symbol=AAPL")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Cotización obtenida correctamente."
    assert data["data"]["cod_symbol"] == "AAPL"
    assert data["data"]["imp_cierre"] == 220.5
    assert data["data"]["imp_cierre_anterior"] == 218.0
    assert data["data"]["imp_variacion"] == 2.5
    assert data["data"]["pct_variacion"] == 1.15
    assert data["data"]["provider"] == "ibkr"


@patch("api.marketdata.MarketDataAPI.quote")
def test_cotizacion_controller_get_explicit_marketdata_provider(mock_quote, client):
    mock_quote.return_value = {
        "s": "ok",
        "symbol": ["MSFT"],
        "last": [420.0],
        "change": [5.0],
        "changepct": [0.012],
    }

    response = client.get(
        "/bagholdercuy/api/v2/cotizaciones?cod_symbol=MSFT&provider=marketdata"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["cod_symbol"] == "MSFT"
    assert data["data"]["imp_cierre"] == 420.0
    assert data["data"]["imp_cierre_anterior"] == 415.0
    assert data["data"]["provider"] == "marketdata"


@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.search_contract_by_symbol")
@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.marketdata_snapshot")
def test_cotizacion_controller_post_success(mock_snapshot, mock_search, client):
    mock_search.return_value = [{"conid": 756733, "symbol": "SPY"}]
    mock_snapshot.return_value = [
        {"conid": 756733, "31": 580.0, "7282": 575.0, "82": 5.0, "83": 0.87}
    ]

    response = client.post(
        "/bagholdercuy/api/v2/cotizaciones",
        json={"cod_symbol": "SPY", "provider": "ibkr"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["cod_symbol"] == "SPY"
    assert data["data"]["imp_cierre"] == 580.0
    assert data["data"]["provider"] == "ibkr"


def test_cotizacion_controller_validation_error_missing_params(client):
    response = client.get("/bagholdercuy/api/v2/cotizaciones")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Debe enviar al menos uno de los parámetros" in data["message"]


def test_cotizacion_controller_unsupported_provider(client):
    response = client.get(
        "/bagholdercuy/api/v2/cotizaciones?cod_symbol=AAPL&provider=proveedor_inexistente"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "no soportado" in data["message"]


@patch.object(CotizacionService, "resolve_items_to_quote")
@patch.object(CotizacionService, "get_cotizaciones")
def test_cotizacion_controller_get_bulk_id_symbol_and_opcion(
    mock_get_cotizaciones, mock_resolve, client
):
    mock_resolve.return_value = [
        {"id_symbol": 10, "id_contrato_opcion": None, "cod_symbol": "AAPL"},
        {"id_symbol": 25, "id_contrato_opcion": None, "cod_symbol": "NVDA"},
        {
            "id_symbol": None,
            "id_contrato_opcion": 5,
            "cod_symbol": "AAPL261120C00150000",
        },
    ]
    mock_get_cotizaciones.return_value = [
        {
            "id_symbol": 10,
            "id_contrato_opcion": None,
            "cod_symbol": "AAPL",
            "imp_cierre": 230.0,
            "imp_cierre_anterior": 228.0,
            "imp_variacion": 2.0,
            "pct_variacion": 0.88,
            "provider": "ibkr",
        },
        {
            "id_symbol": 25,
            "id_contrato_opcion": None,
            "cod_symbol": "NVDA",
            "imp_cierre": 140.0,
            "imp_cierre_anterior": 138.0,
            "imp_variacion": 2.0,
            "pct_variacion": 1.45,
            "provider": "ibkr",
        },
        {
            "id_symbol": None,
            "id_contrato_opcion": 5,
            "cod_symbol": "AAPL261120C00150000",
            "imp_cierre": 15.5,
            "imp_cierre_anterior": 14.0,
            "imp_variacion": 1.5,
            "pct_variacion": 10.71,
            "provider": "ibkr",
        },
    ]

    response = client.get(
        "/bagholdercuy/api/v2/cotizaciones?id_symbol=10,25&id_contrato_opcion=5"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Cotizaciones obtenidas correctamente."
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 3

    assert data["data"][0]["id_symbol"] == 10
    assert data["data"][0]["cod_symbol"] == "AAPL"
    assert data["data"][0]["imp_cierre"] == 230.0

    assert data["data"][1]["id_symbol"] == 25
    assert data["data"][1]["cod_symbol"] == "NVDA"

    assert data["data"][2]["id_contrato_opcion"] == 5
    assert data["data"][2]["cod_symbol"] == "AAPL261120C00150000"
    assert data["data"][2]["imp_cierre"] == 15.5

    mock_resolve.assert_called_once_with(
        symbol_ids=[10, 25], contrato_ids=[5], cod_symbols=[]
    )


@patch.object(CotizacionService, "resolve_items_to_quote")
@patch.object(CotizacionService, "get_cotizaciones")
def test_cotizacion_controller_post_bulk(
    mock_get_cotizaciones, mock_resolve, client
):
    mock_resolve.return_value = [
        {"id_symbol": 1, "id_contrato_opcion": None, "cod_symbol": "SPY"},
    ]
    mock_get_cotizaciones.return_value = [
        {
            "id_symbol": 1,
            "id_contrato_opcion": None,
            "cod_symbol": "SPY",
            "imp_cierre": 585.0,
            "imp_cierre_anterior": 580.0,
            "imp_variacion": 5.0,
            "pct_variacion": 0.86,
            "provider": "ibkr",
        }
    ]

    response = client.post(
        "/bagholdercuy/api/v2/cotizaciones",
        json={"id_symbol": "1"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["data"][0]["id_symbol"] == 1
    assert data["data"][0]["imp_cierre"] == 585.0


# =====================================================================
# Tests para CotizacionService y Proveedores Dinámicos
# =====================================================================

def test_cotizacion_service_dynamic_custom_provider():
    class DummyQuoteProvider(QuoteProviderBase):
        name = "dummy"

        def get_quote(self, cod_symbol: str) -> dict:
            return {
                "cod_symbol": cod_symbol,
                "imp_cierre": 99.99,
                "imp_cierre_anterior": 98.00,
                "imp_variacion": 1.99,
                "pct_variacion": 2.03,
                "provider": self.name,
            }

    service = CotizacionService()
    service.register_provider("dummy", DummyQuoteProvider)

    res = service.get_cotizacion(cod_symbol="TEST", provider="dummy")
    assert res["cod_symbol"] == "TEST"
    assert res["imp_cierre"] == 99.99
    assert res["provider"] == "dummy"


@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.search_contract_by_symbol")
@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.marketdata_snapshot")
def test_ibkr_cotizacion_service_extracts_all_fields(mock_snapshot, mock_search):
    mock_search.return_value = [{"conid": 12345, "symbol": "GOOGL"}]
    mock_snapshot.return_value = [
        {"conid": 12345, "31": 180.25, "7282": 178.50, "82": 1.75, "83": 0.98}
    ]

    service = IbkrCotizacionService()
    quote = service.get_quote("GOOGL")

    assert quote["cod_symbol"] == "GOOGL"
    assert quote["imp_cierre"] == 180.25
    assert quote["imp_cierre_anterior"] == 178.50
    assert quote["imp_variacion"] == 1.75
    assert quote["pct_variacion"] == 0.98
    assert quote["provider"] == "ibkr"


@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.search_contract_by_symbol")
@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.marketdata_snapshot")
def test_ibkr_cotizacion_service_batch_quotes(mock_snapshot, mock_search):
    def fake_search(symbol):
        if symbol == "AAPL":
            return [{"conid": 265598, "symbol": "AAPL"}]
        elif symbol == "MSFT":
            return [{"conid": 272093, "symbol": "MSFT"}]
        return []

    mock_search.side_effect = fake_search
    mock_snapshot.return_value = [
        {"conid": 265598, "31": 225.0, "7282": 220.0, "82": 5.0, "83": 2.27},
        {"conid": 272093, "31": 420.0, "7282": 415.0, "82": 5.0, "83": 1.20},
    ]

    service = IbkrCotizacionService()
    items = [
        {"id_symbol": 101, "id_contrato_opcion": None, "cod_symbol": "AAPL"},
        {"id_symbol": 102, "id_contrato_opcion": None, "cod_symbol": "MSFT"},
    ]
    quotes = service.get_quotes(items)

    assert len(quotes) == 2
    assert quotes[0]["id_symbol"] == 101
    assert quotes[0]["cod_symbol"] == "AAPL"
    assert quotes[0]["imp_cierre"] == 225.0

    assert quotes[1]["id_symbol"] == 102
    assert quotes[1]["cod_symbol"] == "MSFT"
    assert quotes[1]["imp_cierre"] == 420.0

    mock_snapshot.assert_called_once_with(
        conids=[265598, 272093], fields=[31, 84, 86, 7282, 82, 83]
    )


@patch("model.ibkr_contract_map.IbkrContractMapModel.query")
@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.search_contract_by_symbol")
@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.marketdata_snapshot")
def test_ibkr_cotizacion_service_uses_ibkr_contract_map(
    mock_snapshot, mock_search, mock_map_query
):
    mock_map_1 = MagicMock(id_symbol=101, id_contrato_opcion=None, conid=999001)
    mock_map_2 = MagicMock(id_symbol=None, id_contrato_opcion=505, conid=999002)

    mock_filter = MagicMock()
    mock_filter.all.return_value = [mock_map_1, mock_map_2]
    mock_map_query.filter.return_value = mock_filter

    mock_snapshot.return_value = [
        {"conid": 999001, "31": 150.0, "7282": 148.0, "82": 2.0, "83": 1.35},
        {"conid": 999002, "31": 5.5, "7282": 5.0, "82": 0.5, "83": 10.0},
    ]

    service = IbkrCotizacionService()
    items = [
        {"id_symbol": 101, "id_contrato_opcion": None, "cod_symbol": "AAPL"},
        {"id_symbol": None, "id_contrato_opcion": 505, "cod_symbol": "AAPL261120C00150000"},
    ]
    quotes = service.get_quotes(items)

    assert len(quotes) == 2
    assert quotes[0]["id_symbol"] == 101
    assert quotes[0]["imp_cierre"] == 150.0
    assert quotes[1]["id_contrato_opcion"] == 505
    assert quotes[1]["imp_cierre"] == 5.5

    # No debe llamar a search_contract_by_symbol porque los conids vinieron de tb_ibkr_contract_map
    mock_search.assert_not_called()
    mock_snapshot.assert_called_once_with(
        conids=[999001, 999002], fields=[31, 84, 86, 7282, 82, 83]
    )


@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.search_contract_by_symbol")
@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.marketdata_snapshot")
def test_ibkr_cotizacion_service_raises_on_bridge_error(mock_snapshot, mock_search):
    mock_search.return_value = [{"conid": 265598, "symbol": "AAPL"}]
    mock_snapshot.return_value = {"error": "Bad Request: no bridge", "statusCode": 400}

    service = IbkrCotizacionService()
    items = [{"id_symbol": 101, "id_contrato_opcion": None, "cod_symbol": "AAPL"}]

    with pytest.raises(AppException) as exc_info:
        service.get_quotes(items)

    assert "No se pudo obtener la cotización desde el proveedor de mercado." in str(exc_info.value.msg)


@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.search_contract_by_symbol")
@patch("service.markets_data_providers.ibkr.ibkr_cotizacion_service.InteractiveBrokersClient.marketdata_snapshot")
def test_cotizacion_controller_ibkr_bridge_error_returns_400(mock_snapshot, mock_search, client):
    mock_search.return_value = [{"conid": 265598, "symbol": "AAPL"}]
    mock_snapshot.return_value = {"error": "Bad Request: no bridge", "statusCode": 400}

    response = client.get("/bagholdercuy/api/v2/cotizaciones?cod_symbol=AAPL")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No se pudo obtener la cotización desde el proveedor de mercado." in data["message"]

