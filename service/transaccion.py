from constants.tipo_transaccion import get_tipo_transaccion
from reader.movimiento_saldo import MovimientoSaldoReader
from reader.transaccion_saldo import TransaccionSaldoReader
from reader.transaccion import TransaccionReader
from model.transaccion import TransaccionModel
from model.transaccion_saldo import TransaccionSaldoModel
from model.movimiento_saldo import MovimientoSaldoModel
from app import db
import uuid

"""
La clase CompraGeneric es un servicio que se encarga de registrar transacciones de compra.

"""

class CompraGeneric:
    def __init__(self):
        pass

    def registrar(self, transaccion: TransaccionModel):        
        if transaccion.orden_fifo is None:
            transaccion.orden_fifo = TransaccionReader.get_next_orden_fifo(transaccion.id_cuenta, transaccion.cod_symbol)
            
        db.session.add(transaccion)
        db.session.flush() # Generate ID for transaccion

        cantidad_restante = transaccion.cantidad
        
        # 1. Buscar saldos negativos (ventas en corto)
        saldos_negativos = TransaccionSaldoReader.get_saldos_negativos(transaccion.id_cuenta, transaccion.cod_symbol)

        for saldo in saldos_negativos:
            if cantidad_restante <= 0:
                break
                
            cantidad_en_negativo = abs(saldo.ctd_saldo)
            
            if cantidad_restante >= cantidad_en_negativo:
                # Cubrimos todo el saldo negativo
                saldo.ctd_saldo = 0 
                cantidad_matched = cantidad_en_negativo
                cantidad_restante -= cantidad_en_negativo
            else:
                # Cubrimos parcialmente
                saldo.ctd_saldo += cantidad_restante 
                cantidad_matched = cantidad_restante
                cantidad_restante = 0

            # Calcular ganancia/perdida
            # "Apertura" es la transacción original (saldo), que debe ser venta (negativa)
            # "Cierre" es la transacción actual (compra), que es positiva
            # Ganancia = (Precio Venta - Precio Compra) * Cantidad Matched
            
            ganancia = (saldo.transaccion.imp_unitario - transaccion.imp_unitario) * cantidad_matched

            movimiento_saldo = MovimientoSaldoModel(
                id_transaccion_apertura = saldo.id_transaccion,
                id_transaccion_cierre = transaccion.id_transaccion,
                ctd_aplicada = cantidad_matched,
                ctd_saldo_final_apertura = saldo.ctd_saldo, 
                imp_ganancia = ganancia
            )
            db.session.add(movimiento_saldo)
                
        # 2. Si sobra cantidad, crear nuevo saldo positivo asociado a ESTA transaccion
        if cantidad_restante > 0:
            nuevo_saldo = TransaccionSaldoModel(
                id_transaccion = transaccion.id_transaccion,
                ctd_saldo = cantidad_restante,
                imp_saldo = cantidad_restante * transaccion.imp_unitario 
            )
            db.session.add(nuevo_saldo)
        

class VentaGeneric:
    def __init__(self):
        pass

    def registrar(self, transaccion: TransaccionModel):
        if transaccion.orden_fifo is None:
            transaccion.orden_fifo = TransaccionReader.get_next_orden_fifo(transaccion.id_cuenta, transaccion.cod_symbol)
            
        db.session.add(transaccion)
        db.session.flush()

        cantidad_restante = abs(transaccion.cantidad) # Ventas son negativas en theory, pero si viene positivo lo manejamos? 
        # Asumimos que 'cantidad' en TransaccionModel puede ser negativo para ventas? 
        # El docstring dice "venta de 5 acciones"... normalmente ventas se registran con cantidad negativa si son "movimientos".
        # Pero checkeando lógica Compra: cantidad_restante = transaccion.cantidad (positivo).
        # Si Venta viene con negativo, usaremos abs().
        
        # 1. Buscar saldos positivos (compras previas)
        saldos_positivos = TransaccionSaldoReader.get_saldos(transaccion.id_cuenta, transaccion.cod_symbol)

        for saldo in saldos_positivos:
            if cantidad_restante <= 0:
                break
                
            cantidad_disponible = saldo.ctd_saldo
            
            if cantidad_restante >= cantidad_disponible:
                # Consumimos todo el saldo
                saldo.ctd_saldo = 0
                cantidad_matched = cantidad_disponible
                cantidad_restante -= cantidad_disponible
            else:
                # Consumimos parcialmente
                saldo.ctd_saldo -= cantidad_restante
                cantidad_matched = cantidad_restante
                cantidad_restante = 0
                
            # Calcular Ganancia
            # Apertura = Compra (saldo.imp_unitario)
            # Cierre = Venta (transaccion.imp_unitario)
            # Ganancia = (Precio Venta - Precio Compra) * Cantidad
            ganancia = (transaccion.imp_unitario - saldo.transaccion.imp_unitario) * cantidad_matched
            
            movimiento_saldo = MovimientoSaldoModel(
                id_transaccion_apertura = saldo.id_transaccion,
                id_transaccion_cierre = transaccion.id_transaccion,
                ctd_aplicada = cantidad_matched,
                ctd_saldo_final_apertura = saldo.ctd_saldo,
                imp_ganancia = ganancia
            )
            db.session.add(movimiento_saldo)

        # 2. Si sobra cantidad, crear nuevo saldo negativo (Short Sell)
        if cantidad_restante > 0:
            # Es una venta en corto
            nuevo_saldo = TransaccionSaldoModel(
                id_transaccion = transaccion.id_transaccion,
                ctd_saldo = -cantidad_restante,
                imp_saldo = -cantidad_restante * transaccion.imp_unitario
            )
            db.session.add(nuevo_saldo)


class TransaccionService:
    def __init__(self):
        pass

    def registrar(self, transaccion: TransaccionModel):
        tipoTransaccion = get_tipo_transaccion()
        if transaccion.id_tipo_transaccion == tipoTransaccion.C:
            CompraGeneric().registrar(transaccion)
        elif transaccion.id_tipo_transaccion == tipoTransaccion.V:
            VentaGeneric().registrar(transaccion)