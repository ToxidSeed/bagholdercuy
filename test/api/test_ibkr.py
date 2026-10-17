import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from api.ibkr import InteractiveBrokersClient


@pytest.fixture(autouse=True)
def app_context():
    app = Flask("test_app")
    app.config["INTERACTIVE_BROKERS_ENDPOINT"] = "https://localhost:5000/v1/api"
    with app.app_context():
        yield



@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.post")
def test_search_contract_by_symbol_success(mock_post, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"conid": 265598, "symbol": "AAPL", "companyHeader": "APPLE INC"}
    ]
    mock_post.return_value = mock_response

    res = InteractiveBrokersClient.search_contract_by_symbol(symbol="AAPL")

    assert res == [{"conid": 265598, "symbol": "AAPL", "companyHeader": "APPLE INC"}]
    mock_post.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/secdef/search",
        json={"symbol": "AAPL", "name": False},
        headers={"Content-Type": "application/json"},
        verify=False,
    )


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.post")
def test_search_contract_by_symbol_with_sec_type(mock_post, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_post.return_value = mock_response

    res = InteractiveBrokersClient.search_contract_by_symbol(
        symbol="AAPL", name=True, sec_type="STK"
    )

    assert res == []
    mock_post.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/secdef/search",
        json={"symbol": "AAPL", "name": True, "secType": "STK"},
        headers={"Content-Type": "application/json"},
        verify=False,
    )


def test_search_contract_by_symbol_missing_symbol():
    with pytest.raises(ValueError, match="symbol is required"):
        InteractiveBrokersClient.search_contract_by_symbol()


def test_search_contract_by_symbol_debug():
    """
    Método para depurar la respuesta real de InteractiveBrokersClient.search_contract_by_symbol.
    No utiliza mocks en requests.post para permitir probar la integración contra la API real o local.
    Para visualizar la respuesta formateada ejecute:
    pytest -s test/api/test_ibkr.py -k test_search_contract_by_symbol_debug
    """
    import json
    from flask import current_app

    if not current_app.config.get("INTERACTIVE_BROKERS_ENDPOINT"):
        current_app.config["INTERACTIVE_BROKERS_ENDPOINT"] = (
            "https://localhost:5000/v1/api"
        )

    symbol = "XSP"
    print(f"\n[DEBUG IBKR] Petición a search_contract_by_symbol(symbol='{symbol}')...")

    try:
        res = InteractiveBrokersClient.search_contract_by_symbol(symbol=symbol)
        print("\n================== RESPUESTA API IBKR ==================")
        print(json.dumps(res, indent=2, ensure_ascii=False))
        print("========================================================\n")
        assert res is not None
    except Exception as e:
        print(f"\n[DEBUG IBKR EXCEPTION] Ocurrió una excepción al llamar a la API: {e}\n")
        pytest.skip(f"Live IBKR Gateway no autenticado o no disponible: {e}")


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_historical_market_data_success(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "symbol": "AAPL",
        "data": [{"o": 173.4, "c": 174.7, "h": 175.1, "l": 171.7, "v": 472117.45, "t": 16923456000}],
    }
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.historical_market_data(conid=265598, period="1d")

    assert res["symbol"] == "AAPL"
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/marketdata/history",
        params={"conid": 265598, "period": "1d"},
        headers={"Content-Type": "application/json"},
        verify=False,
    )


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_historical_market_data_with_all_params(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = {"symbol": "AAPL", "data": []}
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.historical_market_data(
        conid=265598,
        period="1d",
        bar="1h",
        exchange="SMART",
        start_time="20230821-13:30:00",
        outside_rth=True,
        source="Midpoint",
    )

    assert res == {"symbol": "AAPL", "data": []}
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/marketdata/history",
        params={
            "conid": 265598,
            "period": "1d",
            "bar": "1h",
            "exchange": "SMART",
            "startTime": "20230821-13:30:00",
            "outsideRth": True,
            "source": "Midpoint",
        },
        headers={"Content-Type": "application/json"},
        verify=False,
    )



def test_historical_market_data_missing_conid():
    with pytest.raises(ValueError, match="conid is required"):
        InteractiveBrokersClient.historical_market_data(period="1d")


