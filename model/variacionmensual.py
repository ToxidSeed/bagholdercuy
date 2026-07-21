from config.extensions import db


class VariacionMensualModel(db.Model):
    __tablename__ = "tb_variacion_mensual"

    cod_symbol = db.Column(db.String, primary_key=True)
    fch_mes = db.Column(db.Date, primary_key=True)
    cod_mes = db.Column(db.Integer)
    anyo = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    imp_cierre_ant = db.Column(db.Numeric(15,4))
    imp_apertura = db.Column(db.Numeric(15,4))
    imp_maximo = db.Column(db.Numeric(15,4))
    imp_minimo = db.Column(db.Numeric(15,4))
    imp_cierre = db.Column(db.Numeric(15,4))
    pct_variacion_cierre = db.Column(db.Numeric(8,4))
    imp_variacion_cierre = db.Column(db.Numeric(15,4))
    pct_variacion_apertura = db.Column(db.Numeric(8,4))
    imp_variacion_apertura = db.Column(db.Numeric(15,4))
    pct_variacion_maximo = db.Column(db.Numeric(8,4))
    imp_variacion_maximo = db.Column(db.Numeric(15,4))
    pct_variacion_minimo = db.Column(db.Numeric(8,4))
    imp_variacion_minimo = db.Column(db.Numeric(15,4))

    @classmethod
    def eliminar_x_symbol(cls, cod_symbol):
        rows_affected = db.session.query(
            VariacionMensualModel
        ).where(
            VariacionMensualModel.cod_symbol == cod_symbol
        ).delete()

        return rows_affected

    @classmethod
    def del_desde_fecha(cls, cod_symbol, fch_mes_desde):
        stmt = db.session.query(
            VariacionMensualModel
        ).where(
            VariacionMensualModel.cod_symbol == cod_symbol,
            VariacionMensualModel.fch_mes >= fch_mes_desde
        )

        rows_affected = stmt.delete()
        return rows_affected

    @classmethod
    def insertar_pandas_dataframe(cls, df):
        db.session.bulk_insert_mappings(cls, df.to_dict(orient="records"))

        

