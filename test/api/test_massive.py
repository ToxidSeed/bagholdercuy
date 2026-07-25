import pytest
from unittest.mock import patch, MagicMock
from api.massive import MassiveAPI
from flask import current_app

@pytest.fixture(autouse=True)
def mock_flask_config():
    original_endpoint = current_app.config.get("MASSIVE_ENDPOINT")
    original_token = current_app.config.get("MASSIVE_API_TOKEN")
    
    current_app.config["MASSIVE_ENDPOINT"] = "https://api.massive.com"
    current_app.config["MASSIVE_API_TOKEN"] = "test_token_12345"
    
    yield
    
    if original_endpoint is not None:
        current_app.config["MASSIVE_ENDPOINT"] = original_endpoint
    else:
        current_app.config.pop("MASSIVE_ENDPOINT", None)
        
    if original_token is not None:
        current_app.config["MASSIVE_API_TOKEN"] = original_token
    else:
        current_app.config.pop("MASSIVE_API_TOKEN", None)

def test_massive_api_init():
    api = MassiveAPI()
    assert api.base_endpoint == "https://api.massive.com"
    assert api.token == "test_token_12345"

@patch("requests.get")
def test_massive_custom_bars_positional_args(mock_get):
    mock_get.return_value.json.return_value = {"status": "OK", "results": []}

    api = MassiveAPI()
    result = api.custom_bars(
        indices_ticker="I:NDX",
        multiplier=1,
        timespan="day",
        from_date="2026-01-01",
        to_date="2026-01-10",
        sort="asc",
        limit=100
    )

    expected_url = "https://api.massive.com/v2/aggs/ticker/I:NDX/range/1/day/2026-01-01/2026-01-10"
    mock_get.assert_called_once_with(
        expected_url,
        params={
            "sort": "asc",
            "limit": 100,
            "apiKey": "test_token_12345"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer test_token_12345"
        }
    )
    assert result["status"] == "OK"

@patch("requests.get")
def test_massive_custom_bars_dict_args(mock_get):
    mock_get.return_value.json.return_value = {"status": "OK"}

    api = MassiveAPI()
    result = api.custom_bars(
        args={
            "indicesTicker": "I:SPX",
            "multiplier": 5,
            "timespan": "minute",
            "from": "1678341600000",
            "to": "1678428000000",
            "sort": "desc",
            "limit": 500
        }
    )

    expected_url = "https://api.massive.com/v2/aggs/ticker/I:SPX/range/5/minute/1678341600000/1678428000000"
    mock_get.assert_called_once_with(
        expected_url,
        params={
            "sort": "desc",
            "limit": 500,
            "apiKey": "test_token_12345"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer test_token_12345"
        }
    )
    assert result["status"] == "OK"

def test_massive_custom_bars_missing_args():
    api = MassiveAPI()
    with pytest.raises(ValueError, match="indicesTicker is required"):
        api.custom_bars(multiplier=1, timespan="day", from_date="2026-01-01", to_date="2026-01-10")

    with pytest.raises(ValueError, match="multiplier is required"):
        api.custom_bars(indices_ticker="I:NDX", timespan="day", from_date="2026-01-01", to_date="2026-01-10")

    with pytest.raises(ValueError, match="timespan is required"):
        api.custom_bars(indices_ticker="I:NDX", multiplier=1, from_date="2026-01-01", to_date="2026-01-10")

    with pytest.raises(ValueError, match="from \\(start date/timestamp\\) is required"):
        api.custom_bars(indices_ticker="I:NDX", multiplier=1, timespan="day", to_date="2026-01-10")

    with pytest.raises(ValueError, match="to \\(end date/timestamp\\) is required"):
        api.custom_bars(indices_ticker="I:NDX", multiplier=1, timespan="day", from_date="2026-01-01")
