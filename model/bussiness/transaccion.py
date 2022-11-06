from model.TransaccionFondosModel import TransaccionFondosModel
from model.MovimientoFondosModel import MovimientoFondosModel
from model.conversionmoneda import ConversionMonedaModel
from model.balance import BalanceCuentaModel
from model.MonedaModel import MonedaModel
from model.usuario import UsuarioModel

from common.AppException import AppException
from common.auth import Auth

from model.bussiness.mov_fondos import Ingreso, Salida
from config.negocio import TIPO_TRANS_CONVERSION, TIPO_TRANS_DEPOSITO, TIPO_TRANS_RETIRO
from config.negocio import REPROCESO_PROF_FONDOS_TODO, REPROCESO_PROF_FONDOS_FCH_CIERRE
from app import app, db

from sqlalchemy import func, true, and_
from datetime import datetime, date

class TransaccionHandler:
    def __init__(self, usuario):
        self.usuario = usuario

    def get_sig_num_transaccion(usuario_id, fch_transaccion=""):
        num_trans = 0
        query = db.session.query(
            func.coalesce(func.max(TransaccionFondosModel.num_transaccion),0).label("num_transaccion"),            
        ).filter(
            TransaccionFondosModel.fch_transaccion == fch_transaccion,
            TransaccionFondosModel.usuario_id == usuario_id
        )

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

    def ult_transaccion(usuario_id, fch_transaccion):
        result = TransaccionFondosModel.query.filter(
            TransaccionFondosModel.usuario_id == usuario_id,
            TransaccionFondosModel.fch_transaccion > fch_transaccion
        ).first()

        if result is None:
            return True
        else:
            return False

class ReorganizarHandler:
    def __init__(self, usuario):
        self.usuario = usuario

    def procesar(self, fch_reorganizar, list_trans=[], list_eli_trans=[]):        
        self.reenum_list_trans(list_trans)
        self.eli_list_trans(list_eli_trans)  
        #db.session.flush()
        self.veri_integridad_fecha(fch_reorganizar)
        #reprocesar
        ReprocesadorFondosHandler(usuario=self.usuario).procesar()

    def veri_integridad_fecha(self, fch_transaccion):
        grupos = db.session.query(
            TransaccionFondosModel.fch_transaccion,
            TransaccionFondosModel.num_transaccion,
            func.count(1).label("cantidd")
        ).filter(
            TransaccionFondosModel.fch_transaccion == fch_transaccion
        ).group_by(
            TransaccionFondosModel.fch_transaccion,
            TransaccionFondosModel.num_transaccion
        ).having(
            func.count(1) > 1
        ).all()

        if len(grupos) > 0:
            raise AppException(msg="Error al reenumerar las transacciones")


    def reenum_list_trans(self,list_trans=[]):
        for trans in list_trans:
            self.reenum_trans(trans)

    def reenum_trans(self, trans_reenum):
        trans = TransaccionFondosModel.query.filter(
            TransaccionFondosModel.id == trans_reenum.get('id')
        ).one()

        if trans is None:
            raise AppException(msg="No se ha encontrado una transacción para el id {0}".format(trans_reenum.get('id')))        

        trans.num_transaccion = trans_reenum.get('num_transaccion')

    def eli_list_trans(self,list_eli_trans=[]):
        for trans in list_eli_trans:
            self.eli_trans(trans)
    
    def eli_trans(self, trans):
        TransaccionFondosModel.query.filter(
            TransaccionFondosModel.id == trans.get('id')
        ).delete()
                    

class ReprocesadorFondosHandler:
    def __init__(self, usuario, fch_desde=None, tipo_reproceso=REPROCESO_PROF_FONDOS_TODO):        
        self.fch_desde = fch_desde
        self.usuario = usuario
        self.tipo_reproceso = tipo_reproceso        

    def procesar(self):        
        trasacciones = self.get_transacciones()

        #borrar los movimientos
        self.eliminar_movimientos()        

        #borrar los registros de conversion
        #self.re_conversiones()

        #reprocesar las transacciones
        self.repro_transacciones(trasacciones)

    def get_transacciones(self):
        query = TransaccionFondosModel.query.filter(
            TransaccionFondosModel.usuario_id == self.usuario.id
        )
        if self.tipo_reproceso == REPROCESO_PROF_FONDOS_FCH_CIERRE:
            query = query.filter(
                TransaccionFondosModel.fch_transaccion >= fch_desde
            )

        results = query.all()
        return results

    def eliminar_movimientos(self):
        query = MovimientoFondosModel.query.filter(
            MovimientoFondosModel.usuario_id == self.usuario.id
        )

        if self.tipo_reproceso == REPROCESO_PROF_FONDOS_FCH_CIERRE:
            query = query.filter(
                MovimientoFondosModel.fch_transaccion >= fch_desde
            )
        query.delete()
    
    def re_conversiones(self):
        query = ConversionMonedaModel.query.filter(
            ConversionMonedaModel.usuario_id == self.usuario.id
        )
        if self.tipo_reproceso == REPROCESO_PROF_FONDOS_FCH_CIERRE:
            query = query.filter(
                ConversionMonedaModel.fch_conversion >= fch_desde
            )
        query.delete()
    
    def repro_transacciones(self, trans_list=[]):
        for transaccion in trans_list:
            self.proc_transaccion(transaccion)

    def proc_transaccion(self, transaccion:TransaccionFondosModel):                
        if transaccion.tipo_trans_id == TIPO_TRANS_DEPOSITO:
            DepositoHandler(self.usuario).gen_movimientos(transaccion)            

        if transaccion.tipo_trans_id == TIPO_TRANS_RETIRO:
            RetiroHandler().gen_movimientos(transaccion)
        
        if transaccion.tipo_trans_id == TIPO_TRANS_CONVERSION:
            conversion = TransaccionFondosModel.get_conversion(transaccion.id)            
            ConversionMonedaHandler().gen_movimientos(transaccion, conversion)
            


