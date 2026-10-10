from config.extensions import db


class SymbolTypeMappingModel(db.Model):
    """
    Equivalencia entre un tipo de symbol (tb_symbol_type) y el código que usa cada proveedor de datos.
    Ejemplo: STOCK -> provider_name='IBKR', provider_code='STK'
    """
    __tablename__ = "tb_symbol_type_mapping"

    id_mapping = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_symbol_type = db.Column(
        db.Integer,
        db.ForeignKey("tb_symbol_type.id_symbol_type", name="fk_mapping_symbol_type"),
        nullable=False
    )
    provider_name = db.Column(db.String(50), nullable=False)
    provider_code = db.Column(db.String(20), nullable=False)

    symbol_type = db.relationship("SymbolTypeModel")

    __table_args__ = (
        db.UniqueConstraint("id_symbol_type", "provider_name", name="uk_type_provider"),
    )

    def __repr__(self):
        return f"<SymbolTypeMapping {self.id_symbol_type} - {self.provider_name}:{self.provider_code}>"
