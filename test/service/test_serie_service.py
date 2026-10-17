from datetime import date
from unittest.mock import patch

from model.symbol import SymbolModel
from service.serie.serie_service import SerieService


@patch("service.serie.serie_service.ResumenSerieService")
@patch("service.serie.serie_service.VariacionMensualService")
@patch("service.serie.serie_service.SerieMensualService")
@patch("service.serie.serie_service.VariacionSemanalService")
@patch("service.serie.serie_service.SerieSemanalService")
@patch("service.serie.serie_service.VariacionDiariaService")
@patch("service.serie.serie_service.InteractiveBrokersSerieService")
@patch("service.serie.serie_service.SymbolReader")
def test_sincronize_resolves_symbol_and_delegates_to_ibkr(
    mock_symbol_reader,
    mock_ibkr_service,
    mock_var_diaria,
    mock_serie_semanal,
    mock_var_semanal,
    mock_serie_mensual,
    mock_var_mensual,
    mock_resumen_service,
):
    symbol = SymbolModel(symbol="AAPL")
    mock_symbol_reader.return_value.get.return_value = symbol
    expected_result = (date(2023, 1, 2), date(2023, 1, 3))
    mock_ibkr_service.return_value.load.return_value = expected_result

    result = SerieService().sincronize(
        market_data_provider="IBKR",
        cod_symbol="AAPL",
        fch_desde=date(2023, 1, 1),
        fch_hasta=date(2023, 1, 5),
        modo_carga="APPEND",
    )

    assert result == expected_result
    mock_symbol_reader.return_value.get.assert_called_once_with(
        cod_symbol="AAPL",
        not_found_error=True,
    )
    mock_ibkr_service.return_value.load.assert_called_once_with(
        symbol=symbol,
        fch_desde=date(2023, 1, 1),
        fch_hasta=date(2023, 1, 5),
        modo_carga="APPEND",
    )
    mock_var_diaria.return_value.generar_variaciones.assert_called_once_with(
        "AAPL", date(2023, 1, 2)
    )
    mock_serie_semanal.return_value.generar_series.assert_called_once_with(
        "AAPL", date(2023, 1, 2)
    )
    mock_var_semanal.return_value.generar_series.assert_called_once_with(
        "AAPL", date(2023, 1, 2)
    )
    mock_serie_mensual.return_value.generar_series.assert_called_once_with(
        "AAPL", date(2023, 1, 2)
    )
    mock_var_mensual.return_value.generar_series.assert_called_once_with(
        "AAPL", date(2023, 1, 2)
    )
    mock_resumen_service.return_value.guardar.assert_called_once_with("AAPL")


@patch("service.serie.serie_service.ResumenSerieService")
@patch("service.serie.serie_service.VariacionMensualService")
@patch("service.serie.serie_service.SerieMensualService")
@patch("service.serie.serie_service.VariacionSemanalService")
@patch("service.serie.serie_service.SerieSemanalService")
@patch("service.serie.serie_service.VariacionDiariaService")
@patch("service.serie.serie_service.InteractiveBrokersSerieService")
@patch("service.serie.serie_service.SymbolReader")
def test_sincronize_with_explicit_provider_and_positional_args(
    mock_symbol_reader,
    mock_ibkr_service,
    mock_var_diaria,
    mock_serie_semanal,
    mock_var_semanal,
    mock_serie_mensual,
    mock_var_mensual,
    mock_resumen_service,
):
    symbol = SymbolModel(symbol="MSFT")
    mock_symbol_reader.return_value.get.return_value = symbol
    expected_result = (date(2023, 2, 1), date(2023, 2, 10))
    mock_ibkr_service.return_value.load.return_value = expected_result

    result = SerieService().sincronize(
        "IBKR",
        "MSFT",
        date(2023, 2, 1),
        date(2023, 2, 10),
        "REPLACE",
    )

    assert result == expected_result
    mock_symbol_reader.return_value.get.assert_called_once_with(
        cod_symbol="MSFT",
        not_found_error=True,
    )
    mock_ibkr_service.return_value.load.assert_called_once_with(
        symbol=symbol,
        fch_desde=date(2023, 2, 1),
        fch_hasta=date(2023, 2, 10),
        modo_carga="REPLACE",
    )
    mock_var_diaria.return_value.generar_variaciones.assert_called_once_with(
        "MSFT", date(2023, 2, 1)
    )
    mock_serie_semanal.return_value.generar_series.assert_called_once_with(
        "MSFT", date(2023, 2, 1)
    )
    mock_var_semanal.return_value.generar_series.assert_called_once_with(
        "MSFT", date(2023, 2, 1)
    )
    mock_serie_mensual.return_value.generar_series.assert_called_once_with(
        "MSFT", date(2023, 2, 1)
    )
    mock_var_mensual.return_value.generar_series.assert_called_once_with(
        "MSFT", date(2023, 2, 1)
    )
    mock_resumen_service.return_value.guardar.assert_called_once_with("MSFT")


