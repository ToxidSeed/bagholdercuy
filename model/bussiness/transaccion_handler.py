from model.TransaccionFondosModel import TransaccionFondosModel
from model.balance import BalanceCuentaModel
from model.MonedaModel import MonedaModel
from common.AppException import AppException
from app import app, db
from sqlalchemy import func, true, and_

class TransaccionHandler:
    def __init__(self):
        pass

    def get_sig_num_transaccion(self, fec_transaccion="", num_trans_ref="", tipo_insert=""):
        num_trans = 0
        query = db.session.query(
            func.coalesce(func.max(TransaccionFondosModel.num_transaccion),0).label("num_transaccion")
        ).filter(
            TransaccionFondosModel.fec_transaccion == fec_transaccion
        )

        if num_trans_ref != "":
            if tipo_insert == "ANTES":
                query.filter(TransaccionFondosModel.num_transaccion < num_trans_ref)
            if tipo_insert == "DESPUES":
                query.filter(TransaccionFondosModel.num_transaccion <= num_trans_ref)

        result = query.first()

        if result is not None:
            num_trans = result.num_transaccion + 1
        
        return num_trans
    
    def _check_moneda(self, moneda_symbol=""):
        moneda_found = MonedaModel.query.filter(
            MonedaModel.moneda_id == moneda_symbol
        ).first()

        if moneda_found is None:
            raise AppException(msg="La moneda {0} no existe en la base de datos".format(moneda_symbol))

        return True

    def get_saldos_cuenta(self, moneda_id, usuario_id):
        saldo = BalanceCuentaModel.query.filter(
            BalanceCuentaModel.usuario_id == usuario_id,
            BalanceCuentaModel.moneda_id == moneda_id
        ).first()

        return saldo
