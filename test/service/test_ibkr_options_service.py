import pytest
from unittest.mock import patch, MagicMock
from service.markets_data_providers.ibkr.ibkr_options_service import (
    IbkrOptionsService,
    expiration_cache,
    strikes_cache,
    options_cache,
)


@pytest.fixture(autouse=True)
def clear_cache():
    expiration_cache.clear()
    strikes_cache.clear()
    options_cache.clear()
    yield
    expiration_cache.clear()
    strikes_cache.clear()
    options_cache.clear()


@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
def test_get_expiration_months_from_sections_success(mock_search):
    mock_search.return_value = [
        {
            "conid": 265598,
            "symbol": "AAPL",
            "sections": [
                {"secType": "STK", "exchange": "SMART"},
                {
                    "secType": "OPT",
                    "months": "OCT26;NOV26;DEC26",
                    "exchange": "SMART",
                },
            ],
        }
    ]

    service = IbkrOptionsService()
    result = service.get_expiration_months("AAPL")

    mock_search.assert_called_once_with(symbol="AAPL")
    assert result == ["OCT26", "NOV26", "DEC26"]


@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
def test_get_expiration_months_caching(mock_search):
    mock_search.return_value = [
        {
            "conid": 265598,
            "symbol": "AAPL",
            "sections": [
                {
                    "secType": "OPT",
                    "months": "OCT26;NOV26",
                },
            ],
        }
    ]

    service1 = IbkrOptionsService()
    res1 = service1.get_expiration_months("AAPL")

    # Segunda llamada desde una nueva instancia con diferente casing
    service2 = IbkrOptionsService()
    res2 = service2.get_expiration_months("aapl")

    assert res1 == ["OCT26", "NOV26"]
    assert res2 == ["OCT26", "NOV26"]
    # Debería haberse llamado sólo 1 vez a la API de IBKR gracias a la caché
    mock_search.assert_called_once_with(symbol="AAPL")


@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
def test_get_expiration_months_no_options(mock_search):
    mock_search.return_value = [
        {
            "conid": 11111,
            "symbol": "VXX",
            "secType": "STK",
            "sections": [{"secType": "STK"}],
        }
    ]

    service = IbkrOptionsService()
    result = service.get_expiration_months("VXX")

    assert result == []


def test_get_expiration_months_missing_symbol():
    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="El parámetro 'cod_symbol' es requerido"):
        service.get_expiration_months("")


@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
def test_get_expiration_months_api_error(mock_search):
    mock_search.return_value = {"error": "Gateway timeout"}

    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="Error de la API de IBKR: Gateway timeout"):
        service.get_expiration_months("AAPL")


@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
def test_get_expiration_months_invalid_format(mock_search):
    mock_search.return_value = "invalid response"

    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="Respuesta inesperada de la API de IBKR"):
        service.get_expiration_months("AAPL")


@patch("api.ibkr.InteractiveBrokersClient.search_contract_by_symbol")
def test_get_expiration_dates_backward_compatibility(mock_search):
    mock_search.return_value = [
        {
            "conid": 265598,
            "symbol": "AAPL",
            "sections": [
                {
                    "secType": "OPT",
                    "months": "OCT26;NOV26",
                },
            ],
        }
    ]

    service = IbkrOptionsService()
    result = service.get_expiration_dates("AAPL")

    mock_search.assert_called_once_with(symbol="AAPL")
    assert result == ["OCT26", "NOV26"]


# =====================================================================
# Tests para get_strikes
# =====================================================================

@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
@patch("api.ibkr.InteractiveBrokersClient.secdef_strikes")
def test_get_strikes_success(mock_strikes, mock_find):
    mock_contract = MagicMock()
    mock_contract.conid = 265598
    mock_contract.exchange = "NASDAQ"
    mock_find.return_value = mock_contract

    mock_strikes.return_value = {
        "call": [180.0, 185.0, 190.0],
        "put": [180.0, 185.0, 190.0],
    }

    service = IbkrOptionsService()
    res = service.get_strikes(cod_subyacente="AAPL", expiracion="OCT26")

    assert res == {
        "call": [180.0, 185.0, 190.0],
        "put": [180.0, 185.0, 190.0],
    }
    mock_find.assert_called_once_with(cod_symbol="AAPL")
    mock_strikes.assert_called_once_with(
        conid=265598,
        month="OCT26",
        sec_type="OPT",
        exchange=None,
    )


