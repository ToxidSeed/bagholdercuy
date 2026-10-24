import pytest
from unittest.mock import patch, MagicMock
from parser.symbol import SymbolFinderParser
from controller.SymbolManager import SymbolFinder
from model.symbol import SymbolModel


def test_symbol_finder_parser_parse_args_get_list():
    args = {"cod_symbol": "AAPL", "name": "Apple Inc", "id_symbol": "10"}
    parsed = SymbolFinderParser.parse_args_get_list(args=args)

    assert parsed["cod_symbol"] == "AAPL"
    assert parsed["name"] == "Apple Inc"
    assert parsed["id_symbol"] == 10


def test_symbol_finder_parser_parse_args_get_list_nombre_fallback():
    args = {"nombre": "Apple Inc"}
    parsed = SymbolFinderParser.parse_args_get_list(args=args)

    assert parsed["name"] == "Apple Inc"


@patch("reader.symbol.SymbolReader.get_list")
def test_symbol_finder_get_list(mock_get_list):
    item = SymbolModel(
        id_symbol=31,
        symbol="AAPL",
        name="Apple Inc",
        region="US",
        exchange="XNAS",
        asset_type="EQUITY"
    )
    mock_get_list.return_value = [item]

    res = SymbolFinder().get_list({"name": "Apple", "cod_symbol": "AAPL"})
    assert res["success"] is True
    assert len(res["data"]) == 1
    assert res["data"][0]["id_symbol"] == 31
    assert res["data"][0]["symbol"] == "AAPL"
    assert res["data"][0]["name"] == "Apple Inc"

    mock_get_list.assert_called_once()
    call_args = mock_get_list.call_args[1].get("args") if "args" in mock_get_list.call_args[1] else mock_get_list.call_args[0][0]
    assert call_args["name"] == "Apple"
    assert call_args["cod_symbol"] == "AAPL"
