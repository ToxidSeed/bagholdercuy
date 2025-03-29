from app import db

class VariacionDiariaModel(db.Model):
    __tablename__ = "tb_variacion_diaria"

    symbol = db.Column(db.String, primary_key=True)
    fch_serie = db.Column(db.Date, primary_key=True)
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
    imp_variacion_maximo_minimo = db.Column(db.Numeric(15, 4))

    @classmethod
    def eliminar_x_symbol(cls, cod_symbol):
        rows_affected = db.session.query(
            VariacionDiariaModel
        ).where(
            VariacionDiariaModel.symbol == cod_symbol
        ).delete()
        
        return rows_affected

    @classmethod
    def eliminar_x_symbol_desde_fecha(cls, cod_symbol, fch_desde):
        rows_affected = db.session.query(
            VariacionDiariaModel
        ).where(
            VariacionDiariaModel.symbol == cod_symbol,
            VariacionDiariaModel.fch_serie >= fch_desde
        ).delete()
                
        return rows_affected



        
