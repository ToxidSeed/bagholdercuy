from app import db
from model.transaccion_saldo import TransaccionSaldoModel
from model.transaccion import TransaccionModel

class TransaccionSaldoReader:
    @staticmethod
    def get_saldos(id_cuenta, cod_symbol):
        stmt = db.select(
            TransaccionSaldoModel
        ).join(
            TransaccionModel, TransaccionSaldoModel.id_transaccion == TransaccionModel.id_transaccion
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.cod_symbol == cod_symbol,
            TransaccionSaldoModel.ctd_saldo > 0
        ).order_by(
            TransaccionModel.orden_fifo.asc()
        )

        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_saldos_negativos(id_cuenta, cod_symbol):
        """
        Retorna los saldos negativos (ventas en corto) para un símbolo hasta cierta fecha.
        Se ordena por fecha y orden_fifo ascendente para cubrir primero las posiciones más antiguas (FIFO).
        """
        stmt = db.select(
            TransaccionSaldoModel
        ).join(
            TransaccionModel, TransaccionSaldoModel.id_transaccion == TransaccionModel.id_transaccion
        ).where(
            TransaccionModel.id_cuenta == id_cuenta,
            TransaccionModel.cod_symbol == cod_symbol,
            TransaccionSaldoModel.ctd_saldo < 0
        ).order_by(            
            TransaccionModel.orden_fifo.asc()
        )

        result = db.session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get(id_transaccion):
        stmt = db.select(
            TransaccionSaldoModel
        ).where(
            TransaccionSaldoModel.id_transaccion == id_transaccion
        )

        result = db.session.execute(stmt)
        return result.scalars().one()