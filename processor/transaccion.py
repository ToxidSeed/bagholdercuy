from app import db
from model.orden import OrdenModel
from model.transaccion import TransaccionModel

from reader.transaccion import TransaccionReader
from reader.calendariodiario import CalendarioDiarioReader

from config.app_constants import TIPO_ORDEN_COMPRA, TIPO_ORDEN_VENTA
from config.app_constants import TIPO_ACTIVO_OPT
from settings import config

from datetime import datetime, date
from sqlalchemy import delete

class TransaccionProcessor:

    def __init__(self):
        self.orden = None
        self.trans_con_saldo = []
        self.ctd_saldo_orden = 0

    def generar_desde_orden(self, orden:OrdenModel):
        try:
            self.orden = orden      

            self.ctd_saldo_orden = self.__get_saldo_orden()
            self.trans_con_saldo = self.__get_transacciones_con_saldo()
            self.__procesar_transacciones_con_saldo()
        except Exception as e:
            raise e

    def __get_saldo_orden(self):
        if self.orden.cod_tipo_orden == TIPO_ORDEN_VENTA:
            return self.orden.cantidad * -1
        else:    
            return self.orden.cantidad

    def __get_transacciones_con_saldo(self):
        if self.orden.cod_tipo_activo == TIPO_ACTIVO_OPT:
            return TransaccionReader.get_transacciones_con_saldo_x_opcion(self.orden.id_cuenta, self.orden.id_contrato_opcion)
        else:
            return TransaccionReader.get_transacciones_con_saldo_x_symbol(self.orden.id_cuenta, self.orden.id_symbol)
    
    def __procesar_transacciones_con_saldo(self):
        for transaccion in self.trans_con_saldo:
            if self.ctd_saldo_orden == 0:
                break

            self.__procesar_transaccion_con_saldo(transaccion)            

        self.__crear_transaccion_remanente_orden(orden=self.orden, ctd_remanente=self.ctd_saldo_orden)

    def __procesar_transaccion_con_saldo(self, transaccion):
        if self.orden.cod_tipo_orden == TIPO_ORDEN_COMPRA:
            self.__comprar(self.ctd_saldo_orden, transaccion)

        if self.orden.cod_tipo_orden == TIPO_ORDEN_VENTA:
            self.__vender(self.ctd_saldo_orden, transaccion)      

    def __comprar(self, ctd_comprar, transaccion:TransaccionModel):
        ctd_comprada = 0

        #Si la posicion es una posicion de compra cuando se quiere cerrar una posicon de venta        
        if transaccion.ctd_saldo_transaccion > 0:
            return 0

        if ctd_comprar >= abs(transaccion.ctd_saldo_transaccion):
            #cantidad es compra (+) y el saldo de la posicion es una venta (-)
            ctd_comprada = abs(transaccion.ctd_saldo_transaccion)

            #El saldo de la posicion
            transaccion.ctd_saldo_transaccion = 0
        else:
            #cantidad es compra (+) y el saldo de la posicion es una venta (-)
            ctd_comprada = ctd_comprar

            #Actualizamos el saldo de la posicion
            transaccion.ctd_saldo_transaccion = transaccion.ctd_saldo_transaccion + ctd_comprar

        #actualizamos el saldo de la orden
        self.ctd_saldo_orden -= ctd_comprada 

        #preparamos la transaccion para insertar
        nueva_transaccion = self.__orden_a_transaccion(orden=self.orden, ctd_nueva_transaccion=ctd_comprada)        
        self.__incluir_referencia(transaccion_nueva=nueva_transaccion, transaccion_referencia=transaccion)        
        db.session.add(nueva_transaccion)     

    def __vender(self, ctd_vender, transaccion:TransaccionModel):
        #ctd_vender es negativo

        ctd_vendida = 0
        #Si la posicion es una posicion de venta no se continua
        if transaccion.ctd_saldo_transaccion < 0:
            return 0

        if abs(ctd_vender) >= transaccion.ctd_saldo_transaccion:
            #cantidad es venta (-) y la posicion es compra (+)
            ctd_vendida = transaccion.ctd_saldo_transaccion * -1

            transaccion.ctd_saldo_transaccion = 0
        else:
            #cantidad es venta (-) y la posicion es compra (+)
            ctd_vendida = ctd_vender

            transaccion.ctd_saldo_transaccion = transaccion.ctd_saldo_transaccion + ctd_vender

        #actualizamos el saldo de la orden
        self.ctd_saldo_orden += abs(ctd_vendida) 

        #preparamos la transaccion para insertar
        nueva_transaccion = self.__orden_a_transaccion(orden=self.orden, ctd_nueva_transaccion=ctd_vendida)                
        self.__incluir_referencia(transaccion_nueva=nueva_transaccion, transaccion_referencia=transaccion)        
        db.session.add(nueva_transaccion)

    def __orden_a_transaccion(self, orden:OrdenModel, ctd_nueva_transaccion=0):
        cod_mes_transaccion = int(orden.fch_orden.strftime("%Y%m"))
        calendariodiario = CalendarioDiarioReader.get(orden.fch_orden)

        transaccion = TransaccionModel()
        transaccion.id_orden = orden.id_orden
        transaccion.num_orden = orden.num_orden
        transaccion.num_orden_transaccion = self.__get_sig_num_transaccion()
        transaccion.id_symbol = orden.id_symbol
        transaccion.id_contrato_opcion = orden.id_contrato_opcion
        transaccion.cod_tipo_activo = orden.cod_tipo_activo
        transaccion.cantidad = ctd_nueva_transaccion
        transaccion.ctd_saldo_transaccion = ctd_nueva_transaccion
        transaccion.id_cuenta = orden.id_cuenta
        transaccion.fch_transaccion = orden.fch_orden
        transaccion.cod_mes_transaccion = cod_mes_transaccion
        transaccion.cod_semana_transaccion = calendariodiario.cod_semana
        transaccion.imp_accion = orden.imp_accion        
        transaccion.imp_accion_origen = 0
        transaccion.imp_rentabilidad = 0
        transaccion.fch_registro = date.today()
        transaccion.hora_registro = datetime.now().time()

        multiplicador = 100 if transaccion.id_contrato_opcion is not None else 1
        transaccion.imp_transaccion = transaccion.cantidad * transaccion.imp_accion * multiplicador

        return transaccion        

    def __incluir_referencia(self, transaccion_nueva:TransaccionModel, transaccion_referencia:TransaccionModel):                
        transaccion_nueva.ctd_saldo_transaccion = 0    
        transaccion_nueva.id_transaccion_ref = transaccion_referencia.id_transaccion
        transaccion_nueva.imp_accion_origen = float(transaccion_referencia.imp_accion)
        transaccion_nueva.imp_rentabilidad = self.__calcular_rentabilidad(transaccion_nueva=transaccion_nueva)    

    def __calcular_rentabilidad(self, transaccion_nueva:TransaccionModel):
        multiplicador = 100 if transaccion_nueva.id_contrato_opcion is not None else 1
        imp_rentabilidad = 0

        #Si es una venta
        if transaccion_nueva.cantidad < 0:
            imp_rentabilidad = abs(transaccion_nueva.cantidad) * transaccion_nueva.imp_accion * multiplicador - abs(transaccion_nueva.cantidad) * transaccion_nueva.imp_accion_origen * multiplicador           
        else:
            imp_rentabilidad = abs(transaccion_nueva.cantidad) * transaccion_nueva.imp_accion_origen * multiplicador - abs(transaccion_nueva.cantidad) * transaccion_nueva.imp_accion * multiplicador

        return imp_rentabilidad


    def __crear_transaccion_remanente_orden(self, orden:OrdenModel, ctd_remanente):
        if ctd_remanente != 0:
            transaccion = self.__orden_a_transaccion(orden=orden, ctd_nueva_transaccion=ctd_remanente)
            transaccion.cantidad = ctd_remanente
            transaccion.ctd_saldo_transaccion = ctd_remanente
            db.session.add(transaccion)
    
    def __get_sig_num_transaccion(self):
        num_transaccion =  TransaccionReader.get_max_num_posicion(self.orden.id_cuenta, self.orden.fch_orden)
        num_transaccion+=1        
        return num_transaccion

class TransaccionEliminador:
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
    