@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
@patch("api.ibkr.InteractiveBrokersClient.secdef_strikes")
def test_get_strikes_with_exchange(mock_strikes, mock_find):
    mock_contract = MagicMock()
    mock_contract.conid = 12345
    mock_find.return_value = mock_contract

    mock_strikes.return_value = {"call": [200.0], "put": [200.0]}

    service = IbkrOptionsService()
    res = service.get_strikes(
        cod_subyacente="SPY", expiracion="JAN25", exchange="SMART"
    )

    assert res == {"call": [200.0], "put": [200.0]}
    mock_find.assert_called_once_with(cod_symbol="SPY")
    mock_strikes.assert_called_once_with(
        conid=12345,
        month="JAN25",
        sec_type="OPT",
        exchange="SMART",
    )


@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
def test_get_strikes_contract_not_found(mock_find):
    mock_find.return_value = None

    service = IbkrOptionsService()
    with pytest.raises(
        ValueError, match="No se encontró el contrato para el símbolo 'UNKNOWN'"
    ):
        service.get_strikes(cod_subyacente="UNKNOWN", expiracion="JAN25")


def test_get_strikes_missing_cod_subyacente():
    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="El parámetro 'cod_subyacente' es requerido"):
        service.get_strikes(cod_subyacente="", expiracion="JAN25")


def test_get_strikes_missing_expiracion():
    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="El parámetro 'expiracion' es requerido"):
        service.get_strikes(cod_subyacente="AAPL", expiracion="")


@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
@patch("api.ibkr.InteractiveBrokersClient.secdef_strikes")
def test_get_strikes_api_error(mock_strikes, mock_find):
    mock_contract = MagicMock()
    mock_contract.conid = 265598
    mock_find.return_value = mock_contract
    mock_strikes.return_value = {"error": "Session expired"}

    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="Error de la API de IBKR: Session expired"):
        service.get_strikes(cod_subyacente="AAPL", expiracion="JAN25")


# =====================================================================
# Tests para _get_contracts
# =====================================================================

@patch("api.ibkr.InteractiveBrokersClient.secdef_info")
def test_get_contracts_success(mock_info):
    mock_info.return_value = [
        {
            "conid": 1001,
            "symbol": "AAPL",
            "secType": "OPT",
            "strike": 150.0,
            "right": "C",
            "maturityDate": "20250117",
        },
        {
            "conid": 1002,
            "symbol": "AAPL",
            "secType": "OPT",
            "strike": 150.0,
            "right": "P",
            "maturityDate": "20250117",
        },
    ]

    service = IbkrOptionsService()
    contracts = service._get_contracts(conid=265598, month="JAN25", strike=150)

    assert len(contracts) == 2
    mock_info.assert_called_once_with(
        conid=265598, month="JAN25", strike=150, sec_type="OPT"
    )


def test_get_contracts_missing_params():
    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="El parámetro 'conid' es requerido"):
        service._get_contracts(conid=None, month="JAN25", strike=150)

    with pytest.raises(ValueError, match="El parámetro 'month' es requerido"):
        service._get_contracts(conid=123, month="", strike=150)

    with pytest.raises(ValueError, match="El parámetro 'strike' es requerido"):
        service._get_contracts(conid=123, month="JAN25", strike=None)


@patch("api.ibkr.InteractiveBrokersClient.secdef_info")
def test_get_contracts_api_error(mock_info):
    mock_info.return_value = {"error": "Secdef error"}
    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="Error de la API de IBKR: Secdef error"):
        service._get_contracts(conid=123, month="JAN25", strike=150)


# =====================================================================
# Tests para _build_options_chain
# =====================================================================

