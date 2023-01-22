from app import db

class VariacionSemanalModel(db.Model):
    __tablename__="tb_variacion_semanal"

    symbol = db.Column(db.String, primary_key=True)
    fecha = db.Column(db.Date, primary_key=True)
    anyo = db.Column(db.Integer)
    semana = db.Column(db.Integer)
    imp_cierre_ant = db.Column(db.Numeric(15,4))
    imp_apertura = db.Column(db.Numeric(15,4))
    imp_maximo = db.Column(db.Numeric(15,4))
    imp_minimo = db.Column(db.Numeric(15,4))
    imp_cierre = db.Column(db.Numeric(15,4))
    pct_variacion_cierre = db.Column(db.Numeric(8,4))
    imp_variacion_cierre = db.Column(db.Numeric(15,4))
    pct_variacion_maximo = db.Column(db.Numeric(8,4))
    imp_variacion_maximo = db.Column(db.Numeric(15,4))
    pct_variacion_minimo = db.Column(db.Numeric(8,4))
    imp_variacion_minimo = db.Column(db.Numeric(15,4))