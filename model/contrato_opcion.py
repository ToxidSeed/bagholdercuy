from config.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import synonym


class ContratoOpcionModel(db.Model):
    __tablename__ = "tb_contrato_opcion"
    __table_args__ = (
        db.CheckConstraint("imp_strike > 0", name="chk_contrato_opcion_strike_pos"),
        db.CheckConstraint("tam_contrato > 0", name="chk_contrato_opcion_tam_pos"),
    )

    id_contrato_opcion = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Llave foránea hacia el catálogo de símbolos generales (tb_symbol.id_symbol)
    id_symbol_subyacente = db.Column(
        db.Integer,
        db.ForeignKey("tb_symbol.id_symbol", ondelete="RESTRICT"),
        nullable=False,
    )

    # Identificador del contrato (ticker OSI del contrato, ej. AAPL261120C00150000)
    cod_symbol = db.Column(db.String(50), unique=True, nullable=False)

    # CALL / PUT
    tipo_opcion = db.Column(db.Enum("CALL", "PUT"), nullable=False)

    # Fecha de expiración
    fch_vencimiento = db.Column(db.Date, nullable=False)

    # Precio strike
    imp_strike = db.Column(db.Numeric(15, 4), nullable=False)

    # Multiplicador (tamaño de contrato), normalmente 100
    tam_contrato = db.Column(db.Integer, default=100, nullable=False)

    # Moneda (p.ej. USD)
    cod_moneda = db.Column(db.String(3), nullable=True)

    # Descripción opcional del contrato
    descripcion = db.Column(db.String(250), nullable=True)

    # Auditoría
    fch_registro = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    fch_audit = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    # Relación con el símbolo subyacente
    symbol = db.relationship("SymbolModel", foreign_keys=[id_symbol_subyacente])

    # Sinónimo para compatibilidad hacia atrás
    id_symbol = synonym("id_symbol_subyacente")

    # Propiedad híbrida para compatibilidad con código que consulte o filtre por cod_symbol_subyacente
    @hybrid_property
    def cod_symbol_subyacente(self):
        return self.symbol.symbol if self.symbol else None

    @cod_symbol_subyacente.expression
    def cod_symbol_subyacente(cls):
        from model.symbol import SymbolModel

        return (
            db.select(SymbolModel.symbol)
            .where(SymbolModel.id_symbol == cls.id_symbol_subyacente)
            .scalar_subquery()
        )

    @cod_symbol_subyacente.setter
    def cod_symbol_subyacente(self, value):
        if value:
            from reader.symbol import SymbolReader

            sym = SymbolReader().get(cod_symbol=value)
            if sym:
                self.id_symbol_subyacente = sym.id_symbol

    def __repr__(self):
        return f"<ContratoOpcion {self.id_contrato_opcion} - {self.cod_symbol}>"

