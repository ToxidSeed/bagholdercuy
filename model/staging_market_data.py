from config.extensions import db

class StagingMarketDataModel(db.Model):
    """
    Capa de Staging para datos crudos de mercado y cadenas de opciones del Proyecto Bagholder
    """
    __tablename__ = "tb_staging_market_data"

    id_staging = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proveedor = db.Column(db.String(50), nullable=False)
    endpoint = db.Column(db.String(100), nullable=False)
    ticker = db.Column(db.String(25), nullable=True)
    file_path = db.Column(db.String(255), nullable=False)
    file_size_kb = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.String(20), nullable=False, default="PENDIENTE")
    fch_hr_creacion = db.Column(db.DateTime, nullable=False, default=db.func.now())

    