import pytest
from service.variaciondiaria import VariacionDiariaProcesador
from model.seriediaria import SerieDiariaModel
from app import db
from rich import inspect
from datetime import date

class Session:
    def add(self, any):
        return "mocked"

"""
Creación del primer registro de la variación
"""
def test_crear_variacion_diaria(monkeypatch):        
    
    monkeypatch.setattr(db,"session",Session())

    serie_diaria = SerieDiariaModel(
        symbol="SOXL",   
        imp_apertura=14,     
        imp_maximo=25,
        imp_minimo=15,
        imp_cierre=20    
    )    

    new_serie = VariacionDiariaProcesador(cod_symbol="SOXL").crear_variacion_diaria(serie_diaria=serie_diaria)
    # inspect(new_serie)
    assert new_serie.imp_cierre_ant == 0
    assert new_serie.imp_apertura == serie_diaria.imp_apertura
    assert new_serie.imp_maximo == serie_diaria.imp_maximo
    assert new_serie.imp_minimo == serie_diaria.imp_minimo
    assert new_serie.imp_cierre == 20
    assert new_serie.imp_variacion_cierre == 0
    assert new_serie.pct_variacion_cierre == 0
    assert new_serie.imp_variacion_apertura == 0
    assert new_serie.pct_variacion_apertura == 0
    assert new_serie.imp_variacion_maximo == 0
    assert new_serie.pct_variacion_maximo == 0
    assert new_serie.imp_variacion_minimo == 0
    assert new_serie.pct_variacion_minimo == 0

def test_crear_variacion_diaria_2do_registro(monkeypatch):
    monkeypatch.setattr(db,"session",Session())

    serie_ant = SerieDiariaModel(
        symbol="SOXL",   
        fch_serie=date(2024,9,4),
        imp_apertura=14,     
        imp_maximo=25,
        imp_minimo=15,
        imp_cierre=20    
    )    

    serie_diaria = SerieDiariaModel(
        symbol="SOXL",   
        fch_serie=date(2024,9,5),
        imp_apertura=18,     
        imp_maximo=30,
        imp_minimo=17,
        imp_cierre=23   
    )

    new_serie = VariacionDiariaProcesador(cod_symbol="SOXL").crear_variacion_diaria(serie_diaria=serie_diaria, serie_diaria_ant=serie_ant)
    assert new_serie.imp_cierre_ant == 20
    assert new_serie.imp_apertura == 18
    assert new_serie.imp_maximo == 30
    assert new_serie.imp_minimo == 17
    assert new_serie.imp_cierre == 23
    assert new_serie.imp_variacion_apertura == -2
    assert new_serie.pct_variacion_apertura == -10
    assert new_serie.imp_variacion_cierre == 3
    assert new_serie.pct_variacion_cierre == 15
    assert new_serie.imp_variacion_maximo == 10
    assert new_serie.pct_variacion_maximo == 50
    assert new_serie.imp_variacion_minimo == -3
    assert new_serie.pct_variacion_minimo == -15
    assert new_serie.imp_variacion_maximo_minimo == 15

def test_crear_variacion_diaria_fechas(monkeypatch):

    monkeypatch.setattr(db,"session",Session())

    serie_ant = SerieDiariaModel(
        symbol="SOXL",   
        fch_serie=date(2024,9,5),
        imp_apertura=14,     
        imp_maximo=25,
        imp_minimo=15,
        imp_cierre=20    
    )    

    serie_diaria = SerieDiariaModel(
        symbol="SOXL",   
        fch_serie=date(2024,9,4),
        imp_apertura=18,     
        imp_maximo=30,
        imp_minimo=17,
        imp_cierre=23   
    )

    with pytest.raises(Exception):
        VariacionDiariaProcesador(cod_symbol="SOXL").crear_variacion_diaria(serie_diaria=serie_diaria, serie_diaria_ant=serie_ant)
    #with pytest.raises(Exception):
        
