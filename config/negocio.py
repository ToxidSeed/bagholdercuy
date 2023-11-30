from enum import Enum
from collections import namedtuple

#Tipos de transacción
TIPO_TRANS_DEPOSITO = 'D'
TIPO_TRANS_RETIRO = 'R'
TIPO_TRANS_CONVERSION = 'C'

#Tipos de Movimiento
TIPO_MOV_INGRESO = 'I'
TIPO_MOV_SALIDA = 'S'

#Indicador de actividad inactividad
IND_ACTIVO = 'S'
IND_INACTIVO = 'N'

#Tipos de Orden
TIPO_ORDEN_COMPRA = 1
TIPO_ORDEN_VENTA = 2

#Tipos de operacion
TIPO_OPERACION_COMPRA = 1
TIPO_OPERACION_VENTA = 2
TIPO_OPERACION_TRANSFERENCIA = 3

#
PAR_OPERACION_MUL = "MUL"
PAR_OPERACION_DIV = "DIV"

#Series 
TIPO_FRECUENCIA_SERIE_DIARIA = "daily"
TIPO_FRECUENCIA_SERIE_SEMANAL = "weekly"
TIPO_FRECUENCIA_SERIE_MENSUAL = "monthly"
SERIES_PROF_CARGA_YTD = "YTD"
SERIES_PROF_CARGA_MAX = "MAX"
SERIES_PROF_CARGA_MESACTUAL = "MESACTUAL"
SERIES_PROF_CARGA_ULT3MESES = "ULT3MESES"
SERIES_PROF_CARGA_ULT6MESES = "ULT6MESES"
NUM_SEMANAS_REPROCESAR_MES = 5
SERIES_PROF_CARGA_ULT1ANYO = "ULT1ANYO"

#Reprocesar 
REPROCESO_PROF_FONDOS_TODO = "TODO"
REPROCESO_PROF_FONDOS_FCH_CIERRE = "FCH_DESDE"

#Tipos de Activo
TIPO_ACTIVO_EQUITY = 1
TIPO_ACTIVO_ETF = 2
TIPO_ACTIVO_OPT = 3
TIPO_ACTIVO_OTROS = 4

class TIPO_VARIACION_EJERCICIO(int, Enum):
    COD_IMPORTE_FIJO = 1
    COD_VARIACION_SUBYACENTE = 2

class TIPO_VARIACION_TITULO(int, Enum):
    COD_IMPORTE = 1
    COD_PORCENTAJE = 2

class IEXCLOUD(Enum):
    PROFUNDIDADES = ["5d", "1m", "3m", "6m", "ytd", "1y", "2y", "5y", "max"]
    RANGOS = [
            ("5d", "" ),
            ("1m", "5d"),
            ("3m", "1m"),
            ("6m", "3m"),
            ("ytd", "6m"),
            ("1y", "ytd"),
            ("2y", "1y"),
            ("5y", "2y"),
            ("max", "5y")
    ]