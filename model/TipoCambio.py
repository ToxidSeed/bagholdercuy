from app import db

class TipoCambioModel(db.Model):
    __tablename__ = "tb_tipo_cambio"
    
    fch_cambio = db.Column(db.Date,  primary_key=True)
    mon_base_id = db.Column(db.String,  primary_key=True)
    mon_ref_id = db.Column(db.String,  primary_key=True)    
    ind_activo  = db.Column(db.String)
    par_id = db.Column(db.Integer)
    par_nombre = db.Column(db.String)
    imp_compra = db.Column(db.Numeric(17,3))
    imp_venta = db.Column(db.Numeric(17,3))
    fch_registro = db.Column(db.Date)
    fch_audit = db.Column(db.DateTime)
