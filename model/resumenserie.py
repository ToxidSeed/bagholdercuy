from config.extensions import db

class ResumenSerieModel(db.Model):
    __tablename__ = 'tb_resumen_serie'

    cod_symbol = db.Column(db.String(80), primary_key=True)
    fch_primera_serie_diaria = db.Column(db.Date)
    fch_ultima_serie_diaria = db.Column(db.Date)
    num_series_diarias = db.Column(db.Integer)
    fch_primera_var_diaria = db.Column(db.Date)
    fch_ultima_var_diaria = db.Column(db.Date)
    num_var_diarias = db.Column(db.Integer)
    fch_primera_serie_semanal = db.Column(db.Date)
    fch_ultima_serie_semanal = db.Column(db.Date)
    num_series_semanales = db.Column(db.Integer)
    fch_primera_var_semanal = db.Column(db.Date)
    fch_ultima_var_semanal = db.Column(db.Date)
    num_var_semanales = db.Column(db.Integer)
    fch_primera_serie_mensual = db.Column(db.Date)
    fch_ultima_serie_mensual = db.Column(db.Date)
    num_series_mensuales = db.Column(db.Integer)
    fch_primera_var_mensual = db.Column(db.Date)
    fch_ultima_var_mensual = db.Column(db.Date)
    num_vars_mensuales = db.Column(db.Date)
    fch_registro = db.Column(db.Date)
    fch_actualizacion = db.Column(db.DateTime)

    @classmethod
    def get_all(cls, params = {}):
        stmt = db.session.query(
            ResumenSerieModel
        )

        results = db.session.execute(stmt)
        record = results.scalars().all()
        return record

    @classmethod
    def get_record(cls, cod_symbol):
        stmt = db.session.query(
            ResumenSerieModel
        ).where(
            ResumenSerieModel.cod_symbol == cod_symbol
        )

        results = db.session.execute(stmt)
        record = results.scalars().first()
        return record
