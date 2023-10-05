from app import db

class CalendarioDiarioModel(db.Model):
    __tablename__="tb_calendario_diario"

    fch_dia = db.Column(db.Date, primary_key=True)
    anyo = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    dia = db.Column(db.Integer)
    cod_semana = db.Column(db.Integer)
    fch_semana = db.Column(db.Date)
    num_anyo_semana = db.Column(db.Integer)
    num_semana = db.Column(db.Integer)
    num_dia_semana = db.Column(db.Integer)
    flg_fin_semana = db.Column(db.String)
    flg_usa_mercado_cerrado = db.Column(db.String(1))