def test_sincronize_unsupported_provider():
    import pytest
    from common.AppException import AppException

    with pytest.raises(AppException) as exc_info:
        SerieService().sincronize(
            market_data_provider="UNKNOWN_PROVIDER",
            cod_symbol="AAPL",
            fch_desde=date(2023, 1, 1),
            fch_hasta=date(2023, 1, 5),
            modo_carga="APPEND",
        )
    assert "no soportado" in exc_info.value.msg


@patch("service.serie.serie_service.SymbolReader")
def test_sincronize_symbol_not_found_raises_app_exception(mock_symbol_reader):
    import pytest
    from common.AppException import AppException

    mock_symbol_reader.return_value.get.side_effect = AppException(
        msg="No se ha encontrado symbol para NONEXISTENT"
    )

    with pytest.raises(AppException) as exc_info:
        SerieService().sincronize(
            market_data_provider="IBKR",
            cod_symbol="NONEXISTENT",
            fch_desde=date(2023, 1, 1),
            fch_hasta=date(2023, 1, 5),
            modo_carga="APPEND",
        )

    assert "No se ha encontrado symbol para NONEXISTENT" in exc_info.value.msg


def test_get_provider_class_ibkr():
    from service.markets_data_providers.ibkr.ibkr_serie_service import (
        InteractiveBrokersSerieService,
    )

    cls = SerieService()._get_provider_class("IBKR")
    assert cls is InteractiveBrokersSerieService


@patch("service.serie.serie_service.ResumenSerieService")
@patch("service.serie.serie_service.VariacionMensualService")
@patch("service.serie.serie_service.SerieMensualService")
@patch("service.serie.serie_service.VariacionSemanalService")
@patch("service.serie.serie_service.SerieSemanalService")
@patch("service.serie.serie_service.VariacionDiariaService")
@patch("service.serie.serie_service.InteractiveBrokersSerieService")
@patch("service.serie.serie_service.SymbolReader")
def test_sincronize_no_series_loaded_skips_variaciones_and_series(
    mock_symbol_reader,
    mock_ibkr_service,
    mock_var_diaria,
    mock_serie_semanal,
    mock_var_semanal,
    mock_serie_mensual,
    mock_var_mensual,
    mock_resumen_service,
):
    symbol = SymbolModel(symbol="AAPL")
    mock_symbol_reader.return_value.get.return_value = symbol
    mock_ibkr_service.return_value.load.return_value = (None, None)

    result = SerieService().sincronize(
        market_data_provider="IBKR",
        cod_symbol="AAPL",
        fch_desde=date(2023, 1, 1),
        fch_hasta=date(2023, 1, 5),
        modo_carga="APPEND",
    )

    assert result == (None, None)
    mock_var_diaria.return_value.generar_variaciones.assert_not_called()
    mock_serie_semanal.return_value.generar_series.assert_not_called()
    mock_var_semanal.return_value.generar_series.assert_not_called()
    mock_serie_mensual.return_value.generar_series.assert_not_called()
    mock_var_mensual.return_value.generar_series.assert_not_called()
    mock_resumen_service.return_value.guardar.assert_called_once_with("AAPL")
