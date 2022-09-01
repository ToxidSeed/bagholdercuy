from app import db

class UsuarioModel(db.Model):
    __tablename__="tb_usuario"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String)
    password = db.Column(db.String)
    nombres = db.Column(db.String)
    apellidos = db.Column(db.String)
    moneda_id = db.Column(db.String(3))
    