from common.Response import Response
from common.AppException import AppException
from model.tipocambio import TipoCambioModel
from model.MonedaParModel import MonedaParModel
from processor.tipocambio import TipoCambioWriter

from config.app_constants import PAR_OPERACION_DIV
from config.general import CLIENT_DATE_FORMAT
from datetime import date, datetime
from controller.base import Base

from app import db

class TipoCambioFinder(Base):    

    def get_tc(self, args={}):
        try:
            if "fch_cambio" not in args:
                raise AppException("No se ha enviado 'fch_cambio'")
            if "mon_base_id" not in args:
                raise AppException("No se ha enviado 'mon_base_id'")
            if "mon_ref_id" not in args:
                raise AppException("No se ha enviado 'mon_ref_id'")

            mon_base_id = args["mon_base_id"]
            if mon_base_id == "":
                raise AppException("mon_base_id es nulo o vacío")

            mon_ref_id = args["mon_ref_id"]
            if mon_ref_id == "":
                raise AppException("mon_ref_id es nulo o vacío")

            fch_cambio = datetime.strptime(args["fch_cambio"],"%d/%m/%Y").date() 

            par = MonedaParModel.query.filter(
                MonedaParModel.mon_base_id == mon_base_id,
                MonedaParModel.mon_ref_id == mon_ref_id
            ).first()

            if par is None:
                raise AppException("No se ha encontrado la configuración para el par {0}/{1}".format(mon_base_id, mon_ref_id))

            tc = None
            msg = ""
            tipo=""
            par_usado = ""

            if par.operacion == PAR_OPERACION_DIV:
                par_usado = "{0}/{1}".format(mon_ref_id,mon_base_id)
                tc = TipoCambioModel.query.filter(
                    TipoCambioModel.fch_cambio == fch_cambio,
                    TipoCambioModel.mon_ref_id == mon_base_id,
                    TipoCambioModel.mon_base_id == mon_ref_id
                ).first()
                if tc is None:
                    msg = "El par está configurado como una operación de división por lo tanto se usa el par inverso, sin embargo no se ha encontrado el tipo de cambio para {0}/{1} y la fecha {2}".format(mon_ref_id, mon_base_id, fch_cambio)
                    tipo = "error"
                else:
                    msg = "El par está configurado como una operación de división por lo tanto se usa el par inverso {0}/{1}".format(mon_ref_id, mon_base_id)
                    tipo = "warning"
            else:                
                par_usado = "{0}/{1}".format(mon_base_id,mon_ref_id)
                tc = TipoCambioModel.query.filter(
                    TipoCambioModel.fch_cambio == fch_cambio,
                    TipoCambioModel.mon_base_id == mon_base_id,
                    TipoCambioModel.mon_ref_id == mon_ref_id
                ).first()
                if tc is None:
                    msg ="No se ha encontrado el tipo de cambio para {0}/{1} y la fecha {2}".format(mon_base_id, mon_ref_id, fch_cambio)
                    tipo = "error"            
            
            extradata = {
                "msg":{
                    "type":tipo,
                    "text":msg
                },
                "par_usado":par_usado,
                "operacion":par.operacion
            }
            return Response(extradata=extradata).from_raw_data(tc)  
        except Exception as e:
            return Response().from_exception(e)

class TipoCambioNuevoController(Base):
    def procesar(self, args={}):
        try:
            self.validar(args)
            tc_nuevo = self._collect(args)
            fch_cambio = args.get('fch_cambio')
            TipoCambioWriter().registrar(tc_nuevo)
            db.session.commit()            
            return Response(msg="Se ha procesado el registro del tipo de cambio para la fecha {0}".format(fch_cambio))
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)
              


    def validar(self, args={}):
        fch_cambio = args.get('fch_cambio')
        if fch_cambio is None:
            raise AppException(msg="No se ha enviado la fecha del tipo de cambio")

        par_id = args.get('par_id')
        if par_id is None:
            raise AppException(msg="No se ha enviado 'par_id'")

        if par_id in ["",0]:
            raise AppException(msg="No se ha indicado el par del tipo de cambio")

        imp_compra = args.get('imp_compra')
        if imp_compra is None:
            raise AppException(msg="No se ha enviado imp_compra")

        if imp_compra in ["",0]:
            raise AppException(msg="No se ha ingresado el importe de compra")

        imp_venta = args.get('imp_venta')
        if imp_venta is None:
            raise AppException(msg="No se ha enviado imp_venta")

        if imp_venta in ["",0]:
            raise AppException(msg="No se ha ingresado imp_venta")
        

    def _collect(self, args={}):
        fch_cambio = args.get('fch_cambio')
        fch_cambio = datetime.strptime(fch_cambio, CLIENT_DATE_FORMAT).date()
        par_id = args.get('par_id')                        

        imp_compra = float(args.get('imp_compra'))
        imp_venta = float(args.get('imp_venta'))
        fch_registro = date.today()
        fch_audit = datetime.now()

        tc_nuevo = TipoCambioModel(
            fch_cambio = fch_cambio,            
            par_id = par_id,            
            imp_compra = imp_compra,
            imp_venta = imp_venta,
            fch_registro = fch_registro,
            fch_audit = fch_audit
        )

        return tc_nuevo
