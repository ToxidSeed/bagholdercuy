import pytest
import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import date
from controller.SerieManager import InvestingLoader
from service.serie_service import SerieDiariaLoader

def test_investing_loader_spanish_decimals(monkeypatch):
    # Mock SerieDiariaLoader.load to do nothing
    monkeypatch.setattr(SerieDiariaLoader, "load", lambda self, cod_symbol, df, modo_carga: None)

    # Sample dataframe imitating the structure read by read_csv from Investing.com Spanish CSV
    # Test strings, float/int inputs, and missing/NaN values
    data = {
        "Fecha": ["13.07.2026", "10.07.2026", "09.07.2026", "08.07.2026"],
        "Último": ["7.003,66", 7000.50, None, np.nan],
        "Apertura": ["7.001", 6999.99, None, np.nan],
        "Máximo": ["7.010,00", 7005, None, np.nan],
        "Mínimo": ["6.995,00", 6990, None, np.nan]
    }
    df = pd.DataFrame(data)

    loader = InvestingLoader()
    result_df, fch_max, fch_min = loader.load_series_diarias("TEST_SYM", df, "Agregar")

    # Assert correct date conversion
    assert fch_max == date(2026, 7, 13)
    assert fch_min == date(2026, 7, 8)

    # Assert Decimal conversions for Último (imp_cierre)
    assert result_df.loc[0, "imp_cierre"] == Decimal("7003.66")
    assert result_df.loc[1, "imp_cierre"] == Decimal("7000.50")
    assert result_df.loc[2, "imp_cierre"] is None
    assert result_df.loc[3, "imp_cierre"] is None

    # Assert Decimal conversions for Apertura (imp_apertura)
    assert result_df.loc[0, "imp_apertura"] == Decimal("7001")
    assert result_df.loc[1, "imp_apertura"] == Decimal("6999.99")
    assert result_df.loc[2, "imp_apertura"] is None
    assert result_df.loc[3, "imp_apertura"] is None

    # Assert Decimal conversions for Máximo (imp_maximo)
    assert result_df.loc[0, "imp_maximo"] == Decimal("7010.00")
    assert result_df.loc[1, "imp_maximo"] == Decimal("7005")
    assert result_df.loc[2, "imp_maximo"] is None
    assert result_df.loc[3, "imp_maximo"] is None

    # Assert Decimal conversions for Mínimo (imp_minimo)
    assert result_df.loc[0, "imp_minimo"] == Decimal("6995.00")
    assert result_df.loc[1, "imp_minimo"] == Decimal("6990")
    assert result_df.loc[2, "imp_minimo"] is None
    assert result_df.loc[3, "imp_minimo"] is None
