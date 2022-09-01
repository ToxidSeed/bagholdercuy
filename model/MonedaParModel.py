from app import db

class MonedaParModel(db.Model):
    __tablename__ = "tb_moneda_par"

    par_id = db.Column(db.Integer, primary_key=True)
    mon_base_id = db.Column(db.String)
    mon_ref_id = db.Column(db.String)
    nombre = db.Column(db.String)
    operacion = db.Column(db.String)
    ind_activo = db.Column(db.String)
    fch_registro = db.Column(db.Date)
    fch_audit = db.Column(db.DateTime)