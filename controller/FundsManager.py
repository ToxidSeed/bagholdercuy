from inspect import trace
import traceback, sys
from datetime import date, datetime
from app import app, db

from common.Response import Response
from common.AppException import AppException
from sqlalchemy import func, true, and_
from controller.base import Base
from controller.AuthManager import AuthManager

from model.TransaccionFondosModel import TransaccionFondosModel
from model.MovimientoFondosModel import MovimientoFondosModel
from model.CurrencyModel import CurrencyModel
from model.MovimientoFondosModel import MovimientoFondosModel
from model.conversionmoneda import ConversionMonedaModel

from config.negocio import TIPO_MOV_INGRESO,TIPO_TRANS_DEPOSITO, TIPO_TRANS_RETIRO, TIPO_TRANS_CONVERSION, REPROCESO_PROF_FONDOS_TODO,REPROCESO_PROF_FONDOS_FCH_CIERRE
from config.general import CLIENT_DATE_FORMAT

from model.bussiness.transaccion import TransaccionHandler, DepositoHandler, ReprocesadorFondosHandler,RetiroHandler, ConversionMonedaHandler

class FundsManager(Base):    
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

    def get_transacciones_x_fecha(self, args={}):
        fch_transaccion = args["fch_transaccion"]
        if fch_transaccion is None or fch_transaccion =="":
            raise AppException(msg="No se ha enviado la fecha de transacción") 
        
        fch_transaccion = datetime.strptime(fch_transaccion, CLIENT_DATE_FORMAT)

        results = db.session.query(
            TransaccionFondosModel
        ).filter(
            TransaccionFondosModel.fch_transaccion == fch_transaccion,
            TransaccionFondosModel.usuario_id == self.usuario.id
        ).all()

        return Response().from_raw_data(results)

    def get_count_transacciones(self, args={}):
        fch_desde = args.get("fch_desde")
        fch_hasta = args.get("fch_hasta")

        query = db.session.query(
            TransaccionFondosModel.usuario_id,
            TransaccionFondosModel.fch_transaccion,
            func.count(1).label("num_transacciones")
        ).filter(
            TransaccionFondosModel.usuario_id  == self.usuario.id
        )

        if fch_desde is not None and fch_desde != "":
            fch_desde = datetime.strptime(fch_desde,CLIENT_DATE_FORMAT).date()
            query = query.filter(
                TransaccionFondosModel.fch_transaccion >= fch_desde 
            )
        if fch_hasta is not None and fch_hasta != "":
            fch_hasta = datetime.strptime(fch_hasta,CLIENT_DATE_FORMAT).date()
            query = query.filter(
                TransaccionFondosModel.fch_transaccion <= fch_hasta 
            )
        
        results = query.group_by(
            TransaccionFondosModel.usuario_id,
            TransaccionFondosModel.fch_transaccion
        ).order_by(
            TransaccionFondosModel.fch_transaccion.desc()
        ).all()

        return Response().from_raw_data(results)
      

    def ult_transaccion(self, args={}):
        response = Response()

        fch_transaccion = args.get("fch_transaccion")
        if fch_transaccion is None or fch_transaccion == "":
            raise AppException(msg="No se ha indicado la fecha de transacción")
        else:
            fch_transaccion = datetime.strptime(fch_transaccion, CLIENT_DATE_FORMAT).date()
        
        if TransaccionHandler.ult_transaccion(self.usuario.id, fch_transaccion) is True:            
            response.elem("ult_transaccion",True)
        else:
            response.message("Existen transacciones posteriores a la fecha {0}, se van a reprocesar todas las transacciones".format(fch_transaccion))
            response.elem("ult_transaccion",False)

        return response

class Historial(Base):    
    def get(self, args={}):        
        funds = db.session.query(
            TransaccionFondosModel
        ).filter(
            TransaccionFondosModel.usuario_id == self.usuario.id
        ).order_by(TransaccionFondosModel.fch_transaccion.desc(), TransaccionFondosModel.num_transaccion.desc())\
        .all()

        return Response().from_raw_data(funds)   

