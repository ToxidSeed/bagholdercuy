from model.TransaccionFondosModel import TransaccionFondosModel
from model.MovimientoFondosModel import MovimientoFondosModel
from model.MonedaModel import MonedaModel
from model.balance import BalanceCuentaModel
from config.negocio import TIPO_MOV_INGRESO,  TIPO_MOV_SALIDA
from common.AppException import AppException
from datetime import datetime
from app import app, db
from sqlalchemy import func

class MovFondosHandler:
    def __init__(self):
        pass

    def _check_moneda(self, moneda_symbol=""):
        moneda_found = MonedaModel.query.filter(
            MonedaModel.moneda_id  == moneda_symbol
        ).first()

        if moneda_found is None:
            raise AppException(msg="La moneda {0} no existe en la base de datos".format(moneda_symbol))

        return True    

    def calc_saldo_cuenta(self):
        pass


class Ingreso(MovFondosHandler):
    def __init__(self):
        pass

    def procesar(self, ingreso:TransaccionFondosModel=None, saldocuenta:BalanceCuentaModel=None):
        new_mov = MovimientoFondosModel(
            trans_id = ingreso.id,
            fch_transaccion= ingreso.fec_transaccion,
            num_transaccion=ingreso.num_transaccion,
            tipo_trans_id = ingreso.tipo_trans_id,
            tipo_mov_id = TIPO_MOV_INGRESO,
            imp_mov = ingreso.imp_transaccion,
            mon_mov_id = ingreso.mon_trans_id,
            imp_saldo_mov = ingreso.imp_transaccion,            
            imp_saldo_cuenta = saldocuenta.imp_saldo,
            fch_audit = datetime.now()
        )
        db.session.add(new_mov)

class Salida(MovFondosHandler):
    def __init__(self):
        pass

    def procesar(self, salida:TransaccionFondosModel=None):
        #
        self.imp_pend_retirar = salida.imp_transaccion
        #
        self._val_salida(salida)        
        #
        self._check_moneda(salida.mon_trans_id)
        #
        funds = self.__get_positive_banlance(salida) 
        #        
        self.actualizar_saldos(salida, funds)
        

    def _val_salida(self, salida:TransaccionFondosModel=None):
        saldo_total = self.__get_saldo_total(salida)
        if saldo_total == 0:
            raise AppException(msg="El saldo en la moneda ({0}) es 0".format(salida.mon_trans_id))

        if self.imp_pend_retirar > saldo_total:
            raise AppException(msg="El importe a retirar {0} es mayor al saldo total {1}".format(self.imp_pend_retirar, saldo_total))

    def __get_saldo_total(self, salida:TransaccionFondosModel=None):
        saldo_total = 0
        query = db.session.query(
            func.coalesce(func.sum(MovimientoFondosModel.imp_saldo_mov),0).label("saldo_total")
        ).filter(
            MovimientoFondosModel.tipo_mov_id == TIPO_MOV_INGRESO,
            MovimientoFondosModel.imp_saldo_mov > 0.00,
            MovimientoFondosModel.mon_mov_id == salida.mon_trans_id
        )
        
        resp = query.first()

        if resp is not None:
            saldo_total = float(resp.saldo_total)

        return saldo_total

    def __get_positive_banlance(self, salida:TransaccionFondosModel=None):
        funds = MovimientoFondosModel.query.filter(
            MovimientoFondosModel.tipo_mov_id == TIPO_MOV_INGRESO,
            MovimientoFondosModel.imp_saldo_mov > 0.00,
            MovimientoFondosModel.mon_mov_id == salida.mon_trans_id
        ).order_by(MovimientoFondosModel.fch_transaccion.asc(), MovimientoFondosModel.num_transaccion.asc())\
        .all()

        return funds

    def actualizar_saldos(self,salida=TransaccionFondosModel, movs=[]):
        for fund in movs:            
            self.act_saldo_mov(salida=salida,mov_fondo=fund)
            if self.imp_pend_retirar == 0:
                break

    def act_saldo_mov(self,salida:TransaccionFondosModel=None, mov_fondo:MovimientoFondosModel=None):
        #iniciar proceso de descuento
        #caso 1, si el importe del retiro es mayor al elemento a actualizar
        mov_saldo = float(mov_fondo.imp_saldo_mov)
        imp_a_retirar = 0
        if self.imp_pend_retirar > mov_saldo:
            imp_a_retirar = mov_saldo
            self.imp_pend_retirar = self.imp_pend_retirar - mov_saldo
            mov_fondo.imp_saldo_mov = 0                        

        #caso 2, si el importe del retiro es = al elemento a actualizar
        elif self.imp_pend_retirar == mov_saldo:
            imp_a_retirar = mov_saldo
            mov_fondo.imp_saldo_mov = 0
            self.imp_pend_retirar = 0

        #caso 3, si el importe del retiro es < al elemento a actualizar
        elif self.imp_pend_retirar < mov_saldo:
            imp_a_retirar = self.imp_pend_retirar
            mov_fondo.imp_saldo_mov = mov_saldo - self.imp_pend_retirar
            self.imp_pend_retirar = 0

        #agregar una entrada para el retiro
        self.crear_movimiento(salida,mov_fondo,imp_a_retirar)

    def crear_movimiento(self, salida:TransaccionFondosModel=None,mov_origen:MovimientoFondosModel=None,imp_mov=0):
        mov_salida = MovimientoFondosModel(
            trans_id = salida.id,
            num_transaccion = salida.num_transaccion,
            fch_transaccion = salida.fec_transaccion,
            ref_mov_id=mov_origen.id,
            tipo_trans_id=salida.tipo_trans_id,
            tipo_mov_id=TIPO_MOV_SALIDA,
            imp_mov=imp_mov,
            mon_mov_id=salida.mon_trans_id,
            imp_saldo_mov=0,
            fch_audit=datetime.now()
        )
        db.session.add(mov_salida)