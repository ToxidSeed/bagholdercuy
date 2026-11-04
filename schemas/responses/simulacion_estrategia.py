from config.extensions import ma
from marshmallow import fields


class SimulacionPataResponseSchema(ma.Schema):
    id = fields.Integer(attribute="id_simulacion_pata")
    id_contrato_opcion = fields.Integer(allow_none=True)
    cod_symbol = fields.String(required=True)
    tipo = fields.String(attribute="tipo_opcion", required=True)
    strike = fields.Float(required=True)
    fch_vencimiento = fields.Date(attribute="fecha_vencimiento", required=True)
    posicion = fields.String(required=True)
    cantidad = fields.Integer(required=True)
    multiplicador = fields.Integer(required=True)
    precio_apertura = fields.Float(allow_none=True)
    moneda_id = fields.String(required=True)


class SimulacionGrupoResponseSchema(ma.Schema):
    id = fields.Integer(attribute="id_simulacion_grupo")
    orden = fields.Integer(required=True)
    nombre = fields.String(required=True)
    tipo = fields.String(required=True)
    contratos = fields.Nested(
        SimulacionPataResponseSchema, many=True, attribute="patas"
    )


class SimulacionEstrategiaResponseSchema(ma.Schema):
    id = fields.Integer(attribute="id_simulacion_estrategia")
    fecha_guardado = fields.DateTime(
        attribute="fec_creacion", format="iso", allow_none=True
    )
    nombre = fields.String(required=True)
    tipo = fields.String(attribute="etiqueta", required=True)
    notas = fields.String(allow_none=True)
    instrumento = fields.Method("get_instrumento")
    num_grupos = fields.Method("get_num_grupos")
    total_contratos = fields.Method("get_total_contratos")
    resumen_patas = fields.Method("get_resumen_patas")
    resumen_flujo = fields.Method("get_resumen_flujo")
    grupos = fields.Nested(SimulacionGrupoResponseSchema, many=True)

    def get_instrumento(self, obj):
        symbol = getattr(obj, "subyacente", None)
        if not symbol:
            return None
        return {
            "id": symbol.id_symbol,
            "id_symbol": symbol.id_symbol,
            "symbol": symbol.symbol,
            "name": symbol.name,
            "asset_type": symbol.asset_type,
            "exchange": symbol.exchange,
        }

    def get_num_grupos(self, obj):
        return len(obj.grupos or [])

    def get_total_contratos(self, obj):
        return sum(len(grupo.patas or []) for grupo in (obj.grupos or []))

    def get_resumen_patas(self, obj):
        grupos = []
        for indice, grupo in enumerate(obj.grupos or [], start=1):
            patas = []
            for pata in grupo.patas or []:
                vencimiento = (
                    pata.fecha_vencimiento.isoformat()
                    if pata.fecha_vencimiento
                    else ""
                )
                patas.append(
                    f"{pata.posicion} {pata.cantidad}x {pata.tipo_opcion} "
                    f"${pata.strike} {vencimiento}"
                )
            grupos.append(
                f"[G{indice}] {grupo.nombre}: " + (" + ".join(patas) or "Sin patas")
            )
        return " | ".join(grupos)

    def get_resumen_flujo(self, obj):
        resumen = []
        for indice, grupo in enumerate(obj.grupos or [], start=1):
            total = 0.0
            tiene_precios = False
            for pata in grupo.patas or []:
                if pata.precio_apertura is None:
                    continue
                tiene_precios = True
                signo = -1 if pata.posicion == "LONG" else 1
                total += (
                    signo
                    * float(pata.precio_apertura)
                    * pata.multiplicador
                    * pata.cantidad
                )
            if tiene_precios:
                tipo = "CRÉDITO" if total > 0 else "DÉBITO"
                resumen.append(f"G{indice}: {tipo} ${abs(total):.2f}")
        return " | ".join(resumen) if resumen else None


simulacion_estrategia_response_schema = SimulacionEstrategiaResponseSchema()
simulacion_estrategias_response_schema = SimulacionEstrategiaResponseSchema(many=True)
