from model.TransaccionFondosModel import TransaccionFondosModel
from model.bussiness.mov_fondos import Ingreso
from model.bussiness.transaccion_handler import TransaccionHandler
from model.usuario import UsuarioModel
from model.balance import BalanceCuentaModel
from app import app, db

class DepositoHandler(TransaccionHandler):
    def __init__(self, usuario:UsuarioModel=None):
        self.usuario = usuario

    def add(self, new_deposit:TransaccionFondosModel=None):                  
        #seteando el número de la transacción
        num_trans = self.get_sig_num_transaccion(fec_transaccion=new_deposit.fec_transaccion)        
        new_deposit.num_transaccion = num_trans         
        #calculando los saldos  
        saldocuenta = self.calc_saldos(new_deposit)
        #verificando la moneda
        self._check_moneda(new_deposit.mon_trans_id)
        #insertando la transaccion correspondiente al deposito
        db.session.add(new_deposit)
        db.session.flush()
        #generando los movimientos que generan un dsposito
        Ingreso().procesar(new_deposit,saldocuenta)

    def calc_saldos(self, deposito:TransaccionFondosModel):
        saldo_obj = self.get_saldos_cuenta(deposito.mon_trans_id, deposito.usuario_id)
        if saldo_obj is None:
            saldo_obj = self.crear_saldo_cuenta(deposito)
        else:
            saldo_obj.imp_saldo = float(saldo_obj.imp_saldo) + deposito.imp_transaccion
            
        #seteamos el saldo        
        return saldo_obj

    def crear_saldo_cuenta(self, deposito:TransaccionFondosModel):
        balance = BalanceCuentaModel(
            usuario_id = deposito.usuario_id,
            moneda_id = deposito.mon_trans_id,
            imp_saldo = deposito.imp_transaccion,
            imp_inversion = 0,
            mon_cuenta_id = self.usuario.moneda_id,
            imp_mon_cuenta = deposito.imp_transaccion,
            imp_inv_mon_cuenta = 0
        )
        db.session.add(balance)
        db.session.flush()
        return balance
        
    


        
    