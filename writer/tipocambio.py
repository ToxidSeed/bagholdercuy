from model.tipocambio import TipoCambioModel
from common.AppException import AppException
from app import db
from settings import config

class TipoCambioWriter:     

    def registrar(self, tc_nuevo):
        par = TipoCambioModel.get_par(tc_nuevo.par_id)
        if par is None:
            raise AppException(msg="el par_id {0} no existe".format(tc_nuevo.par_id))
        
        tc_nuevo.mon_base_id = par.mon_base_id
        tc_nuevo.mon_ref_id = par.mon_ref_id
        tc_nuevo.par_nombre = par.nombre

        estados = config['tipo_cambio.estados']
        tc_nuevo.ind_activo = estados.get('activo')

        if self.existe_tc(tc_nuevo) == True:
            raise AppException(msg="Ya existe T/C para la fecha {0} y {1}/{2}".format(tc_nuevo.fch_cambio, tc_nuevo.mon_base_id, tc_nuevo.mon_ref_id))

        db.session.add(tc_nuevo)        

    def existe_tc(self,tc_nuevo):
        tc = TipoCambioModel.get(
            tc_nuevo.fch_cambio,
            tc_nuevo.mon_base_id,
            tc_nuevo.mon_ref_id
        )

        return False if tc is None else True


