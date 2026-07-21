from model.ibkr_operacion_importada import IbkrOperacionImportadaModel

from config.extensions import db


class IbkrOperacionImportadaReader:

    @staticmethod
    def get(id_operacion_importada):
        query = db.select(
            IbkrOperacionImportadaModel
        ).where(
            IbkrOperacionImportadaModel.id_operacion_importada == id_operacion_importada
        )

        result = db.session.execute(query)
        return result.scalars().first()

    @staticmethod
    def get_por_importacion(id_importacion, cod_symbol=None):
        query = db.select(
            IbkrOperacionImportadaModel
        ).where(
            IbkrOperacionImportadaModel.id_importacion == id_importacion
        )

        if cod_symbol:
            query = query.where(
                IbkrOperacionImportadaModel.cod_symbol == cod_symbol
            )
        
        query = query.order_by(
            IbkrOperacionImportadaModel.fch_hora_operacion.asc()
        )

        result = db.session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_por_ids(ids_operaciones_importadas):
        query = db.select(
            IbkrOperacionImportadaModel
        ).where(
            IbkrOperacionImportadaModel.id_operacion_importada.in_(ids_operaciones_importadas)
        ).order_by(
            IbkrOperacionImportadaModel.fch_hora_operacion.asc()
        )

        result = db.session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_pendientes(id_importacion=None):
        query = db.select(
            IbkrOperacionImportadaModel
        ).where(
            IbkrOperacionImportadaModel.procesado == False
        )

        if id_importacion is not None:
            query = query.where(
                IbkrOperacionImportadaModel.id_importacion == id_importacion
            )

        query = query.order_by(
            IbkrOperacionImportadaModel.fch_hora_operacion.asc()
        )

        result = db.session.execute(query)
        return result.scalars().all()
