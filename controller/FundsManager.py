from inspect import trace
import traceback, sys
from datetime import date, datetime
from app import app, db

from common.Response import Response
from common.AppException import AppException
import config as CONFIG

from sqlalchemy import func, true, and_

from controller.AuthManager import AuthManager
from model.ConversionModel import ConversionModel
#from model.FundsHistory import FundsHistory
from model.TransaccionFondosModel import TransaccionFondosModel
from model.CurrencyModel import CurrencyModel
from model.CurrencyExchangeModel import CurrencyExchangeModel as CurrencyExchange
from model.MovimientoFondosModel import MovimientoFondosModel
from config.negocio import *
import config.negocio as CFG_NEG
import config.general as CFG_GEN
from model.bussiness.deposito_handler import DepositoHandler

class FundsManager:

    def __init__(self):
        pass

    def get_funds(self, args={}):
        symbol = args["symbol"]

        funds = db.session.query(\
            TransaccionFondosModel.moneda_symbol,\
            func.sum(TransaccionFondosModel.imp_saldo_trans).label("importe")\
        ).filter(
            TransaccionFondosModel.moneda_symbol.ilike("%{0}%".format(symbol)),
            TransaccionFondosModel.tipo_transaccion == CONFIG.CONST_TIPO_TRANSACCION_INGRESO,
            TransaccionFondosModel.imp_saldo_trans > 0.00
        ).group_by(TransaccionFondosModel.moneda_symbol).all()

        #import logging
        #logging.basicConfig()
        #logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        formats = {
            "importe":"{:0.2f}"
        }

        return Response().from_raw_data(funds, formats=formats)

class Historial:
    def __init__(self):
        pass

    def get(self, args={}):
        funds = db.session.query(
            TransaccionFondosModel
        ).order_by(TransaccionFondosModel.fec_transaccion.desc(), TransaccionFondosModel.num_transaccion.desc())\
        .all()

        return Response().from_raw_data(funds)   

class DepositResource():
    def __init__(self):
        pass

    def add(self, args={}):
        try:
            self.val_add(args)
            new_deposit = self.__collect(args)            
            DepositoHandler().add(new_deposit)
            db.session.commit()
            return Response(msg="Se ha depositado correctamente {0} {1}".format(new_deposit.mon_trans_id,new_deposit.imp_transaccion)).get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def val_add(self, args={}):
        errors = []
        if "moneda_symbol" not in args:
            errors.append("El parámetro 'moneda_symbol' no se encuentra en la petición")
        else:
            moneda_symbol = args["moneda_symbol"]
            if not moneda_symbol:
                errors.append("No se ha ingresado/seleccionado la moneda del depósito")                 

        if "importe" not in args:
            errors.append("El parámetro 'importe' no se encuentra en la petición")
        else:
            importe = float(args["importe"])
            if importe <= 0:
                errors.append("El importe ingresados es menor o igual a 0")

        #validando la fecha de registro
        if "fec_deposito" not in args:
            errors.append("El parámetro 'fec_deposito' no se encuentra en la petición")
        else:
            #converting date client to date server
            fec_transaccion_parm = args["fec_deposito"]
            try:
                datetime.strptime(fec_transaccion_parm,CFG_GEN.CLIENT_DATE_FORMAT).date()                
            except ValueError as e:                
                errors.append("Error al convertir a date: {0}".format(str(e)))

        if len(errors) > 0:
            raise AppException(msg="Errores en la validación del depósito", errors=errors)

    def __collect(self, args={}):
        fund = TransaccionFondosModel()
        fund.fec_transaccion = datetime.strptime(args['fec_deposito'],CFG_GEN.CLIENT_DATE_FORMAT).date()        
        fund.tipo_trans_id = TIPO_TRANS_DEPOSITO
        fund.imp_transaccion = float(args["importe"])
        fund.mon_trans_id = args["moneda_symbol"]
        fund.fec_registro = datetime.now().date()
        fund.fec_audit = datetime.now()                                
        return fund

