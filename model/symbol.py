from config.extensions import db
from sqlalchemy.orm import synonym


class SymbolModel(db.Model):
    __tablename__ = "tb_symbol"

    id_symbol = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(250))
    region = db.Column(db.String(10))
    exchange = db.Column(db.String(15))
    asset_type = db.Column(db.String(15))
    fec_registro = db.Column(db.Date)
    fec_audit = db.Column(db.DateTime)
    moneda_id = db.Column(db.String(3))
    id_symbol_type = db.Column(
        db.Integer, db.ForeignKey("tb_symbol_type.id_symbol_type"), nullable=True
    )

    # Alias / sinónimo para compatibilidad con código existente que use `.id`
    id = synonym("id_symbol")

    def __repr__(self):
        return f"<Symbol {self.id_symbol} - {self.symbol}>"

