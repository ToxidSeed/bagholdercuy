from app import app, db

from datetime import datetime, date, time
from common.AppException import AppException
from common.Response import Response
from domain.mes import Mes
from domain.semana import CodigoSemana

#from model.orden import OrdenModel
from model.StockSymbol import StockSymbol
from model.transaccion import TransaccionModel

from service.transaccion import TransaccionService

#from processor.orden import OrdenProcessor, CargadorMultipleProcessor, ReprocesadorOrdenesProcessor
#from service.orden import OrdenService

from reader.symbol import SymbolReader
#from reader.orden import OrdenReader

from controller.base import Base

import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract

import json, csv

from schemas.orden_schema import OrdenManagerEjecutarParams

# params = CicloVariacionGetCiclosDiarios(**args)

class OrdenController(Base):

    def ejecutar(self, args={}):
        try:
            params = OrdenManagerEjecutarParams(**args)            
            transaccion = self.__parse_params(params)                        
            TransaccionService().registrar(transaccion)
            db.session.commit()
            return Response(msg="la orden se procesó correctamente").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def __parse_params(self, params: OrdenManagerEjecutarParams):
        now = datetime.now()
        transaccion = TransaccionModel(
            cod_symbol = params.cod_symbol,
            id_instrumento_financiero = params.id_instrumento_financiero,            
            id_tipo_transaccion = params.id_tipo_transaccion,
            fch_transaccion = params.fch_transaccion,
            cantidad = params.cantidad,
            imp_unitario = params.imp_accion,
            imp_transaccion = params.imp_accion * params.cantidad,
            fch_hr_registro = datetime.now(),
            id_cuenta = 3         
        )

        return transaccion



"""
class ProcesadorEntryPoint(OrdenManager):
    def __init__(self):
        pass

    def procesar(self, args={}):
        try:
            procesador = OrdenProcessor()
            self._validar_procesar(args)
            orden = self._collect(args)            
            procesador.ejecutar(orden)
            db.session.commit()
            return Response(msg="la orden se procesó correctamente").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)                 
"""

class ReprocesadorEntryPoint:
    def __init__(self):
        pass

    def reprocesar(self, args={}):
        try:

            db.session.commit()
            return Response(msg="Se han reprocesado los symbols de forma correcta")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def reprocesar_todo(self, args={}):
        try:
            reprocesador = Reprocesador()
            reprocesador.reprocesar_todo()
            db.session.commit()
            return Response(msg="Se ha reprocesado todo de forma correcta")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)



class EliminadorEntryPoint:
    def __init__(self):
        pass

    def procesar(self, args={}):
        try:
            self._validar(args=args)
            eliminador = Eliminador()
            eliminador.procesar(args["ids_ordenes"])
            db.session.commit()
            return Response(msg="Se ha eliminado correctamente la lista de ordenes").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def _validar(self, args={}):
        errors = []
        if "ids_ordenes" not in args:
            errors.append("El parámetro 'ids_ordenes' no ha sido enviado en la petición")
        else:
            ids_ordenes = args["ids_ordenes"]
            if len(ids_ordenes) == 0:
                errors.append("No se ha indicado ninguna orden a eliminar")

        if len(errors) > 0:
            raise AppException(msg="Se han encontrado errores de entrada en la petición", errors=errors)