class ReprocesarController(Base):    
    def procesar(self, args={}):
        try:            
            self._validar(args)        
            (fch_desde, tipo_reproceso) = self._collect(args)
            ReprocesadorFondosHandler(self.usuario, fch_desde,tipo_reproceso).procesar()            
            db.session.commit()
            return Response(msg="Se ha reprocesado correctamente")
        except Exception as e:
            return Response().from_exception(e)
            db.session.rollback()

    def _validar(self, args={}):
        fch_desde = args.get("fch_desde")
        tipo_reproceso = args.get("tipo_reproceso")        

        if tipo_reproceso not in [REPROCESO_PROF_FONDOS_FCH_CIERRE,REPROCESO_PROF_FONDOS_TODO]:
            raise AppException(msg="No se ha seleccionado el tipo de proceso")

        if tipo_reproceso == REPROCESO_PROF_FONDOS_FCH_CIERRE:
            if fch_desde is None or fch_desde=="":
                raise AppException(msg="No se ha enviado el parámetro fch_desde")
            else:
                fch_desde = datetime.strptime(fch_desde,CLIENT_DATE_FORMAT).date()                                    

    def _collect(self, args={}):
        tipo_reproceso = args.get("reprocesar_todo")
        fch_desde = args.get("fch_desde")

        if tipo_reproceso == REPROCESO_PROF_FONDOS_FCH_CIERRE:
            fch_desde = datetime.strptime(fch_desde,CLIENT_DATE_FORMAT).date()
        
        return (fch_desde, tipo_reproceso)

class DepositResource(Base):        
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
        fund.fch_transaccion = datetime.strptime(args['fec_deposito'],CLIENT_DATE_FORMAT).date()        
        fund.tipo_trans_id = TIPO_TRANS_DEPOSITO
        fund.imp_transaccion = float(args["importe"])
        fund.mon_trans_id = args["moneda_symbol"]
        fund.fch_registro = datetime.now().date()
        fund.usuario_id = self.usuario.id
        fund.fch_audit = datetime.now()                                
        return fund

class WithdrawResource(Base):        
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
        retiro.fch_transaccion = datetime.strptime(args["fec_retiro"],CLIENT_DATE_FORMAT).date()
        retiro.tipo_trans_id = TIPO_TRANS_RETIRO
        retiro.fch_registro = datetime.now().date()
        retiro.fch_audit = datetime.now()
        retiro.usuario_id = self.usuario.id
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
            ConversionMonedaHandler().procesar(nu_conversion)            
            db.session.commit()
            return Response(msg="Se ha realizado correctamente la conversion").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def __collect(self, args={}):        
        fch_transaccion = datetime.strptime(args.get("fch_cambio"),CLIENT_DATE_FORMAT).date()
        fch_registro = date.today()
        operacion = args.get("operacion")
        imp_tc = float(args.get("importe_tc"))
        imp_trans = float(args.get("importe"))
        mon_base_id = args.get('mon_base_id')
        mon_ref_id = args.get('mon_ref_id')

        if operacion == "MUL":
            imp_convertido = round(imp_trans * imp_tc,2)
        else:
            imp_convertido = round(imp_trans / imp_tc,2)

        #info_adicional = "fch_conver:{0}, tc:{1}, oper:{2}, origen:{3} {4}, destino:{5} {6}".format(fec_transaccion,imp_tc,operacion,imp_trans,mon_base_id, imp_convertido,mon_ref_id)

        #creamos el objeto conversion
        nu_conversion = ConversionMonedaModel(
            id=None,
            fch_conversion=fch_transaccion,
            mon_ori_id = mon_base_id,
            mon_dest_id = mon_ref_id,
            imp_tc = imp_tc,
            operacion_id = operacion,
            imp_origen = imp_trans,
            imp_convertido = imp_convertido,
            fch_registro = fch_registro,
            usuario_id = self.usuario.id,
            fch_audit=datetime.now()
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





            







    




        