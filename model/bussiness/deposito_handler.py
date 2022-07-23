from model.TransaccionFondosModel import TransaccionFondosModel
from controller.AuthManager import AuthManager
from model.bussiness.mov_fondos_handler import MovFondosHandler
from model.bussiness.transaccion_handler import TransaccionHandler
from app import app, db

class DepositoHandler(TransaccionHandler):
    def __init__(self):
        pass

    def add(self, new_deposit:TransaccionFondosModel=None):              
        auth_info = AuthManager().get_user_information()
        new_deposit.user_id =  auth_info["user_id"]
        num_trans = self.get_sig_num_transaccion(fec_transaccion=new_deposit.fec_transaccion)        
        new_deposit.num_transaccion = num_trans   
        #
        self._check_moneda(new_deposit.mon_trans_id)
        db.session.add(new_deposit)
        db.session.flush()
        #add mov
        MovFondosHandler().de_deposito(new_deposit)

        
    