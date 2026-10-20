from config.extensions import db
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy import text


class IbkrContractMapModel(db.Model):
    __tablename__ = "tb_ibkr_contract_map"

    id_ibkr_contract_map = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    id_symbol = db.Column(
        db.Integer,
        db.ForeignKey("tb_symbol.id_symbol", ondelete="CASCADE"),
        unique=True,
        nullable=True,
    )
    id_contrato_opcion = db.Column(
        db.Integer,
        db.ForeignKey("tb_contrato_opcion.id_contrato_opcion", ondelete="CASCADE"),
        unique=True,
        nullable=True,
    )
    conid = db.Column(BIGINT, nullable=False, index=True)
    fch_registro = db.Column(
        DATETIME(fsp=3),
        nullable=False,
        default=db.func.now(),
        server_default=text("CURRENT_TIMESTAMP(3)"),
    )
    fch_audit = db.Column(
        DATETIME(fsp=3),
        nullable=False,
        default=db.func.now(),
        onupdate=db.func.now(),
        server_default=text("CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)"),
    )

    symbol = db.relationship("SymbolModel", foreign_keys=[id_symbol])
    contrato_opcion = db.relationship(
        "ContratoOpcionModel", foreign_keys=[id_contrato_opcion]
    )

    @classmethod
    def get_by_symbol_id(cls, id_symbol: int):
        return cls.query.filter_by(id_symbol=id_symbol).first()

    @classmethod
    def get_by_contrato_opcion_id(cls, id_contrato_opcion: int):
        return cls.query.filter_by(id_contrato_opcion=id_contrato_opcion).first()

    @classmethod
    def set_mapping(
        cls, conid: int, id_symbol: int = None, id_contrato_opcion: int = None
    ):
        if not conid:
            return None
        existing = None
        if id_symbol is not None:
            existing = cls.query.filter_by(id_symbol=id_symbol).first()
        elif id_contrato_opcion is not None:
            existing = cls.query.filter_by(
                id_contrato_opcion=id_contrato_opcion
            ).first()

        if existing:
            existing.conid = int(conid)
            return existing
        else:
            new_map = cls(
                id_symbol=id_symbol,
                id_contrato_opcion=id_contrato_opcion,
                conid=int(conid),
            )
            db.session.add(new_map)
            return new_map
