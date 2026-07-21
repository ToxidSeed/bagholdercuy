from config.extensions import ma


class VariacionDiariaResponseSchema(ma.Schema):
    anyo = ma.Integer()
    symbol = ma.String()
    fch_serie = ma.Date()
    imp_cierre_ant = ma.Float()
    imp_apertura = ma.Float()
    imp_maximo = ma.Float()
    imp_minimo = ma.Float()
    imp_cierre = ma.Float()
    pct_variacion_apertura = ma.Float()
    imp_variacion_apertura = ma.Float()
    pct_variacion_cierre = ma.Float()
    imp_variacion_cierre = ma.Float()
    pct_variacion_maximo = ma.Float()
    imp_variacion_maximo = ma.Float()
    pct_variacion_minimo = ma.Float()
    imp_variacion_minimo = ma.Float()


variaciones_diarias_schema = VariacionDiariaResponseSchema(many=True)
