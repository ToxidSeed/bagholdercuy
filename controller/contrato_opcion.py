"""
Módulo legado contrato_opcion.
Redirige y re-exporta los controladores y servicios hacia contrato_opcion_controller.py
de acuerdo con docs/CONTROLLER.md.
"""

from controller.contrato_opcion_controller import (
    ContratoOpcionController,
    ContratoOpcionChainController,
    ContratoOpcionResumenController,
    ContratoOpcionLoaderMarketDataController,
    ContratoOpcionLoaderCsvController,
    SymbolLoader,
    CsvLoader,
    OpcionesContratoManager,
    init_module,
)

__all__ = [
    "ContratoOpcionController",
    "ContratoOpcionChainController",
    "ContratoOpcionResumenController",
    "ContratoOpcionLoaderMarketDataController",
    "ContratoOpcionLoaderCsvController",
    "SymbolLoader",
    "CsvLoader",
    "OpcionesContratoManager",
    "init_module",
]
