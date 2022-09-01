from model.TransaccionFondosModel import TransaccionFondosModel
from model.bussiness.transaccion_handler import TransaccionHandler
from model.bussiness.mov_fondos import Ingreso, Salida
from app import db
import copy

class ConversionMonedaHandler:
    def __init__(self):
        pass

    def convertir(self, conversion:TransaccionFondosModel=None):
        conversion.num_transaccion = TransaccionHandler().get_sig_num_transaccion(fec_transaccion=conversion.fec_transaccion)
        db.session.add(conversion)
        db.session.flush()

        ingreso = copy.copy(conversion)        
        ingreso.imp_transaccion = ingreso.imp_dest_conv
        ingreso.mon_trans_id = ingreso.mon_dest_conv_id        

        #crear el/los movimientos de salida
        Salida().procesar(conversion)
        #crear el movimiento de ingreso
        Ingreso().procesar(ingreso)
        

        