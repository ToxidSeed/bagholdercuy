from controller.base import Base
from model.tipo_transaccion import TipoTransaccionModel
from model.instrumento_financiero import InstrumentoFinancieroModel
from reader.tipo_transaccion import TipoTransaccionReader
from reader.instrumento_financiero import InstrumentoFinancieroReader
from common.Response import Response

class ConstantsController(Base):
    def get_list(self, args={}):
        try:
            constants_resp = {
                "tiposTransaccion": self.get_tipos_transaccion(),
                "instrumentosFinancieros":self.get_instrumentos_financieros()                
            }

            return Response().from_raw_data(constants_resp)
        except Exception as e:
            return Response().from_exception(e)

    def get_tipos_transaccion(self, args={}):
        records = TipoTransaccionReader.get_list()
        return {row.cod_tipo_transaccion: {"code":row.cod_tipo_transaccion, "value":row.id_tipo_transaccion, "label":row.nom_tipo_transaccion} for row in records} 

    def get_instrumentos_financieros(self, args={}):
        records = InstrumentoFinancieroReader.get_list()
        return {row.cod_instrumento_financiero : {"code":row.cod_instrumento_financiero, "value":row.id_instrumento_financiero, "label":row.nom_instrumento_financiero} for row in records}
