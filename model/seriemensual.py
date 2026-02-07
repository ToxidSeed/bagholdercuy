from app import db
from sqlalchemy import delete

class SerieMensualModel(db.Model):
    __tablename__ = "tb_serie_mensual"

    cod_symbol = db.Column(db.String, primary_key=True)
    fch_mes = db.Column(db.Date, primary_key=True)
    anyo = db.Column(db.Integer)
    mes = db.Column(db.Integer)
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
            SerieMensualModel
        ).where(
            SerieMensualModel.cod_symbol == cod_symbol
        )

        result = db.session.execute(stmt)
        return result

    @classmethod
    def del_series_desde_fecha(cls, cod_symbol, fch_mes_desde):
        query = db.session.query(
            SerieMensualModel
        ).where(
            SerieMensualModel.cod_symbol == cod_symbol,
            SerieMensualModel.fch_mes >= fch_mes_desde
        )

        rows_affected = query.delete()
        return rows_affected

    @classmethod
    def insertar_pandas_dataframe(cls, df):
        db.session.bulk_insert_mappings(cls, df.to_dict(orient="records"))