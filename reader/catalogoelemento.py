from app import db
from model.catalogoelemento import CatalogoElementoModel

class CatalogoElementoReader:

    def get_elementos(cod_catalogo):
        stmt = db.select(
            CatalogoElementoModel
        ).where(
            CatalogoElementoModel.cod_catalogo == cod_catalogo
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records

    def get_elemento(cod_catalogo, cod_elemento):

        stmt = db.select(
            CatalogoElementoModel
        ).where(
            CatalogoElementoModel.cod_catalogo == cod_catalogo,
            CatalogoElementoModel.cod_elemento == cod_elemento
        )

        result = db.session.execute(stmt)
        records = result.scalars().first()
        return records

