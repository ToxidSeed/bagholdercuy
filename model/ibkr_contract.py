from config.extensions import db
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy import text

class IbkrContractsModel(db.Model):
    __tablename__ = "tb_ibkr_contract"

    conid = db.Column(BIGINT, primary_key=True, autoincrement=False)
    cod_symbol = db.Column(db.String(25), nullable=False)
    exchange = db.Column(db.String(50), nullable=False)
    fch_hr_registro = db.Column(
        DATETIME(fsp=3),
        nullable=False,
        default=db.func.now(),
        server_default=text("CURRENT_TIMESTAMP(3)")
    )

    __table_args__ = (
        db.UniqueConstraint('conid', 'exchange', name='uk_ibkr_conid_exchange'),
    )
