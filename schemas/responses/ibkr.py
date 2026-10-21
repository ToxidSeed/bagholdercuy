from config.extensions import ma


class IbkrContractSchema(ma.Schema):
    conid = ma.Integer()
    cod_symbol = ma.String()
    exchange = ma.String()
    fch_hr_registro = ma.DateTime()


ibkr_contract_schema = IbkrContractSchema()
ibkr_contracts_schema = IbkrContractSchema(many=True)
