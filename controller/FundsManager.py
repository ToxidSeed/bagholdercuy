from inspect import trace
import traceback, sys
from datetime import date, datetime
from app import app, db

from common.Response import Response
from common.AppException import AppException
import config as config

from sqlalchemy import func, true

from controller.AuthManager import AuthManager
from model.FundsHistory import FundsHistory
from model.CurrencyModel import MonedaModel

class FundsManager:
    TYPE_INCOME = 'I'
    TYPE_OUTCOME = 'O'

    def __init__(self):
        pass

    def get_funds(self, args={}):
        symbol = args["symbol"]

        funds = db.session.query(\
            FundsHistory.moneda_symbol,\
            func.sum(FundsHistory.saldo).label("importe")\
        ).filter(
            FundsHistory.moneda_symbol.ilike("%{0}%".format(symbol)),
            FundsHistory.tipo_transaccion == FundsManager.TYPE_INCOME,
            FundsHistory.saldo > 0.00
        ).group_by(FundsHistory.moneda_symbol).all()

        #import logging
        #logging.basicConfig()
        #logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        formats = {
            "importe":"{:0.2f}"
        }

        return Response().from_raw_data(funds, formats=formats)


class Deposit:
    def __init__(self):
        pass

    def do(self, args={}):
        try:
            new_deposit = self.__to_object(args)
            
            auth_info = AuthManager().get_user_information()

            new_deposit.user_id =  auth_info["user_id"]
            #new_deposit.fec_registro = date.today()
            new_deposit.estado_id = 0
            new_deposit.tipo_transaccion = FundsManager.TYPE_INCOME
            new_deposit.concepto = ""

            self.__check_moneda(new_deposit.moneda_symbol)

            db.session.add(new_deposit)
            db.session.commit()
            return Response(msg="Se ha depositado correctamente").get()
        except AppException as appe:
            db.session.rollback()
            return Response().from_exception(appe)
        except Exception as e:
            db.session.rollback()            
            return Response(success=False, msg="Error al realizar el deposito en la cuenta. detalles: {0}".format(e)).get()

    def __check_moneda(self, moneda_symbol=""):
        moneda_found = MonedaModel.query.filter(
            MonedaModel.symbol == moneda_symbol
        ).first()

        if moneda_found is None:
            raise AppException(msg="La moneda {0} no existe en la base de datos".format(moneda_symbol))

        return True

    def __to_object(self, args={}):
        fund = FundsHistory()
        fund.fec_audit = datetime.now()

        errors = []
        if "moneda_symbol" not in args:
            errors.append("El parámetro 'moneda_symbol' no se encuentra en la petición")
        else:
            moneda_symbol = args["moneda_symbol"]
            if not moneda_symbol:
                errors.append("No se ha ingresado/seleccionado la moneda del depósito")         
            fund.moneda_symbol = moneda_symbol    

        if "importe" not in args:
            errors.append("El parámetro 'importe' no se encuentra en la petición")

        importe = float(args["importe"])
        if importe <= 0:
            errors.append("El importe ingresados es menor o igual a 0")

        fund.importe = importe
        fund.saldo = importe

        #validando la fecha de registro
        if "fec_registro" not in args:
            errors.append("El parámetro 'fec_registro' no se encuentra en la petición")
        else:
            #converting date client to date server
            fec_registro_parm = args["fec_registro"]
            try:
                fund.fec_registro = datetime.strptime(fec_registro_parm,config.CLIENT_DATE_FORMAT).date()                
            except ValueError as e:                
                errors.append("Error al convertir a date: {0}".format(str(e)))

        if len(errors) > 0:
            raise AppException(msg="Errores en la validación del depósito", errors=errors)

        return fund

class Withdraw:
    def __init__(self):
        self.moneda_symbol = None
        self.importe = None
        self.saldo = None
        self.fec_registro = None
        self.fec_audit = datetime.now()
        self.user_id = AuthManager().get_user_information()["user_id"]            

    def do(self, args={}):
        try:
            self.__collect_args(args)

            funds = self.__get_positive_banlance()
            #update balance
            self.__update_balance(funds=funds)
            db.session.commit()  
            return Response(msg="Se ha retirado correctamente").get()
        except AppException as appe:
            db.session.rollback()
            return Response().from_exception(appe)
        except Exception as e:            
            db.session.rollback()            
            return Response().from_exception(e)

    def __update_balance(self, funds=[]):        
        for fund in funds:
            if self.saldo == 0:
                break

            self.__update_single_balance(fund=fund)


    def __update_single_balance(self, fund:FundsHistory=None):        
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

    def __create_withdraw_entry(self, fund_balance:FundsHistory=None, importe_retiro=0):
        retiro = FundsHistory(
            fec_registro = self.fec_registro,    
            user_id = self.user_id,        
            fec_audit = self.fec_audit,
            estado_id = 0,
            tipo_transaccion = FundsManager.TYPE_OUTCOME,
            importe = importe_retiro,
            saldo = importe_retiro,
            concepto = "retiro",
            moneda_symbol = fund_balance.moneda_symbol,
            referencia_id = fund_balance.id
        )
        db.session.add(retiro)

    def __get_positive_banlance(self):
        funds = FundsHistory.query.filter(
            FundsHistory.tipo_transaccion == FundsManager.TYPE_INCOME,
            FundsHistory.saldo > 0.00
        ).order_by(FundsHistory.fec_registro.asc(), FundsHistory.fec_audit.asc())\
        .all()

        return funds


    def __collect_args(self, args={}):
        errors = []
        if "moneda_symbol" not in args:
            errors.append("El parámetro 'moneda_symbol' no se encuentra en la petición")
        else:
            moneda_symbol = args["moneda_symbol"]
            if not moneda_symbol:
                errors.append("No se ha ingresado/seleccionado la moneda del depósito")
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

        if "fec_registro" not in args:
            errors.append("El parámetro 'fec_registro' no se encuentra en la petición")
        else:
            #converting date client to date server
            fec_registro_parm = args["fec_registro"]
            try:
                self.fec_registro = datetime.strptime(fec_registro_parm,config.CLIENT_DATE_FORMAT).date()                
            except Exception as e:
                print(type(e))
                errors.append("Error al convertir a date")

        if len(errors) > 0:
            raise AppException(msg="Errores en la validación del retiro", errors=errors)

        return self






            







    




        