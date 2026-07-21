from config.extensions import db
from model.movimiento_saldo import MovimientoSaldoModel
from model.transaccion import TransaccionModel

class MovimientoSaldoReader:
    @staticmethod
    def get_historial(cod_symbol):
        stmt = db.select(
            MovimientoSaldoModel
        ).join(
            TransaccionModel, MovimientoSaldoModel.id_transaccion_cierre == TransaccionModel.id_transaccion
        ).where(
            TransaccionModel.cod_symbol == cod_symbol
        ).order_by(
            MovimientoSaldoModel.fch_hr_registro.desc()
        )
        
        result = db.session.execute(stmt)
        return result.scalars().all()