class DepositoHandler(TransaccionHandler):
    def __init__(self, usuario:UsuarioModel=None):
        self.usuario = usuario

    def add(self, new_deposit:TransaccionFondosModel=None):                          
        #seteando el número de la transacción
        num_trans = TransaccionHandler.get_sig_num_transaccion(self.usuario.id, fch_transaccion=new_deposit.fch_transaccion)        
        new_deposit.num_transaccion = num_trans         
        #calculando los saldos  
        #saldocuenta = self.calc_saldos(new_deposit)
        #verificando la moneda
        self._check_moneda(new_deposit.mon_trans_id)
        #insertando la transaccion correspondiente al deposito
        db.session.add(new_deposit)
        db.session.flush()
                
        #Si no es la última transacción se reprocesa todos los movimientos
        if TransaccionHandler.ult_transaccion(self.usuario.id, new_deposit.fch_transaccion) == False:
            ReprocesadorFondosHandler(self.usuario).procesar()
        else:
            #generando los movimientos que generan un dsposito
            self.gen_movimientos(deposito=new_deposit)

    def gen_movimientos(self, deposito:TransaccionFondosModel):        
        Ingreso().procesar(deposito)

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
        
class RetiroHandler(TransaccionHandler):
    def __init__(self):        
        self.imp_pend_retirar = 0        
        self.usuario = None

    def retirar(self, retiro:TransaccionFondosModel=None):
        self.usuario = UsuarioModel.get(retiro.usuario_id)

        #insertamos la transacción de retiro
        retiro.num_transaccion = TransaccionHandler.get_sig_num_transaccion(retiro.usuario_id, fch_transaccion=retiro.fch_transaccion)        
        db.session.add(retiro)

        #Si no es la última transacción se reprocesa todos los movimientos
        if TransaccionHandler.ult_transaccion(self.usuario.id, retiro.fch_transaccion) == False:
            ReprocesadorFondosHandler(self.usuario).procesar()
        else:        
            #generamos los movimientos que requiere la salida
            self.gen_movimientos(retiro)        

    def gen_movimientos(self, retiro:TransaccionFondosModel):        
        Salida(retiro).procesar()


class ConversionMonedaHandler:
    def __init__(self):
        self.usuario = None

    def procesar(self, conversion:ConversionMonedaModel):
        self.usuario = UsuarioModel.get(conversion.usuario_id)

        transaccion = self.gen_transaccion(conversion)        
        #conversion.num_transaccion = TransaccionHandler().get_sig_num_transaccion(fec_transaccion=conversion.fec_transaccion)
        conversion.transaccion_id = transaccion.id
        db.session.add(conversion)

        #Si no es la última transacción se reprocesa todos los movimientos
        if TransaccionHandler.ult_transaccion(self.usuario.id, transaccion.fch_transaccion) == False:
            ReprocesadorFondosHandler(self.usuario).procesar()
        else:                
            self.gen_movimientos(transaccion, conversion)

    def gen_movimientos(self, transaccion:TransaccionFondosModel, conversion:ConversionMonedaModel):        
        #crear el/los movimientos de salida
        Salida(transaccion).procesar()

        #crear el movimiento de ingreso
        Ingreso().procesar(transaccion,conversion=conversion)

    def gen_transaccion(self, conversion:ConversionMonedaModel):        

        info_adicional = "fch_conver:{0}, tc:{1}, oper:{2}, origen:{3} {4}, destino:{5} {6}".format(conversion.fch_conversion,conversion.imp_tc,conversion.operacion_id,conversion.imp_origen,conversion.mon_ori_id, conversion.imp_convertido,conversion.mon_dest_id)

        transaccion = TransaccionFondosModel(            
            fch_transaccion = conversion.fch_conversion,  
            num_transaccion = TransaccionHandler.get_sig_num_transaccion(conversion.fch_conversion),
            tipo_trans_id=TIPO_TRANS_CONVERSION,         
            imp_transaccion=conversion.imp_origen,
            mon_trans_id=conversion.mon_ori_id, 
            info_adicional= info_adicional,                      
            fch_registro = date.today(),
            usuario_id = conversion.usuario_id,
            fch_audit = datetime.now()            
        )

        db.session.add(transaccion)
        db.session.flush()
        return transaccion
            
        