from model.contrato_opcion import ContratoOpcionModel
from model.StockSymbol import StockSymbol
from model.transaccion import TransaccionModel
from model.transaccion_saldo import TransaccionSaldoModel
from constants.instrumento_financiero import get_instrumento_financiero
from sqlalchemy import func
from app import db
import pandas as pd

class PosicionReader:
    def get_active_holdings(id_cuenta):
        """
        Retrieves active holdings based on transaction balances.
        """
        stmt = db.select(
            TransaccionModel.cod_symbol,
            TransaccionModel.id_instrumento_financiero.label("cod_tipo_activo"),
            
            func.min(TransaccionModel.fch_hr_transaccion).label('holding_since'),
            func.sum(TransaccionModel.imp_unitario * TransaccionSaldoModel.ctd_saldo).label("sum_imp_accion"), # Weighted sum price * quantity
            
            func.sum(TransaccionSaldoModel.imp_saldo).label("sum_imp_operacion"), # Remaining invested amount
            
            func.sum(TransaccionSaldoModel.ctd_saldo).label("sum_shares_balance"),
            func.min(TransaccionModel.fch_hr_transaccion).label("min_trade_date"),
            # Placeholder for option/active specifics if needed. 
            # Legacy expected 'cod_opcion' for options. 
            # If type is OPT, cod_symbol is expected to be the option code.
            TransaccionModel.cod_symbol.label("cod_opcion") 
        ).select_from(
            TransaccionModel
        ).join(
            TransaccionSaldoModel, TransaccionModel.id_transaccion == TransaccionSaldoModel.id_transaccion
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionSaldoModel.ctd_saldo != 0
        ).group_by(
            TransaccionModel.cod_symbol,
            TransaccionModel.id_instrumento_financiero
        )
        
        result = db.session.execute(stmt)
        return result.all()

    def get_saldos_actuales_por_cuenta(id_cuenta):
        stmt = db.select(
            TransaccionModel.cod_symbol,
            StockSymbol.name,
            TransaccionModel.orden_fifo,
            TransaccionModel.fch_hr_transaccion,
            TransaccionModel.imp_unitario,
            TransaccionModel.id_transaccion,
            TransaccionSaldoModel.ctd_saldo.label('saldo')
        ).select_from(
            TransaccionModel
        ).join(
            TransaccionSaldoModel, TransaccionModel.id_transaccion == TransaccionSaldoModel.id_transaccion
        ).join(
            StockSymbol, TransaccionModel.cod_symbol == StockSymbol.symbol
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.id_instrumento_financiero != get_instrumento_financiero().OPTION,
            TransaccionSaldoModel.ctd_saldo != 0
        )

        result = db.session.execute(stmt)
        # Convert to list of dicts for DataFrame creation
        data = [row._asdict() for row in result.all()]
        
        if not data:
            return []

        # 2. Load into Pandas DataFrame
        df = pd.DataFrame(data)

        df_resumen = df.groupby('cod_symbol').agg(
            max_orden_fifo=('orden_fifo', 'max'),
            min_orden_fifo=('orden_fifo', 'min'),
            cantidad = ('saldo', 'sum'),
            min_imp_unitario=('imp_unitario', 'min'),
            max_imp_unitario=('imp_unitario', 'max'),
            mean_imp_unitario=('imp_unitario', 'mean')
        ).reset_index()
        
        df_resumen = df_resumen.merge(
            df[['cod_symbol', 'orden_fifo', 'imp_unitario', 'fch_hr_transaccion']],
            left_on=['cod_symbol', 'min_orden_fifo'],
            right_on=['cod_symbol', 'orden_fifo'],
            how='left'
        ).drop(columns=['orden_fifo'])

        df_resumen = df_resumen.rename(columns={'fch_hr_transaccion': 'fch_primera_posicion', 'imp_unitario':'imp_posicion_incial'})

        records = df_resumen.to_dict('records')

        return records

    def get_saldos_opciones_por_cuenta(id_cuenta):
        stmt = db.select(
            TransaccionModel.cod_symbol,
            ContratoOpcionModel.cod_symbol_subyacente,
            ContratoOpcionModel.tipo_opcion,
            ContratoOpcionModel.fch_vencimiento,
            ContratoOpcionModel.imp_strike,
            TransaccionModel.orden_fifo,
            TransaccionModel.fch_hr_transaccion,
            TransaccionModel.imp_unitario,
            TransaccionModel.id_transaccion,
            TransaccionSaldoModel.ctd_saldo.label('saldo')
        ).select_from(
            TransaccionModel
        ).join(
            TransaccionSaldoModel, TransaccionModel.id_transaccion == TransaccionSaldoModel.id_transaccion
        ).join(
            ContratoOpcionModel, TransaccionModel.id_contrato_opcion == ContratoOpcionModel.id_contrato_opcion
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.id_instrumento_financiero == get_instrumento_financiero().OPTION,
            TransaccionSaldoModel.ctd_saldo != 0
        )

        result = db.session.execute(stmt)
        data = [row._asdict() for row in result.all()]
        
        if not data:
            return []

        df = pd.DataFrame(data)

        df_resumen = df.groupby('cod_symbol').agg(
            max_orden_fifo=('orden_fifo', 'max'),
            min_orden_fifo=('orden_fifo', 'min'),
            cantidad = ('saldo', 'sum'),
            min_imp_unitario=('imp_unitario', 'min'),
            max_imp_unitario=('imp_unitario', 'max'),
            mean_imp_unitario=('imp_unitario', 'mean'),
            cod_symbol_subyacente=('cod_symbol_subyacente', 'first'),
            tipo_opcion=('tipo_opcion', 'first'),
            fch_vencimiento=('fch_vencimiento', 'first'),
            imp_strike=('imp_strike', 'first')
        ).reset_index()
        
        df_resumen = df_resumen.merge(
            df[['cod_symbol', 'orden_fifo', 'imp_unitario', 'fch_hr_transaccion']],
            left_on=['cod_symbol', 'min_orden_fifo'],
            right_on=['cod_symbol', 'orden_fifo'],
            how='left'
        ).drop(columns=['orden_fifo'])

        df_resumen = df_resumen.rename(columns={'fch_hr_transaccion': 'fch_primera_posicion', 'imp_unitario':'imp_posicion_incial'})

        records = df_resumen.to_dict('records')

        return records