def test_build_options_chain_selection_around_underlying():
    # 100 strikes de 10 a 1000 con paso 10
    strikes = [float(x) for x in range(10, 1010, 10)]
    imp_underlying = 500.0
    num_strikes = 50

    service = IbkrOptionsService()
    result = service._build_options_chain(
        imp_underlying=imp_underlying,
        strikes=strikes,
        num_strikes=num_strikes,
        fch_expiracion="2025-01-17",
    )

    selected = result["strikes"]
    assert len(selected) == 50
    # 25 strikes por abajo de 500 (260 a 500) y 25 por arriba (510 a 750)
    assert min(selected) == 260.0
    assert max(selected) == 750.0
    assert 500.0 in selected
    assert result["imp_underlying"] == 500.0


def test_build_options_chain_all_strikes_when_zero():
    strikes = [float(x) for x in range(10, 1010, 10)]
    service = IbkrOptionsService()
    result = service._build_options_chain(
        imp_underlying=500.0,
        strikes=strikes,
        num_strikes=0,
        fch_expiracion="2025-01-17",
    )
    assert len(result["strikes"]) == len(strikes)
    assert result["strikes"] == strikes


def test_build_options_chain_missing_fch_expiracion():
    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="El parámetro 'fch_expiracion' es requerido"):
        service._build_options_chain(
            imp_underlying=100.0, strikes=[100.0], fch_expiracion=None
        )

    with pytest.raises(ValueError, match="El parámetro 'fch_expiracion' es requerido"):
        service._build_options_chain(
            imp_underlying=100.0, strikes=[100.0], fch_expiracion=""
        )


@patch.object(IbkrOptionsService, "_get_contracts")
def test_build_options_chain_with_contracts_and_expiration_filter(mock_get_contracts):
    mock_get_contracts.side_effect = lambda conid, month, strike: [
        {
            "conid": 1000 + int(strike),
            "symbol": "AAPL",
            "strike": strike,
            "right": "C",
            "maturityDate": "20250117",
        },
        {
            "conid": 2000 + int(strike),
            "symbol": "AAPL",
            "strike": strike,
            "right": "P",
            "maturityDate": "20250117",
        },
        # Contrato con fecha de otra semana que debe ser filtrado
        {
            "conid": 3000 + int(strike),
            "symbol": "AAPL",
            "strike": strike,
            "right": "C",
            "maturityDate": "20250124",
        },
    ]

    service = IbkrOptionsService()
    result = service._build_options_chain(
        imp_underlying=150.0,
        strikes=[140.0, 150.0, 160.0],
        num_strikes=2,
        conid=265598,
        month="JAN25",
        fch_expiracion="2025-01-17",
    )

    assert "calls" in result
    assert "puts" in result
    assert len(result["calls"]) == 2
    assert len(result["puts"]) == 2
    assert all(c["fch_vencimiento"] == "20250117" for c in result["calls"])
    assert all(p["right"] == "P" for p in result["puts"])
    assert result["fch_vencimiento"] == "2025-01-17"
    assert result["fechas_vencimiento"] == ["2025-01-17", "2025-01-24"]
    assert result["exp_dates"] == ["2025-01-17", "2025-01-24"]


@patch.object(IbkrOptionsService, "_get_contracts")
def test_build_options_chain_closest_date_when_not_exact_match(mock_get_contracts):
    mock_get_contracts.side_effect = lambda conid, month, strike: [
        {
            "conid": 1000 + int(strike),
            "symbol": "AAPL",
            "strike": strike,
            "right": "C",
            "maturityDate": "20250117",
        },
        {
            "conid": 2000 + int(strike),
            "symbol": "AAPL",
            "strike": strike,
            "right": "C",
            "maturityDate": "20250124",
        },
    ]

    service = IbkrOptionsService()
    # 2025-01-19 está a 2 días de 2025-01-17 y a 5 días de 2025-01-24 -> debe elegir 2025-01-17
    result1 = service._build_options_chain(
        imp_underlying=150.0,
        strikes=[150.0],
        num_strikes=1,
        conid=265598,
        month="JAN25",
        fch_expiracion="2025-01-19",
    )
    assert len(result1["calls"]) == 1
    assert result1["calls"][0]["maturityDate"] == "20250117"
    assert result1["fch_vencimiento"] == "2025-01-17"

    # 2025-01-23 está a 1 día de 2025-01-24 y a 6 días de 2025-01-17 -> debe elegir 2025-01-24
    result2 = service._build_options_chain(
        imp_underlying=150.0,
        strikes=[150.0],
        num_strikes=1,
        conid=265598,
        month="JAN25",
        fch_expiracion="2025-01-23",
    )
    assert len(result2["calls"]) == 1
    assert result2["calls"][0]["maturityDate"] == "20250124"
    assert result2["fch_vencimiento"] == "2025-01-24"


