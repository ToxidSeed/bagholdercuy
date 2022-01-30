from app import db

class Balance(db.Model):
    __tablename__ = "tb_balance"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    profundidad_id = db.Column(db.String(1))
    fec_cierre = db.Column(db.Date)
    fec_modificacion = db.Column(db.Date)
    inversion_imp = db.Column(db.Numeric(15,2))
    cash_imp = db.Column(db.Numeric(15,2))
    gain_loss_imp = db.Column(db.Numeric(15,2))
    net_worth_imp = db.Column(db.Numeric(15,2))