class Withdraw:
    def __init__(self):
        self.moneda_symbol = None
        self.importe = None
        self.saldo = None
        self.fec_transaccion = None        
        self.subtipo_transaccion = subtipo
        self.fec_audit = datetime.now()
        self.user_id = AuthManager().get_user_information()["user_id"]            

    def do(self, args={}):
        try:
            self.process(args)
            db.session.commit()  
            return Response(msg="Se ha retirado correctamente").get()        
        except Exception as e:            
            db.session.rollback()            
            return Response().from_exception(e)

    def process(self, args={}):
        self.__collect_args(args)
        self.__val_retiro()
        funds = self.__get_positive_banlance()
        #update balance
        self.__update_balance(funds=funds)

    def __update_balance(self, funds=[]):        
        for fund in funds:
            if self.saldo == 0:
                break

            self.__update_single_balance(fund=fund)


    def __update_single_balance(self, fund:TransaccionFondosModel=None):        
        #iniciar proceso de descuento
        #caso 1, si el importe del retiro es mayor al elemento a actualizar
        fund.saldo = float(fund.saldo)
        importe_retiro = 0
        if self.saldo > fund.saldo:
            importe_retiro = fund.saldo
            fund.saldo = 0            
            self.saldo = self.saldo - fund.saldo

        #caso 2, si el importe del retiro es = al elemento a actualizar
        if self.saldo == fund.saldo:
            importe_retiro = fund.saldo
            fund.saldo = 0
            self.saldo = 0

        #caso 3, si el importe del retiro es < al elemento a actualizar
        if self.saldo < fund.saldo:
            importe_retiro = self.saldo
            fund.saldo = fund.saldo - self.saldo
            self.saldo = 0

        #agregar una entrada para el retiro
        self.__create_withdraw_entry(fund, importe_retiro=importe_retiro)

    def __create_withdraw_entry(self, fund_balance:TransaccionFondosModel=None, importe_retiro=0):        

        retiro = TransaccionFondosModel(
            fec_transaccion = self.fec_transaccion,
            fec_registro = date.today(),    
            user_id = self.user_id,        
            fec_audit = self.fec_audit,
            est_transaccion_fondos_id = CONFIG.CONST_ESTADO_TRANS_FONDOS_REGISTRADO,            
            tipo_transaccion = CONFIG.CONST_TIPO_TRANSACCION_SALIDA,
            subtipo_transaccion = self.subtipo_transaccion,
            importe = importe_retiro,
            saldo = importe_retiro,
            concepto = "retiro",
            moneda_symbol = fund_balance.moneda_symbol,
            ref_transaccion_id = fund_balance.id
        )
        db.session.add(retiro)

    def __get_saldo_total(self):
        saldo_total = 0
        resp = db.session.query(
            func.sum(TransaccionFondosModel.saldo).label("saldo_total")
        ).filter(
            TransaccionFondosModel.tipo_transaccion == CONFIG.CONST_TIPO_TRANSACCION_INGRESO,
            TransaccionFondosModel.saldo > 0.00,
            TransaccionFondosModel.moneda_symbol == self.moneda_symbol
        ).first()

        if resp is not None:
            saldo_total = float(resp.saldo_total)

        return saldo_total

    def __get_positive_banlance(self):
        funds = TransaccionFondosModel.query.filter(
            TransaccionFondosModel.tipo_transaccion == CONFIG.CONST_TIPO_TRANSACCION_INGRESO,
            TransaccionFondosModel.saldo > 0.00,
            TransaccionFondosModel.moneda_symbol == self.moneda_symbol
        ).order_by(TransaccionFondosModel.fec_registro.asc(), TransaccionFondosModel.fec_audit.asc())\
        .all()

        return funds

    def __val_retiro(self):
        saldo_total = self.__get_saldo_total()
        if saldo_total == 0:
            raise AppException(msg="El saldo es 0")

        if self.importe > saldo_total:
            raise AppException(msg="El importe a retirar {0} es mayor al saldo total {1}".format(self.importe, saldo_total))

    def __collect_args(self, args={}):
        errors = []
        if "moneda_symbol" not in args:
            errors.append("El parámetro 'moneda_symbol' no se encuentra en la petición")
        else:
            moneda_symbol = args["moneda_symbol"]
            if not moneda_symbol:
                errors.append("No se ha ingresado/seleccionado la moneda del retiro")
            else:
                self.moneda_symbol = moneda_symbol      

        if "importe" not in args:
            errors.append("El parámetro 'importe' no se encuentra en la petición")
        else:
            importe = float(args["importe"])
            if importe <= 0:
                errors.append("El importe ingresados es menor o igual a 0")          
            else:
                self.importe = importe
                self.saldo = importe

        if "fec_retiro" not in args:
            errors.append("El parámetro 'fec_retiro' no se encuentra en la petición")
        else:
            #converting date client to date server
            fec_transaccion_parm = args["fec_retiro"]
            try:
                self.fec_transaccion = datetime.strptime(fec_transaccion_parm,CONFIG.CLIENT_DATE_FORMAT).date()                
            except Exception as e:
                print(type(e))
                errors.append("Error al convertir a date")

        if len(errors) > 0:
            raise AppException(msg="Errores en la validación del retiro", errors=errors)

        return self

