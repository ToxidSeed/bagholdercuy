import pytest
import pandas as pd
from datetime import date
from unittest.mock import patch, MagicMock
from controller.SerieManager import MassiveSeriesLoader
from service.serie_service import (
    SerieDiariaLoader,
    VariacionDiariaLoader,
    SerieSemanalLoader,
    VariacionSemanalLoader,
    SerieMensualLoader,
    VariacionMensualLoader,
)
from service.resumenserie import ResumenSerieService
from api.massive import MassiveAPI
from config.extensions import db

@patch("api.massive.MassiveAPI.custom_bars")
@patch("service.serie_service.SerieDiariaLoader.load")
@patch("service.serie_service.VariacionDiariaLoader.load")
@patch("service.serie_service.SerieSemanalLoader.load")
@patch("service.serie_service.VariacionSemanalLoader.load")
@patch("service.serie_service.SerieMensualLoader.load")
@patch("service.serie_service.VariacionMensualLoader.load")
@patch("service.resumenserie.ResumenSerieService.guardar")
@patch("config.extensions.db.session.commit")
@patch("config.extensions.db.session.add")
@patch("model.staging_market_data.StagingMarketDataModel.query")
@patch("os.makedirs")
@patch("os.path.getsize")
@patch("builtins.open", new_callable=MagicMock)
def test_massive_loader_success(
    mock_open,
    mock_getsize,
    mock_makedirs,
    mock_query,
    mock_add,
    mock_commit,
    mock_guardar,
    mock_var_mensual,
    mock_serie_mensual,
    mock_var_semanal,
    mock_serie_semanal,
    mock_var_diaria,
    mock_serie_diaria_load,
    mock_custom_bars
):
    # Setup mock returns
    mock_custom_bars.return_value = {
        "status": "OK",
        "ticker": "I:NDX",
        "results": [
            {
                "c": 15000.0,
                "h": 15100.0,
                "l": 14900.0,
                "o": 14950.0,
                "t": 1767225600000  # Unix millisecond timestamp for 2026-01-01
            }
        ]
    }
    mock_serie_diaria_load.return_value = date(2026, 1, 1)
    mock_getsize.return_value = 2048  # 2 KB
    
    mock_staging_entry = MagicMock()
    mock_staging_entry.id_staging = 123
    mock_staging_entry.estado = "PENDIENTE"
    
    # Mock db.session.add to simulate auto-generating id_staging
    def side_effect_add(obj):
        if hasattr(obj, "id_staging"):
            obj.id_staging = 123
    mock_add.side_effect = side_effect_add
    
    # Mock StagingMarketDataModel.query.get(123)
    mock_query.get.return_value = mock_staging_entry

    loader = MassiveSeriesLoader()
    response = loader.load({
        "cod_symbol": "I:NDX",
        "fch_desde": "2026-01-01",
        "fch_hasta": "2026-01-05",
        "modo_carga": "Append"
    })

    # Verify custom_bars call
    mock_custom_bars.assert_called_once_with(
        indices_ticker="I:NDX",
        multiplier=1,
        timespan="day",
        from_date="2026-01-01",
        to_date="2026-01-05"
    )

    # Verify raw file writing was called
    mock_open.assert_called_once()
    mock_makedirs.assert_called_once()
    
    # Verify staging database insert
    assert mock_add.call_count == 1
    added_obj = mock_add.call_args[0][0]
    assert added_obj.proveedor == "MASSIVE"
    assert added_obj.endpoint == "Indices - Custom Bars (OHLC)"
    assert added_obj.ticker == "I:NDX"
    assert added_obj.file_size_kb == 2
    
    # Verify staging state was updated to PROCESADO
    assert mock_staging_entry.estado == "PROCESADO"

    # Verify parsing and data structure passed to SerieDiariaLoader
    assert mock_serie_diaria_load.call_count == 1
    args, kwargs = mock_serie_diaria_load.call_args
    cod_symbol, df, modo_carga = args
    assert cod_symbol == "I:NDX"
    assert modo_carga == "Append"
    assert len(df) == 1
    assert df.loc[0, "fch_serie"] == date(2026, 1, 1)
    assert df.loc[0, "imp_apertura"] == 14950.0
    assert df.loc[0, "imp_cierre"] == 15000.0
    assert df.loc[0, "imp_maximo"] == 15100.0
    assert df.loc[0, "imp_minimo"] == 14900.0
    assert df.loc[0, "volumen"] == 0

    # Verify subsequent loader invocations
    mock_var_diaria.assert_called_once_with("I:NDX", date(2026, 1, 1), "Append")
    mock_serie_semanal.assert_called_once_with("I:NDX", date(2026, 1, 1), "Append")
    mock_var_semanal.assert_called_once_with("I:NDX", date(2026, 1, 1), "Append")
    mock_serie_mensual.assert_called_once_with("I:NDX", date(2026, 1, 1), "Append")
    mock_var_mensual.assert_called_once_with("I:NDX", date(2026, 1, 1), "Append")
    mock_guardar.assert_called_once_with("I:NDX")
    
    # Commit is called twice: once for setting PENDIENTE, once for PROCESADO/business completion
    assert mock_commit.call_count == 2
    
    assert response["success"] is True
    assert response["message"] == "Se ha realizado la carga correctamente"
