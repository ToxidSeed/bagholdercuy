from app import db

class SerieDiariaModel(db.Model):
    __tablename__ = "tb_serie_diaria"

    symbol = db.Column(db.String, primary_key=True)
    fch_serie = db.Column(db.Date, primary_key=True)
    fch_semana = db.Column(db.Date)
    fch_mes = db.Column(db.Date)
    imp_apertura = db.Column(db.Numeric(15,4))
    imp_maximo = db.Column(db.Numeric(15,4))
    imp_minimo = db.Column(db.Numeric(15,4))
    imp_cierre = db.Column(db.Numeric(15,4))
    imp_apertura_ajus = db.Column(db.Numeric(15.4))
    imp_maximo_ajus = db.Column(db.Numeric(15.4))
    imp_minimo_ajus = db.Column(db.Numeric(15.4))
    imp_cierre_ajus = db.Column(db.Numeric(15.4))
    fch_registro = db.Column(db.Date)