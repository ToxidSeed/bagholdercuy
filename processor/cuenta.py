from model.cuenta import CuentaModel
from reader.cuenta import CuentaReader
from app import db

class CuentaProcessor:

    def guardar(self, cuenta:CuentaModel):
        if cuenta.id_cuenta is None:
            db.session.add(cuenta)        
        else:
            cuenta_a_actualizar = CuentaReader.get(cuenta.id_cuenta)
            cuenta_a_actualizar.nom_cuenta = cuenta.nom_cuenta
            cuenta_a_actualizar.usuario_id = cuenta.usuario_id
            cuenta_a_actualizar.flg_activo = cuenta.flg_activo
            