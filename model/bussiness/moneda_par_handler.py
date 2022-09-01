from model.MonedaParModel import MonedaParModel
from model.MonedaModel import MonedaModel
from app import db
from common.AppException import AppException
from datetime import datetime, date

class MonedaParHandler:
    def __init__(self):
        pass

    def add(self, par:MonedaParModel):
        self._val_add(par)
        par.ind_activo = 'S'
        par.fch_registro = date.today()
        par.fch_audit = datetime.now()
        db.session.add(par)

    def _val_add(self, par:MonedaParModel):
        mon_ref = self._get_moneda(par.mon_ref_id)
        if mon_ref is None:
            errors.append("La moneda de referencia {0} no existe en la base de datos".format(par.mon_ref_id))

        par_encontrado = self._get_par(par)
        if par_encontrado is not None and par_encontrado.ind_activo == 'S':
            raise AppException(msg="El par {0} ya se encuentra registrado y activo".format(par.nombre))

    def _get_par(self, in_par:MonedaParModel):
        par_encontrado = db.session.query(
            MonedaParModel
        ).filter(
            MonedaParModel.mon_base_id == in_par.mon_base_id,
            MonedaParModel.mon_ref_id == in_par.mon_ref_id
        ).first()
        return par_encontrado
    
    def _get_moneda(self, moneda_id):
        moneda = MonedaModel.query.filter_by(
            moneda_id = moneda_id
        ).first()
        return moneda

