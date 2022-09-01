from inspect import trace
import traceback, sys
from datetime import date, datetime
from app import app, db

from common.Response import Response
from common.AppException import AppException
from sqlalchemy import func, true, and_
from controller.base import Base

from controller.AuthManager import AuthManager
#from model.ConversionModel import ConversionModel
#from model.FundsHistory import FundsHistory
from model.TransaccionFondosModel import TransaccionFondosModel
from model.MovimientoFondosModel import MovimientoFondosModel
from model.CurrencyModel import CurrencyModel
from model.MovimientoFondosModel import MovimientoFondosModel

from config.negocio import TIPO_MOV_INGRESO,TIPO_TRANS_DEPOSITO, TIPO_TRANS_RETIRO, TIPO_TRANS_CONVERSION
from config.general import CLIENT_DATE_FORMAT

from model.bussiness.deposito_handler import DepositoHandler
from model.bussiness.retiro import RetiroHandler
from model.bussiness.conversion_moneda import ConversionMonedaHandler

class FundsManager(Base):
    AUTH_REQUIRED = True    

    def get_funds(self, args={}):
        symbol = args["symbol"]

        funds = db.session.query(\
            MovimientoFondosModel.mon_mov_id.label("moneda"),\
            func.sum(MovimientoFondosModel.imp_saldo_mov).label("importe")\
        ).filter(
            MovimientoFondosModel.mon_mov_id.ilike("%{0}%".format(symbol)),
            MovimientoFondosModel.tipo_mov_id == TIPO_MOV_INGRESO,
            MovimientoFondosModel.imp_saldo_mov > 0.00
        ).group_by(MovimientoFondosModel.mon_mov_id).all()

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

class DepositResource(Base):    
    AUTH_REQUIRED = True

    def add(self, args={}):
        try:
            self.val_add(args)
            new_deposit = self.__collect(args)                        
            DepositoHandler(self.usuario).add(new_deposit)
            db.session.commit()
            extradata = {
                "trans_id":new_deposit.id
            }
            return Response(msg="Se ha depositado correctamente {0} {1}".format(new_deposit.mon_trans_id,new_deposit.imp_transaccion),
            extradata=extradata).get()
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
                datetime.strptime(fec_transaccion_parm,CLIENT_DATE_FORMAT).date()                
            except ValueError as e:                
                errors.append("Error al convertir a date: {0}".format(str(e)))

        if len(errors) > 0:
            raise AppException(msg="Errores en la validación del depósito", errors=errors)

    def __collect(self, args={}):
        fund = TransaccionFondosModel()
        fund.fec_transaccion = datetime.strptime(args['fec_deposito'],CLIENT_DATE_FORMAT).date()        
        fund.tipo_trans_id = TIPO_TRANS_DEPOSITO
        fund.imp_transaccion = float(args["importe"])
        fund.mon_trans_id = args["moneda_symbol"]
        fund.fec_registro = datetime.now().date()
        fund.usuario_id = self.usuario.id
        fund.fec_audit = datetime.now()                                
        return fund

