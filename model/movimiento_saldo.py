from app import db

class MovimientoSaldoModel(db.Model):
    __tablename__ = 'tb_movimiento_saldo'

    id_movimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_symbol = db.Column(db.String(5), nullable=False)
    cod_symbol_opcion = db.Column(db.String(21), nullable=True)
    id_transaccion_apertura = db.Column(db.Integer, nullable=False)
    fch_movimiento = db.Column(db.Date, nullable=False)
    ctd_apertura = db.Column(db.Numeric(17, 2), nullable=False)
    imp_accion_apertura = db.Column(db.Numeric(17, 2), nullable=False)
    id_transaccion_cierre = db.Column(db.Integer, nullable=True)
    ctd_saldo_apertura_inicial = db.Column(db.Numeric(17, 2), nullable=False)
    ctd_cierre = db.Column(db.Numeric(17, 2), nullable=False)
    ctd_saldo_apertura_final = db.Column(db.Numeric(17, 2), nullable=False)
    imp_accion_cierre = db.Column(db.Numeric(17, 2), nullable=False)
    imp_ganancia = db.Column(db.Numeric(17, 2), nullable=False)

    def __repr__(self):
        return f'<MovimientoSaldo id={self.id_movimiento}, symbol={self.cod_symbol}>'