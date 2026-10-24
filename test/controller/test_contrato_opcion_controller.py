import pytest
from datetime import date, datetime
from unittest.mock import patch, MagicMock
from flask import Flask

from controller.contrato_opcion_controller import (
    init_module,
    ContratoOpcionController,
    ContratoOpcionChainController,
)
from model.contrato_opcion import ContratoOpcionModel
from model.symbol import SymbolModel
from common.AppException import AppException


@pytest.fixture
def app():
    app = Flask("test_contrato_opcion_app")
    app.secret_key = "test-secret"
    app.config["SECRET_KEY"] = "test-secret"
    app.config["BAGHOLDER_APPNAME"] = "bagholdercuy"
    app.config["AUTH_SECRET_KEY"] = "test-secret"

    init_module(app, "/bagholdercuy/api/v2")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def _crear_mock_contrato(
    id_contrato=1,
    cod_symbol="AAPL261120C00150000",
    tipo="CALL",
    subyacente="AAPL",
    strike=150.0,
    vencimiento=date(2026, 11, 20),
):
    contrato = MagicMock(spec=ContratoOpcionModel)
    contrato.id_contrato_opcion = id_contrato
    contrato.id_symbol_subyacente = 10
    contrato.cod_symbol = cod_symbol
    contrato.cod_symbol_subyacente = subyacente
    contrato.tipo_opcion = tipo
    contrato.fch_vencimiento = vencimiento
    contrato.imp_strike = strike
    contrato.tam_contrato = 100
    contrato.cod_moneda = "USD"
    contrato.descripcion = "Apple Call"
    contrato.fch_registro = datetime(2026, 1, 1, 10, 0, 0)
    contrato.fch_audit = datetime(2026, 1, 1, 10, 0, 0)
    return contrato


# =============================================================================
# Tests de Listado y Búsqueda (GET /contratos-opcion)
# =============================================================================

@patch("service.contrato_opcion_service.ContratoOpcionReader.get_contratos")
def test_get_contratos_list_success(mock_get_contratos, client):
    mock_get_contratos.return_value = [
        _crear_mock_contrato(1, "AAPL261120C00150000", "CALL", "AAPL", 150.0),
        _crear_mock_contrato(2, "AAPL261120P00150000", "PUT", "AAPL", 150.0),
    ]

    response = client.get("/bagholdercuy/api/v2/contratos-opcion?cod_symbol=AAPL&sentidos=CALL,PUT")
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Contratos de opciones obtenidos correctamente."
    assert len(data["data"]) == 2
    assert data["data"][0]["cod_symbol"] == "AAPL261120C00150000"
    assert data["data"][0]["symbol"] == "AAPL261120C00150000"
    assert data["data"][0]["id"] == 1
    assert data["data"][0]["moneda_id"] == "USD"
    assert data["data"][0]["tipo_opcion"] == "CALL"
    assert data["data"][0]["side"] == "CALL"
    assert data["data"][0]["underlying"] == "AAPL"
    assert data["data"][0]["strike"] == 150.0


