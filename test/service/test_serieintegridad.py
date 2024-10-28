import pytest
from model.seriediaria import SerieDiariaModel
from model.stocksplit import StockSplitModel
from datetime import date, datetime
from manager.serieintegridad import SerieDiariaIntegridad
# from reader.seriediaria import SerieDiariaReader


class TestSerieDiariaIntegridad:
    def test_eval_single_split(self, mocker):
        serie1 = SerieDiariaModel()
        mocker.patch("reader.seriediaria.SerieDiariaReader.get_serie", return_value=serie1)

        serie2 = SerieDiariaModel()
        mocker.patch("reader.seriediaria.SerieDiariaReader.get_serie_anterior_a_fecha", return_value=serie2)

        stock_split = StockSplitModel(
            id_symbol=1,
            fch_split=date(2023,12,4),
            numerador=1,
            denominador=20
        )
        
        serie_diaria_integridad = SerieDiariaIntegridad()
        flg_ok, fch_split = serie_diaria_integridad.eval_single_split(split=stock_split)
        
        assert flg_ok is True
        assert fch_split is None

        