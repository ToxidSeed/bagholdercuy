from config.extensions import ma


class CotizacionResponseSchema(ma.Schema):
    id_symbol = ma.Integer(allow_none=True)
    id_contrato_opcion = ma.Integer(allow_none=True)
    cod_symbol = ma.String(required=True)
    imp_cierre = ma.Float(allow_none=True)
    imp_cierre_anterior = ma.Float(allow_none=True)
    imp_variacion = ma.Float(allow_none=True)
    pct_variacion = ma.Float(allow_none=True)
    provider = ma.String(allow_none=True)


cotizacion_response_schema = CotizacionResponseSchema()
cotizaciones_response_schema = CotizacionResponseSchema(many=True)
