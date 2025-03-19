from app import db
from sqlalchemy import delete

class SerieDiariaModel(db.Model):
    __tablename__ = "tb_serie_diaria"

    cod_symbol = db.Column(db.String, primary_key=True)
    fch_serie = db.Column(db.Date, primary_key=True)
    fch_semana = db.Column(db.Date)
    fch_mes = db.Column(db.Date)
    imp_apertura = db.Column(db.Numeric(15,4))
    imp_maximo = db.Column(db.Numeric(15,4))
    imp_minimo = db.Column(db.Numeric(15,4))
    imp_cierre = db.Column(db.Numeric(15,4))
    imp_apertura_sin_ajus = db.Column(db.Numeric(15.4))
    imp_maximo_sin_ajus = db.Column(db.Numeric(15.4))
    imp_minimo_sin_ajus = db.Column(db.Numeric(15.4))
    imp_cierre_sin_ajus = db.Column(db.Numeric(15.4))    
    fch_registro = db.Column(db.Date)


    # desde fecha mayor o igual
    @classmethod
    def eliminar_x_symbol_desde_fecha(cls, cod_symbol, fch_serie):
        stmt = delete(SerieDiariaModel).where(
            SerieDiariaModel.cod_symbol == cod_symbol,
            SerieDiariaModel.fch_serie >= fch_serie
        )
        db.session.execute(stmt)