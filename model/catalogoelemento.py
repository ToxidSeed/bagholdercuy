from app import db

class CatalogoElementoModel(db.Model):

    __tablename__="tb_catalogo_detalle"

    cod_catalogo = db.Column(db.Integer,primary_key=True)
    cod_elemento = db.Column(db.Integer)
    nom_elemento = db.Column(db.String(100))