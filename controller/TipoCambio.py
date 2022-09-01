from common.Response import Response
from model.TipoCambio import TipoCambioModel
from model.MonedaParModel import MonedaParModel
from config.negocio import PAR_OPERACION_DIV
from datetime import date, datetime
from controller.base import Base

class TipoCambioFinder(Base):
    AUTH_REQUIRED = True

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
