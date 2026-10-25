import pytest
from unittest.mock import patch, MagicMock
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


@patch.object(MonitoreoReader, "get_monitoreo_activo")
def test_monitoreo_get_calculates_dias_expiracion(mock_get_activo, client):
    from datetime import date, timedelta

    venc = date.today() + timedelta(days=5)
    mock_get_activo.return_value = [
        {
            "id_monitoreo": 4,
            "id_symbol_type": 2,
            "id_contrato_opcion": 2,
            "id_cuenta": 3,
            "cod_symbol": "SPX261028P07570000",
            "fch_vencimiento": venc.isoformat(),
            "tipo_opcion": "PUT",
            "imp_strike": 7570.0,
        }
    ]

    response = client.get("/bagholdercuy/api/v2/monitoreos?id_cuenta=3")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["dias_expiracion"] == 5
    assert data["data"][0]["fch_vencimiento"] == venc.isoformat()
    assert data["data"][0]["tipo_opcion"] == "PUT"
    assert data["data"][0]["imp_strike"] == 7570.0


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


@patch("controller.monitoreo.db.session.commit")
@patch.object(MonitoreoManager, "registrar")
def test_monitoreo_post_option_success(mock_registrar, mock_commit, client):
    def fake_registrar(monitoreo_nuevo):
        monitoreo_nuevo.id_monitoreo = 99
        monitoreo_nuevo.id_symbol_type = 2
        return monitoreo_nuevo

    mock_registrar.side_effect = fake_registrar

    response = client.post(
        "/bagholdercuy/api/v2/monitoreos",
        json={"id_cuenta": 1, "id_contrato_opcion": 50},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["id_monitoreo"] == 99
    assert data["data"]["id_contrato_opcion"] == 50
    assert data["data"]["id_symbol_type"] == 2
    mock_commit.assert_called_once()


@patch("controller.monitoreo.db.session.commit")
@patch.object(MonitoreoManager, "registrar")
def test_monitoreo_post_option_by_attributes_success(mock_registrar, mock_commit, client):
    def fake_registrar(monitoreo_nuevo):
        monitoreo_nuevo.id_monitoreo = 101
        monitoreo_nuevo.id_contrato_opcion = 77
        monitoreo_nuevo.id_symbol_type = 2
        return monitoreo_nuevo

    mock_registrar.side_effect = fake_registrar

    response = client.post(
        "/bagholdercuy/api/v2/monitoreos",
        json={
            "id_cuenta": 1,
            "id_symbol_type": 2,
            "id_symbol": 10,
            "cod_symbol": "AAPL261120C00150000",
            "tipo_opcion": "CALL",
            "fch_vencimiento": "2026-11-20",
            "imp_strike": 150.0,
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["id_monitoreo"] == 101
    assert data["data"]["id_contrato_opcion"] == 77
    assert data["data"]["id_symbol_type"] == 2
    mock_commit.assert_called_once()


@patch("manager.monitoreo.db.session.add")
@patch("manager.monitoreo.db.session.flush")
@patch("manager.monitoreo.MonitoreoReader")
@patch("manager.monitoreo.SymbolReader")
@patch("manager.monitoreo.ContratoOpcionReader")
def test_monitoreo_manager_registrar_creates_option_contract(
    mock_opt_reader, mock_sym_reader, mock_mon_reader, mock_flush, mock_add
):
    mock_opt_reader.get_contrato.return_value = None
    mock_sym = MagicMock()
    mock_sym.id_symbol = 10
    mock_sym_reader.return_value.get.return_value = mock_sym

    mock_mon_reader_instance = MagicMock()
    mock_mon_reader_instance.get_by_option.return_value = None
    mock_mon_reader.return_value = mock_mon_reader_instance

    def fake_flush():
        for call_args in mock_add.call_args_list:
            obj = call_args[0][0]
            if hasattr(obj, "cod_symbol") and not getattr(obj, "id_contrato_opcion", None):
                obj.id_contrato_opcion = 888

    mock_flush.side_effect = fake_flush
    mock_opt_reader.get_by_id.return_value = MagicMock(
        id_contrato_opcion=888, cod_symbol="AAPL261120C00150000"
    )

    from parser.monitoreo import MonitoreoParser

    parser = MonitoreoParser()
    mon = parser.parse_args_registrar({
        "id_cuenta": 1,
        "id_symbol_type": 2,
        "id_symbol": 10,
        "cod_symbol": "AAPL261120C00150000",
        "tipo_opcion": "CALL",
        "fch_vencimiento": "2026-11-20",
        "imp_strike": 150.0,
    })

    manager = MonitoreoManager()
    res = manager.registrar(mon)

    assert res.id_contrato_opcion == 888
    assert res.id_symbol_type == 2
    assert res.id_symbol is None


@patch("manager.monitoreo.db.session.add")
@patch("manager.monitoreo.db.session.flush")
@patch("manager.monitoreo.MonitoreoReader")
@patch("manager.monitoreo.SymbolReader")
@patch("manager.monitoreo.ContratoOpcionReader")
def test_monitoreo_manager_registrar_with_id_symbol_subyacente(
    mock_opt_reader, mock_sym_reader, mock_mon_reader, mock_flush, mock_add
):
    from model.contrato_opcion import ContratoOpcionModel
    from schemas.monitoreo_schema import MonitoreoRegistrarRequest

    mock_opt_reader.get_contrato.return_value = None
    mock_sym = MagicMock()
    mock_sym.id_symbol = 25
    mock_sym_reader.return_value.get.return_value = mock_sym

    mock_mon_reader_instance = MagicMock()
    mock_mon_reader_instance.get_by_option.return_value = None
    mock_mon_reader.return_value = mock_mon_reader_instance

    created_option = None

    def fake_flush():
        nonlocal created_option
        for call_args in mock_add.call_args_list:
            obj = call_args[0][0]
            if isinstance(obj, ContratoOpcionModel):
                created_option = obj
                obj.id_contrato_opcion = 999

    mock_flush.side_effect = fake_flush
    mock_opt_reader.get_by_id.return_value = MagicMock(
        id_contrato_opcion=999, cod_symbol="SPX261218P05000000"
    )

    req = MonitoreoRegistrarRequest(
        id_cuenta=2,
        id_symbol_type=2,
        id_symbol_subyacente=25,
        cod_symbol="SPX261218P05000000",
        tipo_opcion="PUT",
        fch_vencimiento="2026-12-18",
        imp_strike=5000.0,
    )
    mon = req.to_model()

    manager = MonitoreoManager()
    res = manager.registrar(mon)

    assert res.id_contrato_opcion == 999
    assert res.id_symbol_type == 2
    assert created_option is not None
    assert created_option.id_symbol_subyacente == 25
    assert created_option.id_symbol == 25
    assert created_option.tipo_opcion == "PUT"


@patch("manager.monitoreo.db.session.add")
@patch("manager.monitoreo.db.session.flush")
@patch("manager.monitoreo.MonitoreoReader")
@patch("manager.monitoreo.SymbolReader")
@patch("manager.monitoreo.ContratoOpcionReader")
def test_monitoreo_manager_auto_formats_osi_when_cod_symbol_is_underlying(
    mock_opt_reader, mock_sym_reader, mock_mon_reader, mock_flush, mock_add
):
    from model.contrato_opcion import ContratoOpcionModel
    from schemas.monitoreo_schema import MonitoreoRegistrarRequest

    mock_opt_reader.get_contrato.return_value = None
    mock_sym = MagicMock()
    mock_sym.id_symbol = 30
    mock_sym.symbol = "SPX"
    mock_sym_reader.return_value.get.return_value = mock_sym

    mock_mon_reader_instance = MagicMock()
    mock_mon_reader_instance.get_by_option.return_value = None
    mock_mon_reader.return_value = mock_mon_reader_instance

    created_option = None

    def fake_flush():
        nonlocal created_option
        for call_args in mock_add.call_args_list:
            obj = call_args[0][0]
            if isinstance(obj, ContratoOpcionModel):
                created_option = obj
                obj.id_contrato_opcion = 1010

    mock_flush.side_effect = fake_flush
    mock_opt_reader.get_by_id.return_value = MagicMock(
        id_contrato_opcion=1010, cod_symbol="SPX261019C05000000"
    )

    # El usuario/cliente envió cod_symbol="SPX" (el subyacente por error)
    req = MonitoreoRegistrarRequest(
        id_cuenta=3,
        id_symbol_type=2,
        id_symbol_subyacente=30,
        cod_symbol="SPX",
        tipo_opcion="CALL",
        fch_vencimiento="2026-10-19",
        imp_strike=5000.0,
    )
    mon = req.to_model()

    manager = MonitoreoManager()
    res = manager.registrar(mon)

    assert res.id_contrato_opcion == 1010
    assert created_option is not None
    # Debe ser el ticker OSI, NUNCA "SPX"
    assert created_option.cod_symbol == "SPX261019C05000000"
    assert created_option.id_symbol_subyacente == 30


# =====================================================================
# Tests para DELETE /monitoreos/<id> (Eliminación lógica)
# =====================================================================

@patch("controller.monitoreo.db.session.commit")
@patch.object(MonitoreoManager, "desactivar")
def test_monitoreo_delete_success(mock_desactivar, mock_commit, client):
    mock_desactivar.return_value = MagicMock(id_monitoreo=42, flg_activo=0)

    response = client.delete("/bagholdercuy/api/v2/monitoreos/42")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Se ha eliminado el monitoreo correctamente."
    assert data["data"]["id_monitoreo"] == 42
    mock_desactivar.assert_called_once_with(id_monitoreo=42)
    mock_commit.assert_called_once()


def test_monitoreo_delete_missing_id(client):
    response = client.delete("/bagholdercuy/api/v2/monitoreos")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Debe proporcionar el id_monitoreo a eliminar" in data["message"]


@patch("controller.monitoreo.db.session.rollback")
@patch.object(MonitoreoManager, "desactivar")
def test_monitoreo_delete_not_found(mock_desactivar, mock_rollback, client):
    mock_desactivar.side_effect = AppException("No se ha encontrado el monitoreo con id 999")

    response = client.delete("/bagholdercuy/api/v2/monitoreos/999")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No se ha encontrado el monitoreo con id 999" in data["message"]
    mock_rollback.assert_called_once()


@patch.object(MonitoreoReader, "get")
def test_monitoreo_manager_desactivar(mock_get):
    fake_monitoreo = MagicMock(id_monitoreo=55, flg_activo=1)
    mock_get.return_value = fake_monitoreo

    manager = MonitoreoManager()
    res = manager.desactivar(id_monitoreo=55)

    assert res.flg_activo == 0
    mock_get.assert_called_once_with(id_monitoreo=55)


@patch.object(MonitoreoReader, "get_by_symbol")
@patch("manager.monitoreo.SymbolReader")
def test_monitoreo_manager_reactivar_si_inactivo(mock_sym_reader_cls, mock_get_by_symbol):
    mock_sym_reader = MagicMock()
    mock_sym_reader_cls.return_value = mock_sym_reader
    mock_sym_reader.get.return_value = MagicMock(id_symbol=10, symbol="AAPL", id_symbol_type=1)

    inactive_record = MagicMock(id_monitoreo=12, id_symbol=10, id_cuenta=1, flg_activo=0)
    mock_get_by_symbol.return_value = inactive_record

    mon = MagicMock(
        id_symbol=10,
        id_cuenta=1,
        id_contrato_opcion=None,
        id_symbol_type=1,
        contrato_opcion_data=None,
        fch_registro=None,
        flg_activo=1,
    )

    manager = MonitoreoManager()
    res = manager.registrar(mon)

    assert res.id_monitoreo == 12
    assert res.flg_activo == 1




