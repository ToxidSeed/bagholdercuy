from config.extensions import db

class VariacionSemanalModel(db.Model):
    __tablename__="tb_variacion_semanal"

    symbol = db.Column(db.String, primary_key=True)
    fecha = db.Column(db.Date, primary_key=True)
    cod_semana = db.Column(db.Integer)
    anyo = db.Column(db.Integer)
    semana = db.Column(db.Integer)
    imp_cierre_ant = db.Column(db.Numeric(15,4))
    imp_apertura = db.Column(db.Numeric(15,4))
    imp_maximo = db.Column(db.Numeric(15,4))
    imp_minimo = db.Column(db.Numeric(15,4))
    imp_cierre = db.Column(db.Numeric(15,4))
    pct_variacion_cierre = db.Column(db.Numeric(8,4))
    imp_variacion_cierre = db.Column(db.Numeric(15,4))
    pct_variacion_maximo = db.Column(db.Numeric(8,4))
    imp_variacion_maximo = db.Column(db.Numeric(15,4))
    pct_variacion_minimo = db.Column(db.Numeric(8,4))
    imp_variacion_minimo = db.Column(db.Numeric(15,4))


    @classmethod
    def eliminar_x_symbol(cls, cod_symbol):
        result = VariacionSemanalModel.query.filter(VariacionSemanalModel.symbol == cod_symbol).delete()        
        return result

    @classmethod
    def eliminar_desde_fecha(cls, cod_symbol, fch_semana_desde):
        stmt = db.session.query(
            VariacionSemanalModel
        ).where(
            VariacionSemanalModel.symbol == cod_symbol,
            VariacionSemanalModel.fecha >= fch_semana_desde
        )
    
        rows_affected = stmt.delete()
        return rows_affected

    @classmethod
    def insertar_pandas_dataframe(cls, df):
        db.session.bulk_insert_mappings(cls, df.to_dict(orient="records"))



