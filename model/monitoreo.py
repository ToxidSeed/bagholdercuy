from config.extensions import db


class MonitoreoModel(db.Model):
    __tablename__ = "tb_monitoreo"

    id_monitoreo = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    id_cuenta = db.Column(db.Integer, nullable=False)
    id_symbol_type = db.Column(
        db.Integer, db.ForeignKey("tb_symbol_type.id_symbol_type"), nullable=False
    )
    id_symbol = db.Column(
        db.Integer,
        db.ForeignKey("tb_symbol.id_symbol", ondelete="CASCADE"),
        nullable=True,
    )
    id_contrato_opcion = db.Column(
        db.Integer,
        db.ForeignKey("tb_contrato_opcion.id_contrato_opcion", ondelete="CASCADE"),
        nullable=True,
    )
    fch_registro = db.Column(db.Date)

    # Relaciones
    symbol_type = db.relationship("SymbolTypeModel", foreign_keys=[id_symbol_type])
    symbol = db.relationship("SymbolModel", foreign_keys=[id_symbol])
    contrato_opcion = db.relationship("ContratoOpcionModel", foreign_keys=[id_contrato_opcion])

    def __repr__(self):
        target = f"symbol={self.id_symbol}" if self.id_symbol else f"option={self.id_contrato_opcion}"
        return f"<Monitoreo {self.id_monitoreo} cuenta={self.id_cuenta} type={self.id_symbol_type} {target}>"