class Conversion:
    def __init__(self):
        pass

    def convert(self, args={}):
        try:
            self.__val_convert(args)
            retiro_params, deposito_params, nu_conversion = self.__collect(args)

            #hacer los retiros en la moneda origen
            Withdraw(subtipo=CONFIG.CONST_SUBTIPO_TRANS_CONVERSION).process(retiro_params)

            #hacer el depósito en la moneda destino
            Deposit(subtipo=CONFIG.CONST_SUBTIPO_TRANS_CONVERSION).process(deposito_params)

            #registrar la conversion
            db.session.add(nu_conversion)

            db.session.commit()
            return Response(msg="Se ha realizado correctamente la conversion").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def __collect(self, args={}):
        
        #Realizar el retiro en la moneda origen
        withdraw_params = {
            "moneda_symbol":args["moneda_origen"],
            "importe":args["importe"],
            "fec_retiro":args["fec_cambio"]
        }        

        #calcular el importe post_conversion
        tipo_operacion = args["tipo_operacion"]
        if tipo_operacion == CONFIG.CONST_FX_TIPO_OPERACION_COMPRA:
            imp_post_conversion = float(args["importe"]) / float(args["importe_tc"])
        if tipo_operacion == CONFIG.CONST_FX_TIPO_OPERACION_VENTA:
            imp_post_conversion = float(args["importe"]) * float(args["importe_tc"])

        #Realizar el depósito en la moneda destino
        deposit_params = {
            "moneda_symbol":args["moneda_destino"],
            "importe":imp_post_conversion,
            "fec_deposito":args["fec_cambio"]
        }
                
        fec_transaccion = datetime.strptime(args["fec_cambio"], CONFIG.CLIENT_DATE_FORMAT).date()
        #creamos el objeto conversion
        nu_conversion = ConversionModel(
            id=None,
            fec_transaccion=fec_transaccion,            
            moneda_base_symbol=args["moneda_origen"],
            moneda_ref_symbol=args["moneda_destino"],
            importe_conversion=args["importe"],
            tipo_operacion=args["tipo_operacion"],
            importe_tc=args["importe_tc"],
            importe_post_conversion=imp_post_conversion,
            fec_registro=date.today(),
            fec_audit=datetime.now()
        )

        return (withdraw_params, deposit_params, nu_conversion)

    def __val_convert(self, args={}):
        errors = []
        if "conversion_id" not in args:
            errors.append("El parámetro 'conversion_id'  no ha sido enviado")

        if "fec_cambio" not in args:
            errors.append("El parámetro 'fec_cambio'  no ha sido enviado")
        else:
            if args["fec_cambio"] == "":
                errors.append("No se ha ingresado la 'fecha de cambio'")
            else:
                try:
                    datetime.strptime(args["fec_cambio"],CONFIG.CLIENT_DATE_FORMAT).date()                
                except ValueError as e:                
                    errors.append("Error al convertir a date: {0}".format(str(e)))

        if "tipo_operacion" not in args:
            errors.append("El parámetro 'tipo_operacion' no ha sido enviado")
        else:
            if args["tipo_operacion"] not in ["C","V"]:
                errors.append("El parámetro 'tipo_operacion' solo debe tener los valores 'C','V'")
        
        if "importe" not in args:
            errors.append("El parámetro 'importe' no ha sido enviado")

        if "importe_tc" not in args:
            errors.append("El parámetro 'importe_tc' no ha sido enviado")

        if "concepto" not in args:
            errors.append("El parámetro 'concepto' no ha sido enviado")

        if "moneda_origen" not in args:
            errors.append("El parámetro 'moneda_destino' no ha sido enviado")

        if "moneda_destino" not in args:
            errors.append("El parámetro 'moneda_destino' no ha sido enviado")

        if len(errors)>0:
            raise AppException(msg="Se han encontrado errores en el envío de la petición", errors=errors)





            







    




        