# =====================================================================
# Tests para get_options_chain
# =====================================================================

@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
@patch.object(IbkrOptionsService, "get_expiration_months")
@patch.object(IbkrOptionsService, "get_strikes")
@patch.object(IbkrOptionsService, "_get_contracts")
@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_get_options_chain_success(
    mock_snapshot, mock_get_contracts, mock_get_strikes, mock_get_exp, mock_find
):
    mock_contract = MagicMock()
    mock_contract.conid = 265598
    mock_find.return_value = mock_contract

    mock_get_exp.return_value = ["DEC24", "JAN25", "FEB25"]
    mock_snapshot.side_effect = [
        [{"conid": 265598, "31": 152.5}],
        [
            {"conid": 5150, "84": "4.20", "86": "4.30", "31": "4.25"},
            {"conid": 5160, "84": "1.10", "86": "1.15", "31": "C1.12"},
            {"conid": 6150, "84": "1.70", "86": "1.75", "31": "1.72"},
            {"conid": 6160, "84": "8.50", "86": "8.60", "31": "8.55"},
        ],
    ]
    mock_get_strikes.return_value = {
        "call": [140.0, 150.0, 160.0],
        "put": [140.0, 150.0, 160.0],
    }
    mock_get_contracts.side_effect = lambda conid, month, strike: [
        {
            "conid": 5000 + int(strike),
            "symbol": "AAPL",
            "strike": strike,
            "right": "C",
            "maturityDate": "20250117",
        },
        {
            "conid": 6000 + int(strike),
            "symbol": "AAPL",
            "strike": strike,
            "right": "P",
            "maturityDate": "20250117",
        },
    ]

    service = IbkrOptionsService()
    result = service.get_options_chain(
        cod_subyacente="AAPL",
        fch_expiracion="2025-01-17",
        num_strikes=2,
    )

    assert result["imp_underlying"] == 152.5
    assert len(result["calls"]) == 2
    assert len(result["puts"]) == 2
    assert result["fch_vencimiento"] == "2025-01-17"
    assert result["fechas_vencimiento"] == ["2025-01-17"]
    assert result["exp_dates"] == ["2025-01-17"]

    # Verificar que las llamadas y puts recibieron bid, ask, last
    call_5150 = next(c for c in result["calls"] if c["conid"] == 5150)
    assert call_5150["bid"] == 4.20
    assert call_5150["ask"] == 4.30
    assert call_5150["last"] == 4.25

    call_5160 = next(c for c in result["calls"] if c["conid"] == 5160)
    assert call_5160["bid"] == 1.10
    assert call_5160["ask"] == 1.15
    assert call_5160["last"] == 1.12

    put_6150 = next(p for p in result["puts"] if p["conid"] == 6150)
    assert put_6150["bid"] == 1.70
    assert put_6150["ask"] == 1.75
    assert put_6150["last"] == 1.72

    mock_find.assert_called_once_with(cod_symbol="AAPL")
    mock_get_exp.assert_called_once_with(cod_symbol="AAPL")
    assert mock_snapshot.call_count == 2
    mock_snapshot.assert_any_call(conids=[265598], fields=[31, 84, 86])
    mock_snapshot.assert_any_call(conids=[5150, 5160, 6150, 6160], fields=[31, 84, 86])
    mock_get_strikes.assert_called_once_with(cod_subyacente="AAPL", expiracion="JAN25")


