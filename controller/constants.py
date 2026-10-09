from controller.base import Base
from model.tipo_transaccion import TipoTransaccionModel
from model.symbol_type import SymbolTypeModel
from reader.tipo_transaccion import TipoTransaccionReader
from reader.symbol_type import SymbolTypeReader
from common.Response import Response

class ConstantsController(Base):
    def get_list(self, args={}):
        try:
            constants_resp = {
                "tiposTransaccion": self.get_tipos_transaccion(),
                "symbolTypes":self.get_symbol_types()                
            }

            return Response().from_raw_data(constants_resp)
        except Exception as e:
            return Response().from_exception(e)

    def get_tipos_transaccion(self, args={}):
        records = TipoTransaccionReader.get_list()
        return {row.cod_tipo_transaccion: {"code":row.cod_tipo_transaccion, "value":row.id_tipo_transaccion, "label":row.nom_tipo_transaccion} for row in records} 

    def get_symbol_types(self, args={}):
        records = SymbolTypeReader.get_list()
        return {row.cod_symbol_type : {"code":row.cod_symbol_type, "value":row.id_symbol_type, "label":row.nom_symbol_type} for row in records}