@patch("service.contrato_opcion_service.ContratoOpcionReader.get_contratos")
def test_get_contratos_with_empty_query_params_success(mock_get_contratos, client):
    mock_get_contratos.return_value = [
        _crear_mock_contrato(1, "SPX261022C07735000", "CALL", "SPX", 7735.0),
    ]

    response = client.get(
        "/bagholdercuy/api/v2/contratos-opcion?id_contrato_opcion=&cod_symbol=&fch_expiracion=&imp_ejercicio="
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["symbol"] == "SPX261022C07735000"
    assert data["data"][0]["moneda_id"] == "USD"

    # Verificar que get_contratos recibió None para los filtros vacíos
    mock_get_contratos.assert_called_once()
    _, kwargs = mock_get_contratos.call_args
    assert kwargs.get("cod_subyacente") is None
    assert kwargs.get("id_contrato_opcion") is None
    assert kwargs.get("fch_expiracion") is None
    assert kwargs.get("imp_ejercicio") is None


@patch("service.contrato_opcion_service.ContratoOpcionReader.get_contratos")
def test_get_contratos_with_dd_mm_yyyy_date_filter(mock_get_contratos, client):
    from datetime import date
    mock_get_contratos.return_value = []

    response = client.get(
        "/bagholdercuy/api/v2/contratos-opcion?fch_expiracion=28/10/2026"
    )
    assert response.status_code == 200
    mock_get_contratos.assert_called_once()
    _, kwargs = mock_get_contratos.call_args
    assert kwargs.get("fch_expiracion") == date(2026, 10, 28)


@patch("service.contrato_opcion_service.ContratoOpcionReader.get_by_id")
def test_get_contrato_by_id_success(mock_get_by_id, client):
    mock_get_by_id.return_value = _crear_mock_contrato(123, "MSFT261218C00400000", "CALL", "MSFT", 400.0)

    response = client.get("/bagholdercuy/api/v2/contratos-opcion/123")
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["id_contrato_opcion"] == 123
    assert data["data"]["cod_symbol"] == "MSFT261218C00400000"


@patch("service.contrato_opcion_service.ContratoOpcionReader.get_by_id")
def test_get_contrato_by_id_not_found(mock_get_by_id, client):
    mock_get_by_id.return_value = None

    response = client.get("/bagholdercuy/api/v2/contratos-opcion/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert "no encontrado" in data["message"]


def test_get_contratos_invalid_sentido_pydantic_error(client):
    response = client.get("/bagholdercuy/api/v2/contratos-opcion?sentidos=INVALID")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No se ha indicado un tipo de opcion valido" in data["message"]


# =============================================================================
# Tests de Creación (POST /contratos-opcion)
# =============================================================================

@patch("service.contrato_opcion_service.SymbolReader.get")
@patch("service.contrato_opcion_service.OpcionProcessor.guardar")
@patch("service.contrato_opcion_service.db.session.commit")
def test_crear_contrato_opcion_success(mock_commit, mock_guardar, mock_get_symbol, client):
    mock_symbol = MagicMock(spec=SymbolModel)
    mock_symbol.id_symbol = 15
    mock_symbol.symbol = "NVDA"
    mock_get_symbol.return_value = mock_symbol

    payload = {
        "cod_symbol": "NVDA261120C00120000",
        "sentido": "CALL",
        "cod_subyacente": "NVDA",
        "fch_expiracion": "2026-11-20",
        "imp_ejercicio": 120.0,
        "ctd_tamano_contrato": 100,
        "cod_moneda": "USD",
        "descripcion": "Nvidia Call Option",
    }

    response = client.post("/bagholdercuy/api/v2/contratos-opcion", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Se ha guardado correctamente la opcion."
    assert data["data"]["cod_symbol"] == "NVDA261120C00120000"
    assert data["data"]["tipo_opcion"] == "CALL"
    assert data["data"]["strike"] == 120.0
    mock_commit.assert_called_once()


def test_crear_contrato_opcion_missing_fields(client):
    payload = {
        "cod_symbol": "NVDA261120C00120000",
        # missing cod_subyacente, fch_expiracion, imp_ejercicio
    }
    response = client.post("/bagholdercuy/api/v2/contratos-opcion", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert len(data["errors"]) > 0


def test_crear_contrato_opcion_invalid_sentido(client):
    payload = {
        "cod_symbol": "NVDA261120C00120000",
        "sentido": "STRADDLE",
        "cod_subyacente": "NVDA",
        "fch_expiracion": "2026-11-20",
        "imp_ejercicio": 120.0,
        "ctd_tamano_contrato": 100,
        "cod_moneda": "USD",
    }
    response = client.post("/bagholdercuy/api/v2/contratos-opcion", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "no es valido" in data["message"]


@patch("service.contrato_opcion_service.SymbolReader.get")
def test_crear_contrato_opcion_subyacente_no_existe(mock_get_symbol, client):
    mock_get_symbol.return_value = None

    payload = {
        "cod_symbol": "UNKNOWN261120C00100000",
        "sentido": "CALL",
        "cod_subyacente": "UNKNOWN",
        "fch_expiracion": "2026-11-20",
        "imp_ejercicio": 100.0,
        "ctd_tamano_contrato": 100,
        "cod_moneda": "USD",
    }
    response = client.post("/bagholdercuy/api/v2/contratos-opcion", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "El subyacente UNKNOWN no existe" in data["message"]


# =============================================================================
# Tests de Cadena de Opciones (GET/POST /contratos-opcion/chain)
# =============================================================================

@patch("service.contrato_opcion_service.ContratoOpcionReader.get_puts")
@patch("service.contrato_opcion_service.ContratoOpcionReader.get_calls")
def test_get_options_chain_success(mock_get_calls, mock_get_puts, client):
    c1 = _crear_mock_contrato(1, "AAPL261120C00150000", "CALL", "AAPL", 150.0, date(2026, 11, 20))
    p1 = _crear_mock_contrato(2, "AAPL261120P00150000", "PUT", "AAPL", 150.0, date(2026, 11, 20))

    mock_get_calls.return_value = [c1]
    mock_get_puts.return_value = [p1]

    response = client.get("/bagholdercuy/api/v2/contratos-opcion/chain?cod_symbol=AAPL")
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert "calls" in data["data"]
    assert "puts" in data["data"]
    assert data["data"]["exp_dates"] == ["2026-11-20"]
    assert data["data"]["strikes"] == [150.0]


def test_get_options_chain_missing_symbol(client):
    response = client.get("/bagholdercuy/api/v2/contratos-opcion/chain")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "cod_symbol" in data["message"]


# =============================================================================
# Tests de Resumen de Subyacentes (GET /contratos-opcion/resumen-subyacentes)
# =============================================================================

@patch("service.contrato_opcion_service.ContratoOpcionService.get_resumen_subyacentes")
def test_get_resumen_subyacentes_success(mock_resumen, client):
    class DummyResumen:
        cod_symbol_subyacente = "AAPL"
        fch_registro = datetime(2026, 1, 1, 10, 0, 0)
        fch_vencimiento = date(2026, 12, 18)

    mock_resumen.return_value = [DummyResumen()]

    response = client.get("/bagholdercuy/api/v2/contratos-opcion/resumen-subyacentes")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["cod_symbol_subyacente"] == "AAPL"


# =============================================================================
# Tests de Métodos Legacy en ContratoOpcionController
# =============================================================================

@patch("service.contrato_opcion_service.ContratoOpcionReader.get_contratos")
def test_legacy_get_contratos_method(mock_get_contratos):
    mock_get_contratos.return_value = [
        _crear_mock_contrato(1, "AAPL261120C00150000", "CALL", "AAPL", 150.0)
    ]
    ctrl = ContratoOpcionController()
    res = ctrl.get_contratos({"cod_symbol": "AAPL"})
    assert res["success"] is True
    assert len(res["data"]) == 1
