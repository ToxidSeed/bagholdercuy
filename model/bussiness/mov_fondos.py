from model.TransaccionFondosModel import TransaccionFondosModel
from model.conversionmoneda import ConversionMonedaModel
from model.MovimientoFondosModel import MovimientoFondosModel
from model.MonedaModel import MonedaModel
from config.app_constants import TIPO_MOV_INGRESO,  TIPO_MOV_SALIDA
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

    def procesar(self, ingreso:TransaccionFondosModel, conversion:ConversionMonedaModel=None):
        imp_mov = ingreso.imp_transaccion
        mon_mov_id = ingreso.mon_trans_id
        imp_saldo_mov = ingreso.imp_transaccion

        if conversion is not None:
            imp_mov = conversion.imp_convertido
            mon_mov_id = conversion.mon_dest_id
            imp_saldo_mov = imp_mov

        new_mov = MovimientoFondosModel(
            trans_id = ingreso.id,
            fch_transaccion= ingreso.fch_transaccion,
            num_transaccion=ingreso.num_transaccion,
            tipo_trans_id = ingreso.tipo_trans_id,
            tipo_mov_id = TIPO_MOV_INGRESO,
            imp_mov = imp_mov,
            mon_mov_id = mon_mov_id,
            imp_saldo_mov = imp_saldo_mov,
            usuario_id = ingreso.usuario_id,            
            fch_audit = datetime.now()
        )
        db.session.add(new_mov)

class Salida(MovFondosHandler):
    def __init__(self, transaccion:TransaccionFondosModel):
        self.imp_pend_retirar = float(transaccion.imp_transaccion)
        self.usuario_id = transaccion.usuario_id
        self.transaccion = transaccion

    def procesar(self):
        self._val_salida()
        self._check_moneda(self.transaccion.mon_trans_id)
        funds = self.__get_positive_banlance() 
        self.actualizar_saldos(movs=funds)      

    def _val_salida(self):
        saldo_total = self.__get_saldo_total()
        if saldo_total == 0:
            raise AppException(msg="El saldo en la moneda ({0}) es 0".format(self.transaccion.mon_trans_id))

        if self.imp_pend_retirar > saldo_total:
            raise AppException(msg="El importe a retirar {0} es mayor al saldo total {1}".format(self.imp_pend_retirar, saldo_total))

    def __get_saldo_total(self):
        saldo_total = 0
        query = db.session.query(
            func.coalesce(func.sum(MovimientoFondosModel.imp_saldo_mov),0).label("saldo_total")
        ).filter(
            MovimientoFondosModel.tipo_mov_id == TIPO_MOV_INGRESO,
            MovimientoFondosModel.imp_saldo_mov > 0.00,
            MovimientoFondosModel.usuario_id == self.transaccion.usuario_id,
            MovimientoFondosModel.mon_mov_id == self.transaccion.mon_trans_id
        )
        
        resp = query.first()

        if resp is not None:
            saldo_total = float(resp.saldo_total)

        return saldo_total

    def __get_positive_banlance(self):
        funds = MovimientoFondosModel.query.filter(
            MovimientoFondosModel.tipo_mov_id == TIPO_MOV_INGRESO,
            MovimientoFondosModel.imp_saldo_mov > 0.00,
            MovimientoFondosModel.usuario_id == self.transaccion.usuario_id,
            MovimientoFondosModel.mon_mov_id == self.transaccion.mon_trans_id
        ).order_by(MovimientoFondosModel.fch_transaccion.asc(), MovimientoFondosModel.num_transaccion.asc())\
        .all()

        return funds

    def actualizar_saldos(self, movs=[]):
        for fund in movs:            
            (mov_fondo,imp_a_retirar) = self.act_saldo_mov(mov_fondo=fund)
            self.crear_movimiento_salida(mov_fondo, imp_a_retirar)
            if self.imp_pend_retirar == 0:
                break

    def act_saldo_mov(self,mov_fondo:MovimientoFondosModel=None):
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
        return (mov_fondo, imp_a_retirar)        

    def crear_movimiento_salida(self,mov_origen:MovimientoFondosModel=None,imp_a_retirar=0):
        mov_salida = MovimientoFondosModel(
            trans_id = self.transaccion.id,
            num_transaccion = self.transaccion.num_transaccion,
            fch_transaccion = self.transaccion.fch_transaccion,
            ref_mov_id = mov_origen.id,
            tipo_trans_id = self.transaccion.tipo_trans_id,
            tipo_mov_id=TIPO_MOV_SALIDA,
            imp_mov = imp_a_retirar,
            mon_mov_id = self.transaccion.mon_trans_id,
            imp_saldo_mov = 0,
            usuario_id = self.transaccion.usuario_id,
            fch_audit=datetime.now()            
        )
        db.session.add(mov_salida)