@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
def test_get_options_chain_contract_not_found(mock_find):
    mock_find.return_value = None
    service = IbkrOptionsService()
    with pytest.raises(
        ValueError, match="No se encontró el contrato para el símbolo 'UNKNOWN'"
    ):
        service.get_options_chain(
            cod_subyacente="UNKNOWN", fch_expiracion="2025-01-17"
        )


@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
@patch.object(IbkrOptionsService, "get_expiration_months")
def test_get_options_chain_expiration_month_not_available(mock_get_exp, mock_find):
    mock_contract = MagicMock()
    mock_contract.conid = 265598
    mock_find.return_value = mock_contract
    mock_get_exp.return_value = ["OCT26", "NOV26"]

    service = IbkrOptionsService()
    with pytest.raises(
        ValueError, match="El mes de expiración 'JAN25' no está disponible"
    ):
        service.get_options_chain(
            cod_subyacente="AAPL", fch_expiracion="2025-01-17"
        )


def test_get_options_chain_missing_arguments():
    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="El parámetro 'cod_subyacente' es requerido"):
        service.get_options_chain(cod_subyacente="", fch_expiracion="2025-01-17")

    with pytest.raises(ValueError, match="El parámetro 'cod_subyacente' es requerido"):
        service.get_options_chain(cod_subyacente=None)


@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
@patch.object(IbkrOptionsService, "get_expiration_months")
@patch.object(IbkrOptionsService, "get_strikes")
@patch.object(IbkrOptionsService, "_get_contracts")
@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_get_options_chain_default_system_date_when_omitted(
    mock_snapshot, mock_get_contracts, mock_get_strikes, mock_get_exp, mock_find
):
    from datetime import date
    service = IbkrOptionsService()
    current_month = service._parse_expiration_month(date.today())

    mock_contract = MagicMock()
    mock_contract.conid = 265598
    mock_find.return_value = mock_contract

    mock_get_exp.return_value = [current_month]
    mock_snapshot.return_value = [{"conid": 265598, "31": 150.0}]
    mock_get_strikes.return_value = {"call": [150.0], "put": [150.0]}
    mock_get_contracts.return_value = [
        {
            "conid": 5001,
            "symbol": "AAPL",
            "strike": 150.0,
            "right": "C",
            "maturityDate": "20261023",
        }
    ]

    # Sin fch_expiracion
    result = service.get_options_chain(cod_subyacente="AAPL")

    assert result["imp_underlying"] == 150.0
    assert len(result["calls"]) == 1
    mock_find.assert_called_once_with(cod_symbol="AAPL")
    mock_get_exp.assert_called_once_with(cod_symbol="AAPL")
    mock_get_strikes.assert_called_once_with(
        cod_subyacente="AAPL", expiracion=current_month
    )


@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
@patch.object(IbkrOptionsService, "get_expiration_months")
@patch.object(IbkrOptionsService, "get_strikes")
@patch.object(IbkrOptionsService, "_get_contracts")
@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_get_options_chain_default_system_date_when_empty_string(
    mock_snapshot, mock_get_contracts, mock_get_strikes, mock_get_exp, mock_find
):
    from datetime import date
    service = IbkrOptionsService()
    current_month = service._parse_expiration_month(date.today())

    mock_contract = MagicMock()
    mock_contract.conid = 265598
    mock_find.return_value = mock_contract

    mock_get_exp.return_value = [current_month]
    mock_snapshot.return_value = [{"conid": 265598, "31": 150.0}]
    mock_get_strikes.return_value = {"call": [150.0], "put": [150.0]}
    mock_get_contracts.return_value = []

    # Con fch_expiracion="" (string vacío)
    result = service.get_options_chain(cod_subyacente="AAPL", fch_expiracion="")

    assert result["imp_underlying"] == 150.0
    mock_get_strikes.assert_called_once_with(
        cod_subyacente="AAPL", expiracion=current_month
    )


