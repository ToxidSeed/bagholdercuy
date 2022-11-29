from app import db
#from model.CurrencyPairModel import CurrencyPairModel
from model.MonedaParModel import MonedaParModel
from common.Response import Response
from config.negocio import IND_INACTIVO, PAR_OPERACION_DIV
from controller.base import Base 

class CurrencyPairManager:
    def __init__(self):
        pass

class ParFinder(Base):    

    def get_list_by_text(self, args={}):
        text = args["search_text"]
        pairs = MonedaParModel.query.filter(
            MonedaParModel.nombre.ilike("%{0}%".format(text))
        ).all()

        return Response().from_raw_data(pairs)

    def get_par_info(self, args={}):
        if "mon_base_id" not in args:
            raise AppException(msg="El parámetro 'mon_base_id' no ha sido enviado")
        if "mon_ref_id" not in args:
            raise AppException(msg="El parámetro 'mon_ref_id' no ha sido enviado")

        mon_base_id = args["mon_base_id"]
        mon_ref_id = args["mon_ref_id"]
        
        par = MonedaParModel.query.filter(
            MonedaParModel.mon_base_id == mon_base_id,
            MonedaParModel.mon_ref_id == mon_ref_id
        ).first()

        par_param = "{0}/{1}".format(mon_base_id, mon_ref_id)

        par_ind_activo = ""
        if par is None:
            raise AppException(msg="No existe información para el par {0}".format(par_param))
        else:
            par_ind_activo = par.ind_activo

        if par_ind_activo == IND_INACTIVO:
            raise AppException(msg="El par {0} se encuentra inactivo".format(par_param))

        msg = ""
        if par.operacion == PAR_OPERACION_DIV:
            par_inverso = "{0}/{1}".format(mon_ref_id,mon_base_id)

            msg = "El par {0} tiene como operación {1}, por lo que el tipo de cambio se deberá obtener el tipo de cambio del par inverso {2}".format(par_param, par.operacion, par_inverso)
        
        return Response(msg=msg).from_raw_data(par)

        


