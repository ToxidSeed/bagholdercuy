from config.extensions import ma


class IbkrContractMapResponseSchema(ma.Schema):
    id_ibkr_contract_map = ma.Integer(allow_none=True)
    id_symbol = ma.Integer(allow_none=True)
    id_contrato_opcion = ma.Integer(allow_none=True)
    conid = ma.Integer(required=True)
    cod_symbol = ma.String(allow_none=True)
    exchange = ma.String(allow_none=True)
    fch_registro = ma.String(allow_none=True)
    fch_audit = ma.String(allow_none=True)


ibkr_contract_map_response_schema = IbkrContractMapResponseSchema()
ibkr_contract_maps_response_schema = IbkrContractMapResponseSchema(many=True)
