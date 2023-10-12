from model.cuenta import CuentaModel
from app import db

class CuentaReader:

    def get(id_cuenta):
        stmt = db.select(
            CuentaModel
        ).where(
            CuentaModel.id_cuenta == id_cuenta
        )

        result = db.session.execute(stmt)
        return result.scalars().one()

    def get_cuentas(args={}):

        stmt = db.select(
            CuentaModel
        )

        id_usuario = args.get("id_usuario")
        if id_usuario is not None:
            stmt = stmt.where(
                CuentaModel.usuario_id == id_usuario
            )
        
        text = args.get("text")
        if text not in [None, ""]:
            stmt = stmt.where(
                CuentaModel.nom_cuenta.ilike("%{0}%".format(text))
            )

        result = db.session.execute(stmt)
        return result.scalars().all()