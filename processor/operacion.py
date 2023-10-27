from model.orden import OrdenModel
from model.operacion import OperacionModel
from model.posicion import PosicionModel

from reader.operacion import OperacionReader
from reader.posicion import PosicionReader
from config.negocio import TIPO_ORDEN_COMPRA, TIPO_ORDEN_VENTA
from datetime import date, datetime

from app import db

class OperacionProcessor:   
    def __init__(self):
        pass

    def procesar_orden(self, orden:OrdenModel, posicion:PosicionModel=None, operacion:OperacionModel=None, num_orden_operacion=None):

        ctd_operacion = (orden.cantidad if orden.cod_tipo_orden == TIPO_ORDEN_COMPRA else orden.cantidad * -1)
        nom_tipo_orden = "Compra" if orden.cod_tipo_orden == TIPO_ORDEN_COMPRA else "Venta"
        dsc_glosa_operacion = f"{nom_tipo_orden}: {ctd_operacion} x {orden.imp_accion}"

        if num_orden_operacion is None:
            num_orden_operacion = self.__get_siguiente_num_orden_operacion(orden.id_cuenta, orden.fch_orden)
        
        #posicion = self.__get_posicion(id_cuenta=orden.id_cuenta, id_symbol=orden.id_symbol, id_contrato_opcion=orden.id_contrato_opcion)
        if operacion is None:
            ctd_nueva_posicion = ctd_operacion if posicion is None else posicion.cantidad
        else:
            ctd_nueva_posicion = operacion.ctd_posicion + ctd_operacion

        oper = OperacionModel(
            id_cuenta = orden.id_cuenta,
            fch_operacion = orden.fch_orden,
            num_orden = num_orden_operacion,
            id_tipo_operacion = orden.cod_tipo_orden,
            id_symbol = orden.id_symbol,
            id_contrato_opcion = orden.id_contrato_opcion,
            cantidad = ctd_operacion,
            ctd_posicion = ctd_nueva_posicion,
            dsc_glosa_operacion = dsc_glosa_operacion,
            fch_registro = date.today()
        )

        db.session.add(oper)
        return oper        
    
    def __get_ctd_posicion(self, posicion:PosicionModel, operacion:OperacionModel):
        pass

    def __get_siguiente_num_orden_operacion(self, id_cuenta, fch_operacion):                        
        max_num_orden = OperacionReader.get_max_num_orden(id_cuenta=id_cuenta, fch_operacion=fch_operacion)
        num_orden_operacion = max_num_orden + 1
        return num_orden_operacion
            


        
        
        
    

        
