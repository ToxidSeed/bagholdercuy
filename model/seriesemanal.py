from config.extensions import db
from sqlalchemy import delete

class SerieSemanalModel(db.Model):
    __tablename__ = "tb_serie_semanal"

    symbol = db.Column(db.String, primary_key=True)
    fch_semana = db.Column(db.Date, primary_key=True)
    anyo = db.Column(db.Integer)
    semana = db.Column(db.Integer)
    cod_semana = db.Column(db.Integer)
    imp_apertura = db.Column(db.Numeric(15,4))
    imp_maximo = db.Column(db.Numeric(15,4))
    imp_minimo = db.Column(db.Numeric(15,4))
    imp_cierre = db.Column(db.Numeric(15,4))    
    imp_apertura_sin_ajus = db.Column(db.Numeric(15,4))
    imp_maximo_sin_ajus = db.Column(db.Numeric(15,4))
    imp_minimo_sin_ajus = db.Column(db.Numeric(15,4))
    imp_cierre_sin_ajus = db.Column(db.Numeric(15,4))    
    fch_registro = db.Column(db.Date)
    
    @classmethod
    def eliminar_x_symbol(cls, cod_symbol):  
        stmt = delete(
            SerieSemanalModel
        ).where(
            SerieSemanalModel.symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        return result

    @classmethod
    def eliminar_por_symbol_desde_fecha(cls, cod_symbol, fch_semana):
        rows_affected = db.session.query(
            SerieSemanalModel
        ).where(
            SerieSemanalModel.symbol == cod_symbol,
            SerieSemanalModel.fch_semana >= fch_semana
        ).delete()

        return rows_affected

    @classmethod
    def insertar_pandas_dataframe(cls, df):
        objects = [cls(**row) for row in df.to_dict(orient="records")]
        db.session.add_all(objects)