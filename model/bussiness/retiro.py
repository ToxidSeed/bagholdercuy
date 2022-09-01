from model.TransaccionFondosModel import TransaccionFondosModel
from model.MovimientoFondosModel import MovimientoFondosModel
from model.bussiness.transaccion_handler import TransaccionHandler
from model.bussiness.mov_fondos import Salida
from controller.AuthManager import AuthManager
from common.AppException import AppException
from config.negocio import TIPO_MOV_INGRESO, TIPO_TRANS_RETIRO, TIPO_MOV_SALIDA
from datetime import datetime
from app import app, db
from sqlalchemy import func


class RetiroHandler(TransaccionHandler):
    def __init__(self):
        self.imp_pend_retirar = 0

    def retirar(self, retiro:TransaccionFondosModel=None):
        #insertamos la transacción de retiro
        retiro.num_transaccion = self.get_sig_num_transaccion(fec_transaccion=retiro.fec_transaccion)        
        db.session.add(retiro)
        #generamos los movimientos que requiere la salida
        Salida().procesar(retiro)
