from app import db

class TransaccionModel(db.Model):
    __tablename__ = 'tb_transaccion'

    id_transaccion = db.Column(db.Integer,primary_key=True,nullable=False)
    id_cuenta = db.Column(db.Integer,nullable=False)
    num_transaccion = db.Column(db.Integer, nullable=False)
    cod_symbol = db.Column(db.String, nullable=False)
    cod_symbol_opcion = db.Column(db.String)
    cod_tipo_transaccion = db.Column(db.String)
    fch_transaccion = db.Column(db.Date,nullable=False)
    cantidad = db.Column(db.Numeric(15,3),nullable=False)
    cod_mes = db.Column(db.Integer,nullable=False)     
    cod_semana = db.Column(db.Integer,nullable=False)
    imp_accion = db.Column(db.Numeric(17,2))
    imp_transaccion = db.Column(db.Numeric(17,2),nullable=False)
    fch_registro = db.Column(db.Date)
    hora_registro = db.Column(db.Time)

    @classmethod
    def get_next_num_transaccion(cls, cod_symbol, cod_symbol_opcion, fch_transaccion):
        query = cls.query.filter_by(
            cod_symbol=cod_symbol,
            cod_symbol_opcion=cod_symbol_opcion,
            fch_transaccion=fch_transaccion
        )

        return query.first()
