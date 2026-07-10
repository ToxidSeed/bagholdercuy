from config.extensions import db
from schemas.posicion import RecalcularPosicionesRequest
from reader.transaccion import TransaccionReader
from model.transaccion_saldo import TransaccionSaldoModel
from model.movimiento_saldo import MovimientoSaldoModel
from constants.indicador_apcierre import IndicadorApcierre
from collections import defaultdict
from decimal import Decimal


class PosicionRecalculador:
    def __init__(self, dto: RecalcularPosicionesRequest):
        self.dto = dto

    def ejecutar(self):
        transacciones = self._obtener_transacciones()
        if not transacciones:
            return

        self._validar_transacciones(transacciones)
        t_por_symbol, t_map, t_ids = self._agrupar_transacciones(transacciones)
        self._limpiar_registros_previos(t_ids)
        self._procesar_fifo_por_simbolo(t_por_symbol, t_map)

    def _obtener_transacciones(self):
        if self.dto.cod_tipo_procesamiento == "TODOS":
            return TransaccionReader.get_transacciones_x_cuenta(self.dto.id_cuenta)
        return TransaccionReader.get_transacciones_x_cuenta_y_symbols(
            self.dto.id_cuenta, self.dto.cod_symbol_list
        )

    def _validar_transacciones(self, transacciones):
        for t in transacciones:
            if t.ind_requiere_revision == 1:
                raise Exception(f"La transacción {t.id_transaccion} requiere revisión. No se puede reprocesar.")

    def _agrupar_transacciones(self, transacciones):
        t_por_symbol = defaultdict(list)
        t_map = {}
        t_ids = []
        for t in transacciones:
            t_por_symbol[t.cod_symbol].append(t)
            t_map[t.id_transaccion] = t
            t_ids.append(t.id_transaccion)
        return t_por_symbol, t_map, t_ids

    def _limpiar_registros_previos(self, t_ids):
        if not t_ids:
            return

        # Delete MovimientoSaldoModel
        db.session.query(MovimientoSaldoModel).filter(
            db.or_(
                MovimientoSaldoModel.id_transaccion_apertura.in_(t_ids),
                MovimientoSaldoModel.id_transaccion_cierre.in_(t_ids)
            )
        ).delete(synchronize_session=False)

        # Delete TransaccionSaldoModel
        db.session.query(TransaccionSaldoModel).filter(
            TransaccionSaldoModel.id_transaccion.in_(t_ids)
        ).delete(synchronize_session=False)

    def _procesar_fifo_por_simbolo(self, t_por_symbol, t_map):
        for symbol, t_list in t_por_symbol.items():
            if not t_list:
                continue
            
            t_list.sort(key=lambda x: (x.fch_hr_transaccion, x.orden_fifo))

            first_t = t_list[0]

            if not (first_t.indicador_apcierre.cod_indicador == IndicadorApcierre.APERTURA.cod_indicador):
                raise Exception(
                    f"La primera transacción para el symbol {symbol} debe ser de {IndicadorApcierre.APERTURA.nom_indicador}. "
                )

            saldos_abiertos = []

            for t_transaccion in t_list:
                cod_indicador = t_transaccion.indicador_apcierre.cod_indicador
                
                if IndicadorApcierre.APERTURA.cod_indicador == cod_indicador:
                    self._procesar_transaccion_apertura(t_transaccion, saldos_abiertos)
                elif IndicadorApcierre.CIERRE.cod_indicador == cod_indicador:
                    self._procesar_transaccion_cierre(t_transaccion, saldos_abiertos, t_map)
                else:
                    raise Exception(f"Indicador de cierre inválido: {cod_indicador}")

    def _procesar_transaccion_apertura(self, t_transaccion, saldos_abiertos):
        nuevo_saldo = TransaccionSaldoModel(
            id_transaccion=t_transaccion.id_transaccion,
            ctd_saldo=t_transaccion.cantidad,
            imp_saldo=t_transaccion.imp_bruto
        )
        db.session.add(nuevo_saldo)
        saldos_abiertos.append(nuevo_saldo)

    def _procesar_transaccion_cierre(self, t, saldos_abiertos, t_map):
        ctd_a_consumir = Decimal(str(t.cantidad))
        
        while ctd_a_consumir > 0 and saldos_abiertos:
            saldo_actual = saldos_abiertos[0]
            t_apertura = t_map[saldo_actual.id_transaccion]
            
            ctd_saldo_actual_abs = abs(Decimal(str(saldo_actual.ctd_saldo)))
            
            if ctd_saldo_actual_abs <= ctd_a_consumir:
                ctd_aplicada = ctd_saldo_actual_abs
                ctd_a_consumir -= ctd_aplicada
                saldo_actual.ctd_saldo = Decimal('0.000')
                saldo_actual.imp_saldo = Decimal('0.00')
                saldos_abiertos.pop(0)
            else:
                ctd_aplicada = ctd_a_consumir
                if saldo_actual.ctd_saldo > 0:
                    saldo_actual.ctd_saldo -= ctd_aplicada
                else:
                    saldo_actual.ctd_saldo += ctd_aplicada
                    
                saldo_actual.imp_saldo = Decimal(str(saldo_actual.ctd_saldo)) * Decimal(str(t_apertura.imp_unitario))
                ctd_a_consumir = Decimal('0.000')

            if t_apertura.cantidad > 0:
                imp_ganancia = ctd_aplicada * (Decimal(str(t.imp_unitario)) - Decimal(str(t_apertura.imp_unitario)))
            else:
                imp_ganancia = ctd_aplicada * (Decimal(str(t_apertura.imp_unitario)) - Decimal(str(t.imp_unitario)))
                
            movimiento = MovimientoSaldoModel(
                id_transaccion_apertura=saldo_actual.id_transaccion,
                id_transaccion_cierre=t.id_transaccion,
                ctd_aplicada=ctd_aplicada,
                ctd_saldo_final_apertura=saldo_actual.ctd_saldo,
                imp_ganancia=imp_ganancia
            )
            db.session.add(movimiento)

        if ctd_a_consumir > 0:
            nuevo_saldo_short = TransaccionSaldoModel(
                id_transaccion=t.id_transaccion,
                ctd_saldo=-ctd_a_consumir,
                imp_saldo=-ctd_a_consumir * Decimal(str(t.imp_unitario))
            )
            db.session.add(nuevo_saldo_short)
            saldos_abiertos.append(nuevo_saldo_short)


class PosicionService:
    @staticmethod
    def recalcular_posiciones(dto: RecalcularPosicionesRequest):
        recalculador = PosicionRecalculador(dto)
        recalculador.ejecutar()
