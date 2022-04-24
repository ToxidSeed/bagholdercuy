from app import db
class TipoModel(db.Model):
    __tablename__="tb_tipo"

    num_catalogo = db.Column(db.Integer, primary_key=True)
    tipo_id = db.Column(db.String(3), primary_key=True)
    tipo_nombre = db.Column(db.String(100))