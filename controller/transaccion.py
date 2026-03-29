from controller.base import Base
from reader.transaccion import TransaccionReader
from common.Response import Response

class TransaccionController(Base):
    def get_fechas_con_transacciones(self, args=None):
        id_cuenta = args.get("id_cuenta")
        cod_symbol = args.get("cod_symbol")
        fch_ini = args.get("fch_ini")
        fch_fin = args.get("fch_fin")
        results = TransaccionReader.get_fechas_con_transacciones(id_cuenta, cod_symbol, fch_ini, fch_fin)
        return Response().from_raw_data(results)

    def get_transacciones_x_fecha(self, args=None):
        id_cuenta = args.get("id_cuenta")
        cod_symbol = args.get("cod_symbol")
        fch_transaccion = args.get("fch_transaccion")
        results = TransaccionReader.get_transacciones_x_fecha(id_cuenta, cod_symbol, fch_transaccion)
        return Response().from_raw_data(results)

    def get_transacciones_x_symbol(self, args=None):
        id_cuenta = args.get("id_cuenta")
        cod_symbol = args.get("cod_symbol")
        results = TransaccionReader.get_transacciones_x_symbol(id_cuenta, cod_symbol)
        return Response().from_raw_data(results)