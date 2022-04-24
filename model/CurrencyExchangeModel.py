from app import db

class CurrencyExchangeModel(db.Model):
    __tablename__ = "tb_currency_exchange"
    
    fecha_cambio = db.Column(db.Date,  primary_key=True)
    moneda_base_symbol = db.Column(db.String,  primary_key=True)
    moneda_ref_symbol = db.Column(db.String,  primary_key=True)    
    ind_activo  = db.Column(db.String)
    par_id = db.Column(db.Integer)
    par_name = db.Column(db.String)
    importe_compra = db.Column(db.Numeric(17,3))
    importe_venta = db.Column(db.Numeric(17,3))
    fecha_registro = db.Column(db.Date)
    fecha_audit = db.Column(db.DateTime)
