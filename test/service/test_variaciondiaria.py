import pytest
from model.seriediaria import SerieDiariaModel
from service.variaciondiaria import VariacionDiariaService
from app import db
from rich import inspect
from datetime import date

class Session:
    def add(self, any):
        return "mocked"


def test_crear_variacion_diaria_2do_registro(monkeypatch):
    monkeypatch.setattr(db,"session",Session())

    serie_ant = SerieDiariaModel(
        cod_symbol="SOXL",   
        fch_serie=date(2024,9,4),
        imp_apertura=14,     
        imp_maximo=25,
        imp_minimo=15,
        imp_cierre=20    
    )    

    serie_diaria = SerieDiariaModel(
        cod_symbol="SOXL",   
        fch_serie=date(2024,9,5),
        imp_apertura=18,     
        imp_maximo=30,
        imp_minimo=17,
        imp_cierre=23   
    )

    assert(True)

def test_crear_variacion_diaria_fechas(monkeypatch):

    monkeypatch.setattr(db,"session",Session())

    serie_ant = SerieDiariaModel(
        cod_symbol="SOXL",   
        fch_serie=date(2024,9,5),
        imp_apertura=14,     
        imp_maximo=25,
        imp_minimo=15,
        imp_cierre=20    
    )    

    serie_diaria = SerieDiariaModel(
        cod_symbol="SOXL",   
        fch_serie=date(2024,9,4),
        imp_apertura=18,     
        imp_maximo=30,
        imp_minimo=17,
        imp_cierre=23   
    )

    assert(True)

def test_generar_variacion(monkeypatch):
    vds = VariacionDiariaService()
    vds.generar_variaciones(cod_symbol="SOXL", fch_serie_inicial=date(2024,5,5))

        
