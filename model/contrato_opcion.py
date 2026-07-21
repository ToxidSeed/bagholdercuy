from config.extensions import db

class ContratoOpcionModel(db.Model):
    __tablename__ = "tb_contrato_opcion"

    id_contrato_opcion = db.Column(db.Integer, primary_key=True)
    
    # Identificador del contrato (idealmente OPRA u otro ticker único del contrato)
    cod_symbol = db.Column(db.String(50), unique=True, nullable=False)

    # Subyacente (ticker del activo subyacente)
    cod_symbol_subyacente = db.Column(db.String(25), nullable=False)

    # CALL / PUT
    tipo_opcion = db.Column(db.Enum('CALL', 'PUT'), nullable=False)

    # Fecha de expiración
    fch_vencimiento = db.Column(db.Date, nullable=False)

    # Precio strike
    imp_strike = db.Column(db.Numeric(15, 4), nullable=False)

    # Multiplicador (tamaño de contrato), normalmente 100
    tam_contrato = db.Column(db.Integer, default=100, nullable=False)

    # Moneda (p.ej. USD)
    cod_moneda = db.Column(db.String(3))

    descripcion = db.Column(db.String(250))

    # Auditoría
    fch_registro = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    fch_audit = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