@patch("model.ibkr_contract.IbkrContractsModel.find_by_symbol")
@patch.object(IbkrOptionsService, "get_expiration_months")
@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_get_options_chain_snapshot_no_price(mock_snapshot, mock_get_exp, mock_find):
    mock_contract = MagicMock()
    mock_contract.conid = 265598
    mock_find.return_value = mock_contract
    mock_get_exp.return_value = ["JAN25"]
    mock_snapshot.return_value = [{"conid": 265598}]  # No price field

    service = IbkrOptionsService()
    with pytest.raises(
        ValueError, match="No se pudo obtener el precio del subyacente"
    ):
        service.get_options_chain(
            cod_subyacente="AAPL", fch_expiracion="2025-01-17"
        )


# =====================================================================
# Tests para get_underlying_price
# =====================================================================

@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_get_underlying_price_success(mock_snapshot):
    mock_snapshot.return_value = [{"conid": 265598, "31": 175.25}]

    service = IbkrOptionsService()
    price = service.get_underlying_price(conid=265598, cod_subyacente="AAPL")

    assert price == 175.25
    mock_snapshot.assert_called_once_with(conids=[265598], fields=[31, 84, 86])


def test_get_underlying_price_missing_conid():
    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="El parámetro 'conid' es requerido"):
        service.get_underlying_price(conid=None)


@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_get_underlying_price_api_error(mock_snapshot):
    mock_snapshot.return_value = {"error": "Snapshot timeout"}

    service = IbkrOptionsService()
    with pytest.raises(ValueError, match="Error de la API de IBKR: Snapshot timeout"):
        service.get_underlying_price(conid=265598)


# =====================================================================
# Tests para _enrich_options_with_market_data
# =====================================================================

@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_enrich_options_with_market_data_success(mock_snapshot):
    mock_snapshot.return_value = [
        {"conid": 1001, "84": "3.50", "86": "3.60", "31": "3.55"},
        {"conid": 2001, "84": "1.20", "86": "1.25", "31": "C1.22"},
    ]

    service = IbkrOptionsService()
    calls = [{"conid": 1001, "strike": 100}]
    puts = [{"conid": 2001, "strike": 100}, {"conid": 3001, "strike": 95}]

    service._enrich_options_with_market_data(calls=calls, puts=puts)

    assert calls[0]["bid"] == 3.50
    assert calls[0]["ask"] == 3.60
    assert calls[0]["last"] == 3.55

    assert puts[0]["bid"] == 1.20
    assert puts[0]["ask"] == 1.25
    assert puts[0]["last"] == 1.22

    # Conid 3001 no presente en snapshot recibe None
    assert puts[1]["bid"] is None
    assert puts[1]["ask"] is None
    assert puts[1]["last"] is None


@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_enrich_options_with_market_data_api_exception(mock_snapshot):
    mock_snapshot.side_effect = Exception("API error")

    service = IbkrOptionsService()
    calls = [{"conid": 1001, "strike": 100}]
    puts = [{"conid": 2001, "strike": 100}]

    service._enrich_options_with_market_data(calls=calls, puts=puts)

    assert calls[0]["bid"] is None
    assert calls[0]["ask"] is None
    assert calls[0]["last"] is None


def test_enrich_options_with_market_data_empty():
    service = IbkrOptionsService()
    service._enrich_options_with_market_data(calls=[], puts=[])
    # No exception raised


@patch("api.ibkr.InteractiveBrokersClient.marketdata_snapshot")
def test_enrich_options_with_market_data_pre_flight_flow(mock_snapshot):
    # Simula la primera llamada como pre-flight (sin valores de mercado)
    # y la segunda llamada entregando los datos reales del stream abierto
    mock_snapshot.side_effect = [
        [{"conid": 929933597}],  # Pre-flight inicial: IServer solo devuelve conid
        [{"conid": 929933597, "84": "56.5", "86": "57.4", "31": "56.1"}],  # Segunda consulta con stream abierto
    ]

    service = IbkrOptionsService()
    calls = [{"conid": 929933597, "strike": 7635.0}]
    puts = []

    # Usamos pre_flight_delay=0.01 para rapidez en el test
    service._enrich_options_with_market_data(calls=calls, puts=puts, pre_flight_delay=0.01)

    assert mock_snapshot.call_count == 2
    assert calls[0]["bid"] == 56.5
    assert calls[0]["ask"] == 57.4
    assert calls[0]["last"] == 56.1





