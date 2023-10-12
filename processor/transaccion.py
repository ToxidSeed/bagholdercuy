from app import db
from model.orden import OrdenModel
from model.transaccion import TransaccionModel

from reader.transaccion import TransaccionReader

from config.negocio import ORDEN_TIPO_COMPRA, ORDEN_TIPO_VENTA
from config.negocio import TIPO_ACTIVO_OPT
from settings import config

from datetime import datetime
from sqlalchemy import delete

class TransaccionProcessor:

    def __init__(self):
        self.orden = None
        self.trans_con_saldo = []
        self.ctd_saldo_orden = 0

    def generar_desde_orden(self, orden:OrdenModel):
        try:
            self.orden = orden      
            num_orden = orden.num_orden
            cod_opcion = orden.cod_opcion

            self.ctd_saldo_orden = orden.cantidad if orden.cod_tipo_orden == config.get("tipo.orden","compra") else orden.cantidad * -1    
            self.trans_con_saldo = self.__get_transacciones_con_saldo()
            self.__gen_posiciones()
        except Exception as e:
            raise e

    def __get_transacciones_con_saldo(self):
        if str(self.orden.cod_tipo_activo) == str(config.get("tipo.activo","opcion")):
            return TransaccionReader.get_posiciones_abiertas_x_opcion(self.orden.usuario_id, self.orden.cod_opcion)
        else:
            return TransaccionReader.get_posiciones_abiertas_x_symbol(self.orden.usuario_id, self.orden.cod_symbol)
    
    def __gen_posiciones(self):
        for posicion in self.posiciones:
            if self.ctd_saldo_orden == 0:
                break

            self.__procesar_posicion(posicion)            

        #si aun hay saldo de la orden se crea la operacion correspondiente por el total
        if self.ctd_saldo_orden != 0:
            PosicionWriter().insertar(self.orden, self.ctd_saldo_orden)

    def __procesar_posicion(self, posicion:TransaccionModel):
        ctd_nueva_posicion = self.__cerrar(posicion, self.orden, self.ctd_saldo_orden)

        if ctd_nueva_posicion == 0:
            return
        
        #Actualizar el saldo de la orden
        self.ctd_saldo_orden = self.ctd_saldo_orden - ctd_nueva_posicion
        
        #Crear posicion        
        PosicionWriter().insertar(self.orden, ctd_nueva_posicion, pos_referencia=posicion)          

    def __cerrar(self, posicion:TransaccionModel, orden:OrdenModel, cantidad):
        if orden.cod_tipo_orden == ORDEN_TIPO_COMPRA:
            return self.__cerrar_venta(posicion, cantidad)

        if orden.cod_tipo_orden == ORDEN_TIPO_VENTA:
            return self.__cerrar_compra(posicion, cantidad)

    def __cerrar_venta(self, posicion:TransaccionModel, cantidad):
        ctd_cierre = 0

        #Si la posicion es una posicion de compra cuando se quiere cerrar una posicon de venta        
        if posicion.ctd_saldo_posicion > 0:
            return 0

        if cantidad >= abs(posicion.ctd_saldo_posicion):
            #cantidad es compra (+) y el saldo de la posicion es una venta (-)
            ctd_cierre = abs(posicion.ctd_saldo_posicion)

            #El saldo de la posicion
            posicion.ctd_saldo_posicion = 0
        else:
            #cantidad es compra (+) y el saldo de la posicion es una venta (-)
            ctd_cierre = cantidad

            #Actualizamos el saldo de la posicion
            posicion.ctd_saldo_posicion = posicion.ctd_saldo_posicion + cantidad

        return ctd_cierre

    def __cerrar_compra(self, posicion:TransaccionModel, cantidad):

        ctd_cierre = 0
        #Si la posicion es una posicion de venta no se continua
        if posicion.ctd_saldo_posicion < 0:
            return 0

        if abs(cantidad) >= posicion.ctd_saldo_posicion:
            #cantidad es venta (-) y la posicion es compra (+)
            ctd_cierre = posicion.ctd_saldo_posicion * -1

            posicion.ctd_saldo_posicion = 0
        else:
            #cantidad es venta (-) y la posicion es compra (+)
            ctd_cierre = cantidad

            posicion.ctd_saldo_posicion = posicion.ctd_saldo_posicion + cantidad

        return ctd_cierre

