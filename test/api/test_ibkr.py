import pytest
from unittest.mock import patch, MagicMock
from api.ibkr import InteractiveBrokersClient
from flask import current_app


@pytest.fixture(autouse=True)
def mock_flask_config():
    original_endpoint = current_app.config.get("INTERACTIVE_BROKERS_ENDPOINT")
    current_app.config["INTERACTIVE_BROKERS_ENDPOINT"] = "https://localhost:5000/v1/api"

    yield

    if original_endpoint is not None:
        current_app.config["INTERACTIVE_BROKERS_ENDPOINT"] = original_endpoint
    else:
        current_app.config.pop("INTERACTIVE_BROKERS_ENDPOINT", None)


@patch("requests.post")
def test_secdef_search_positional_and_kwargs(mock_post):
    mock_post.return_value.json.return_value = [
        {
            "conid": 265598,
            "companyHeader": "APPLE INC",
            "symbol": "AAPL",
            "description": "NASDAQ",
            "restricted": None,
            "fop": None,
            "opt": "20261016",
            "war": None,
            "sections": [{"secType": "STK"}],
        }
    ]

    result = InteractiveBrokersClient.secdef_search(
        symbol="AAPL",
        sec_type="STK",
        name=False,
    )

    expected_url = "https://localhost:5000/v1/api/iserver/secdef/search"
    mock_post.assert_called_once_with(
        expected_url,
        json={"symbol": "AAPL", "name": False, "secType": "STK"},
        headers={"Content-Type": "application/json"},
        verify=False,
    )
    assert isinstance(result, list)
    assert result[0]["conid"] == 265598
    assert result[0]["symbol"] == "AAPL"


@patch("requests.post")
def test_secdef_search_dict_args(mock_post):
    mock_post.return_value.json.return_value = [{"conid": 265598, "symbol": "AAPL"}]

    result = InteractiveBrokersClient.secdef_search(
        args={"symbol": "AAPL", "secType": "STK", "more": True}
    )

    expected_url = "https://localhost:5000/v1/api/iserver/secdef/search"
    mock_post.assert_called_once_with(
        expected_url,
        json={"symbol": "AAPL", "secType": "STK", "more": True},
        headers={"Content-Type": "application/json"},
        verify=False,
    )
    assert result[0]["conid"] == 265598


@patch("requests.post")
def test_secdef_search_aliases(mock_post):
    mock_post.return_value.json.return_value = [{"conid": 265598}]

    # Test search alias
    InteractiveBrokersClient.search(symbol="AAPL")
    assert mock_post.call_count == 1

    # Test iserver_secdef_search alias
    InteractiveBrokersClient.iserver_secdef_search(symbol="AAPL")
    assert mock_post.call_count == 2


def test_secdef_search_missing_symbol():
    with pytest.raises(ValueError, match="symbol is required"):
        InteractiveBrokersClient.secdef_search()


@patch("api.ibkr.InteractiveBrokersClient.secdef_search")
def test_ibkr_symbol_controller_get_success(mock_secdef_search):
    from app import app

    mock_secdef_search.return_value = [
        {"conid": 265598, "symbol": "AAPL", "secType": "STK"}
    ]

    client = app.test_client()
    prefix = f"/{app.config.get('BAGHOLDER_APPNAME', 'bagholdercuy')}/api/v2"
    response = client.get(f"{prefix}/ibkr/symbol?symbol=AAPL&name=false&sec_type=STK")

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["data"][0]["conid"] == 265598
    mock_secdef_search.assert_called_once_with(
        symbol="AAPL",
        name=False,
        sec_type="STK",
        more=None,
    )


def test_ibkr_symbol_controller_get_missing_symbol():
    from app import app

    client = app.test_client()
    prefix = f"/{app.config.get('BAGHOLDER_APPNAME', 'bagholdercuy')}/api/v2"
    response = client.get(f"{prefix}/ibkr/symbol")

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] is False
    assert "El parámetro 'symbol' es requerido" in json_data["message"]