def test_historical_market_data_missing_period():
    with pytest.raises(ValueError, match="period is required"):
        InteractiveBrokersClient.historical_market_data(conid=265598)


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_marketdata_snapshot_success(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"conid": 265598, "31": 180.5, "55": "AAPL"},
        {"conid": 8314, "31": 340.2, "55": "IBM"},
    ]
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.marketdata_snapshot(
        conids=[265598, 8314], fields=[31, 55, 84, 86]
    )

    assert len(res) == 2
    assert res[0]["conid"] == 265598
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/marketdata/snapshot",
        params={"conids": "265598,8314", "fields": "31,55,84,86"},
        headers={"Content-Type": "application/json"},
        verify=False,
    )


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_marketdata_snapshot_alias_and_single_conid(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = [{"conid": 265598, "31": 180.5}]
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.marketdata_snapshot(conid=265598, fields="31,84")

    assert res == [{"conid": 265598, "31": 180.5}]
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/marketdata/snapshot",
        params={"conids": "265598", "fields": "31,84"},
        headers={"Content-Type": "application/json"},
        verify=False,
    )


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_marketdata_snapshot_via_args(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = [{"conid": 265598}]
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.marketdata_snapshot(args={"conids": "265598"})

    assert res == [{"conid": 265598}]
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/marketdata/snapshot",
        params={"conids": "265598"},
        headers={"Content-Type": "application/json"},
        verify=False,
    )


def test_marketdata_snapshot_missing_conids():
    with pytest.raises(ValueError, match="conids is required"):
        InteractiveBrokersClient.marketdata_snapshot()



@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_secdef_strikes_success(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "call": [180.0, 185.0, 190.0],
        "put": [180.0, 185.0, 190.0],
    }
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.secdef_strikes(conid=265598, month="OCT26")

    assert res == {
        "call": [180.0, 185.0, 190.0],
        "put": [180.0, 185.0, 190.0],
    }
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/secdef/strikes",
        params={"conid": 265598, "sectype": "OPT", "month": "OCT26"},
        headers={"Content-Type": "application/json"},
        verify=False,
    )


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_secdef_strikes_with_exchange_and_alias(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = {"call": [200.0], "put": [200.0]}
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.strikes(
        conid=265598, month="NOV26", sec_type="OPT", exchange="SMART"
    )

    assert res == {"call": [200.0], "put": [200.0]}
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/secdef/strikes",
        params={
            "conid": 265598,
            "sectype": "OPT",
            "month": "NOV26",
            "exchange": "SMART",
        },
        headers={"Content-Type": "application/json"},
        verify=False,
    )


def test_secdef_strikes_missing_conid():
    with pytest.raises(ValueError, match="conid is required"):
        InteractiveBrokersClient.secdef_strikes(month="OCT26")


def test_secdef_strikes_missing_month():
    with pytest.raises(ValueError, match="month is required"):
        InteractiveBrokersClient.secdef_strikes(conid=265598)


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_secdef_info_success(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "conid": 541234567,
            "ticker": "AAPL",
            "secType": "OPT",
            "strike": "195.0",
            "right": "C",
            "maturityDate": "20261016",
        }
    ]
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.secdef_info(
        conid=265598,
        month="OCT26",
        strike=195.0,
        right="C",
        exchange="SMART",
    )

    assert len(res) == 1
    assert res[0]["conid"] == 541234567
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/secdef/info",
        params={
            "conid": 265598,
            "sectype": "OPT",
            "month": "OCT26",
            "exchange": "SMART",
            "strike": 195.0,
            "right": "C",
        },
        headers={"Content-Type": "application/json"},
        verify=False,
    )


@patch("api.ibkr.current_app", new_callable=MagicMock)
@patch("requests.get")
def test_secdef_info_with_args_and_alias(mock_get, mock_app):
    mock_app.config.get.return_value = "https://localhost:5000/v1/api"
    mock_response = MagicMock()
    mock_response.json.return_value = [{"conid": 999888}]
    mock_get.return_value = mock_response

    res = InteractiveBrokersClient.info(
        args={
            "conid": 265598,
            "secType": "OPT",
            "month": "NOV26",
            "right": "PUT",
            "issuerId": "iss_123",
        }
    )

    assert res == [{"conid": 999888}]
    mock_get.assert_called_once_with(
        "https://localhost:5000/v1/api/iserver/secdef/info",
        params={
            "conid": 265598,
            "sectype": "OPT",
            "month": "NOV26",
            "right": "P",
            "issuerId": "iss_123",
        },
        headers={"Content-Type": "application/json"},
        verify=False,
    )


def test_secdef_info_missing_conid():
    with pytest.raises(ValueError, match="conid is required"):
        InteractiveBrokersClient.secdef_info(month="OCT26")




