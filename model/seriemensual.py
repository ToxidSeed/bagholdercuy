from app import db

class SerieMensualModel(db.Model):
    __tablename__ = "tb_serie_mensual"

    symbol = db.Column(db.String, primary_key=True)
    fch_ini_mes = db.Column(db.Date, primary_key=True)
    anyo = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    imp_apertura = db.Column(db.Numeric(15,4))
    imp_maximo = db.Column(db.Numeric(15,4))
    imp_minimo = db.Column(db.Numeric(15,4))
    imp_cierre = db.Column(db.Numeric(15,4))    
    imp_apertura_ajus = db.Column(db.Numeric(15,4))
    imp_maximo_ajus = db.Column(db.Numeric(15,4))
    imp_minimo_ajus = db.Column(db.Numeric(15,4))
    imp_cierre_ajus = db.Column(db.Numeric(15,4))    
    fch_registro = db.Column(db.Date)
    
    @classmethod
    def eliminar_x_symbol(cls, cod_symbol):
        stmt = db.session.delete(
            SerieMensualModel
        ).where(
            SerieMensualModel.cod_symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        return result