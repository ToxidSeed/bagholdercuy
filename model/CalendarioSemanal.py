from app import db
class CalendarioSemanalModel(db.Model):
    __tablename__="tb_calendario_semanal"

    fch_semana = db.Column(db.Date, primary_key=True)
    anyo = db.Column(db.Integer)
    semana = db.Column(db.Integer)
    fch_inicio = db.Column(db.Date)
    fch_fin = db.Column(db.Date)
    fch_lunes = db.Column(db.Date)
    fch_martes = db.Column(db.Date)
    fch_miercoles = db.Column(db.Date)
    fch_jueves = db.Column(db.Date)
    fch_viernes = db.Column(db.Date)