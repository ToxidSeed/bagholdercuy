from config.extensions import ma


class ContratoOpcionResponseSchema(ma.Schema):
    id_contrato_opcion = ma.Integer()
    id_symbol_subyacente = ma.Integer(allow_none=True)
    cod_symbol = ma.String(required=True)
    cod_symbol_subyacente = ma.String(allow_none=True)
    tipo_opcion = ma.String(required=True)
    fch_vencimiento = ma.Date(allow_none=True)
    imp_strike = ma.Float(allow_none=True)
    tam_contrato = ma.Integer(allow_none=True)
    cod_moneda = ma.String(allow_none=True)
    descripcion = ma.String(allow_none=True)
    fch_registro = ma.DateTime(allow_none=True)
    fch_audit = ma.DateTime(allow_none=True)

    # Campos de compatibilidad con vistas cliente
    description = ma.Method("get_description")
    expiration_date = ma.Method("get_expiration_date")
    side = ma.Method("get_side")
    strike = ma.Method("get_strike")
    underlying = ma.Method("get_underlying")

    def get_description(self, obj):
        return getattr(obj, "descripcion", None) or getattr(obj, "description", None)

    def get_expiration_date(self, obj):
        val = getattr(obj, "fch_vencimiento", None) or getattr(obj, "expiration_date", None)
        if hasattr(val, "isoformat"):
            return val.isoformat()
        return str(val) if val is not None else None

    def get_side(self, obj):
        return getattr(obj, "tipo_opcion", None) or getattr(obj, "side", None)

    def get_strike(self, obj):
        val = getattr(obj, "imp_strike", None) or getattr(obj, "strike", None)
        return float(val) if val is not None else None

    def get_underlying(self, obj):
        return getattr(obj, "cod_symbol_subyacente", None) or getattr(obj, "underlying", None)


class ContratoOpcionChainResponseSchema(ma.Schema):
    calls = ma.Nested(ContratoOpcionResponseSchema, many=True)
    puts = ma.Nested(ContratoOpcionResponseSchema, many=True)
    exp_dates = ma.List(ma.String())
    strikes = ma.List(ma.Float())


class ContratoOpcionResumenResponseSchema(ma.Schema):
    cod_symbol_subyacente = ma.String()
    fch_registro = ma.DateTime(allow_none=True)
    fch_vencimiento = ma.Date(allow_none=True)


contrato_opcion_response_schema = ContratoOpcionResponseSchema()
contratos_opcion_response_schema = ContratoOpcionResponseSchema(many=True)
contrato_opcion_chain_response_schema = ContratoOpcionChainResponseSchema()
contrato_opcion_resumen_list_response_schema = ContratoOpcionResumenResponseSchema(many=True)
