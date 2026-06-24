from config.extensions import ma

class TransaccionAgrupadaSchema(ma.Schema):
    cod_symbol = ma.String()
    max_fch_hr_transaccion = ma.DateTime()
    min_fch_hr_transaccion = ma.DateTime()
    min_orden_fifo = ma.Integer()
    ctd_transacciones = ma.Integer()

transacciones_agrupadas_schema = TransaccionAgrupadaSchema(many=True)