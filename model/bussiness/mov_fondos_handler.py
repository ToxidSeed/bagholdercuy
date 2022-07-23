from model.TransaccionFondosModel import TransaccionFondosModel
from model.MovimientoFondosModel import MovimientoFondosModel
from config.negocio import TIPO_MOV_INGRESO
from datetime import datetime
from app import app, db

class MovFondosHandler:
    def __init__(self):
        pass

    def de_deposito(self, ingreso:TransaccionFondosModel=None):
        new_mov = MovimientoFondosModel(
            trans_id = ingreso.id,
            tipo_trans_id = ingreso.tipo_trans_id,
            tipo_mov_id = TIPO_MOV_INGRESO,
            imp_mov = ingreso.imp_transaccion,
            mon_mov_id = ingreso.mon_trans_id,
            imp_saldo_mov = ingreso.imp_transaccion,
            fch_audit = datetime.now()
        )
        db.session.add(new_mov)

    def calc_saldo_cuenta(self):
        pass

    def calc_saldo_cuenta_usd(self):
        pass