class PosicionEliminador:
    def eliminar_x_opcion(usuario_id, cod_opcion):
        stmt = delete(
            TransaccionModel
        ).where(
            TransaccionModel.usuario_id == usuario_id,
            TransaccionModel.cod_opcion == cod_opcion
        )

        db.session.execute(stmt)

    def eliminar_x_otros_activos(usuario_id, cod_symbol):
        stmt = delete(
            TransaccionModel
        ).where(
            TransaccionModel.usuario_id == usuario_id,
            TransaccionModel.cod_symbol == cod_symbol
        )

        db.session.execute(stmt)

    def eliminar_todo(usuario_id):
        stmt = delete(
            TransaccionModel
        ).where(
            TransaccionModel.usuario_id == usuario_id
        )
        
        db.session.execute(stmt)
    
class PosicionWriter:
    def __init__(self):
        self.orden = None

    def insertar(self, orden:OrdenModel, ctd_operacion, pos_referencia:TransaccionModel=None):

        self.orden = orden      

        #default valores
        imp_accion = float(orden.imp_accion)    
        ctd_operacion = int(ctd_operacion)    

        """
        ctd_saldo_posicion = ctd_operacion        
        imp_accion_origen = 0
        imp_gp_realizada = 0
        imp_posicion = imp_accion * ctd_operacion
        posicion_ref_id = None
        """

        if pos_referencia is None:
            ctd_saldo_posicion = ctd_operacion
            imp_accion_origen = 0
            imp_gp_realizada = 0
            posicion_ref_id = None

            if orden.cod_tipo_activo == int(config.get("tipo.activo","opcion")):
                imp_posicion = imp_accion * 100 * ctd_operacion
            else:
                imp_posicion = imp_accion * ctd_operacion
            
        else:
            ctd_saldo_posicion = 0            
            imp_accion_origen = pos_referencia.imp_accion            
            posicion_ref_id = pos_referencia.id
        
            if orden.cod_tipo_activo == int(config.get("tipo.activo","opcion")):
                imp_posicion = imp_accion * 100 * ctd_operacion
                imp_gp_realizada = float(ctd_operacion * imp_accion_origen * 100) - float(ctd_operacion * imp_accion * 100)
            else:
                imp_posicion = imp_accion * ctd_operacion
                imp_gp_realizada = float(ctd_operacion * imp_accion_origen) - float(ctd_operacion * imp_accion)
                
        
        posicion = TransaccionModel(            
            orden_id = orden.orden_id,
            num_orden = orden.num_orden,            
            num_posicion=self.__get_sig_num_posicion(),
            cod_symbol=orden.cod_symbol,
            cod_opcion=orden.cod_opcion,
            cod_tipo_orden = orden.cod_tipo_orden,            
            cod_tipo_activo = orden.cod_tipo_activo,
            cantidad = ctd_operacion,                
            ctd_saldo_posicion = ctd_saldo_posicion,     
            fch_transaccion = orden.fch_orden,
            num_mes_posicion = orden.fch_orden.month,
            imp_accion = imp_accion,
            posicion_ref_id = posicion_ref_id,
            imp_accion_origen = imp_accion_origen,    
            imp_gp_realizada = imp_gp_realizada,  
            imp_posicion = imp_posicion,            
            fch_registro = datetime.now().date(),
            hora_registro = datetime.now().time(),            
            usuario_id = orden.usuario_id            
        )        
        
        try:
            db.session.add(posicion)
            db.session.flush()
        except Exception as e:
            raise e
        

    def __get_sig_num_posicion(self):
        num_posicion =  TransaccionReader.get_max_num_posicion(self.orden.usuario_id, self.orden.fch_orden, self.orden.cod_symbol, self.orden.cod_opcion)
        if num_posicion is None:
            return 1
        else:
            num_posicion+=1
        
        return num_posicion


