from controller.base import Base
from reader.transaccion import TransaccionReader
from common.AppException import AppException
from common.Response import Response
from common.Formatter import Formatter

from parser.posicion import PosicionParser

from domain.contratoopcion import ContratoOpcion

class PosicionManager(Base):
    def get_posiciones_acciones(self, args={}):
        args = PosicionParser.parse_args_get_posiciones_acciones(args=args)
        id_cuenta = args.get("id_cuenta")        
        records = TransaccionReader.get_pos_abiertas_agrup_x_accion(id_cuenta=id_cuenta)
        return Response().from_raw_data(records)
    
    def get_posiciones_contratos_opciones(self, args={}):
        args = PosicionParser.parse_args_get_posiciones_contratos_opciones(args=args)
        id_cuenta = args.get("id_cuenta")
        records = TransaccionReader.get_pos_abiertas_agrup_x_contrato_opcion(id_cuenta=id_cuenta)

        records_output = []
        for posicion in records:            
            cod_contrato_opcion = ContratoOpcion(posicion.symbol)
            posicion_dict = Formatter().format(posicion)
            posicion_dict["cod_symbol_subyacente"] = cod_contrato_opcion.cod_symbol_subyacente
            posicion_dict["cod_tipo_opcion"] = cod_contrato_opcion.cod_tipo_opcion
            posicion_dict["fch_expiracion"] = cod_contrato_opcion.fch_expiracion
            posicion_dict["imp_ejercicio"] = cod_contrato_opcion.imp_ejercicio
            records_output.append(posicion_dict)

        return Response().from_raw_data(records_output)