class WithdrawResource(Base):
    AUTH_REQUIRED = True

    def retirar(self, args={}):
        try:
            #self.process(args)
            self._val_retirar(args)
            retiro = self._collect_retirar(args)
            retiro.usuario_id = self.usuario.id
            RetiroHandler().retirar(retiro)
            db.session.commit()  
            return Response(msg="Se ha retirado correctamente").get()        
        except Exception as e:            
            db.session.rollback()            
            return Response().from_exception(e)

    def _val_retirar(self, args={}):
        errors = []
        if "moneda_symbol" not in args:
            errors.append("El parámetro 'moneda_symbol' no se encuentra en la petición")
        else:
            moneda_symbol = args["moneda_symbol"]
            if not moneda_symbol:
                errors.append("No se ha ingresado/seleccionado la moneda del retiro")            

        if "importe" not in args:
            errors.append("El parámetro 'importe' no se encuentra en la petición")
        else:
            importe = float(args["importe"])
            if importe <= 0:
                errors.append("El importe ingresados es menor o igual a 0")                      

        if "fec_retiro" not in args:
            errors.append("El parámetro 'fec_retiro' no se encuentra en la petición")
        else:
            #converting date client to date server            
            try:
                datetime.strptime(args["fec_retiro"],CLIENT_DATE_FORMAT).date()                
            except Exception as e:
                print(type(e))
                errors.append("Error al convertir a date")

        if len(errors) > 0:
            raise AppException(msg="Errores en la validación del retiro", errors=errors)
        

    def _collect_retirar(self, args={}):
        retiro = TransaccionFondosModel()
        retiro.mon_trans_id = args["moneda_symbol"]
        retiro.imp_transaccion = float(args["importe"])
        retiro.fec_transaccion = datetime.strptime(args["fec_retiro"],CLIENT_DATE_FORMAT).date()
        retiro.tipo_trans_id = TIPO_TRANS_RETIRO
        retiro.fec_registro = datetime.now().date()
        retiro.fec_audit = datetime.now()
        return retiro


    def process(self, args={}):
        self.__collect_args(args)
        self.__val_retiro()
        funds = self.__get_positive_banlance()
        #update balance
        self.__update_balance(funds=funds)

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

class Conversion(Base):    

    def convert(self, args={}):
        try:
            self.__val_convert(args)
            nu_conversion = self.__collect(args)
            ConversionMonedaHandler().convertir(nu_conversion)            
            db.session.commit()
            return Response(msg="Se ha realizado correctamente la conversion").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def __collect(self, args={}):
        
        fec_transaccion = datetime.strptime(args["fch_cambio"],CLIENT_DATE_FORMAT).date()
        operacion = args["operacion"]
        imp_tc = float(args["importe_tc"])
        imp_trans = float(args["importe"])
        mon_base_id = args.get('mon_base_id')
        mon_ref_id = args.get('mon_ref_id')

        if operacion == "MUL":
            imp_convertido = round(imp_trans * imp_tc,2)
        else:
            imp_convertido = round(imp_trans / imp_tc,2)

        info_adicional = "fch_conver:{0}, tc:{1}, oper:{2}, origen:{3} {4}, destino:{5} {6}".format(fec_transaccion,imp_tc,operacion,imp_trans,mon_base_id, imp_convertido,mon_ref_id)

        #creamos el objeto conversion
        nu_conversion = TransaccionFondosModel(
            id=None,
            fec_transaccion=fec_transaccion,   
            tipo_trans_id=TIPO_TRANS_CONVERSION,         
            imp_transaccion=imp_trans,
            mon_trans_id=args.get("mon_base_id"),            
            operacion_id = operacion,                        
            fec_registro=date.today(),
            fec_audit=datetime.now(),
            info_adicional=info_adicional
        )

        return nu_conversion

    def __val_convert(self, args={}):
        errors = []        

        if "fch_cambio" not in args:
            errors.append("El parámetro 'fch_cambio'  no ha sido enviado")
        else:
            if args["fch_cambio"] == "":
                errors.append("No se ha ingresado la 'fecha de cambio'")
            else:
                try:
                    datetime.strptime(args["fch_cambio"],CLIENT_DATE_FORMAT).date()                
                except ValueError as e:                
                    errors.append("Error al convertir a date: {0}".format(str(e)))
        
        if "importe" not in args:
            errors.append("El parámetro 'importe' no ha sido enviado")

        importe = args["importe"]
        if importe == "":
            errors.append("No se ha informado una cantidad válida para el importe a convertir")

        if "importe_tc" not in args:
            errors.append("El parámetro 'importe_tc' no ha sido enviado")        

        if "mon_base_id" not in args:
            errors.append("El parámetro 'mon_base_id' no ha sido enviado")

        if "mon_ref_id" not in args:
            errors.append("El parámetro 'mon_ref_id' no ha sido enviado")

        if "operacion" not in args:
            errors.append("El parámetro 'operacion' no ha sido enviado")

        if len(errors)>0:
            raise AppException(msg="Se han encontrado errores en el envío de la petición", errors=errors)





            







    




        