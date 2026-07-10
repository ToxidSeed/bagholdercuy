from config.extensions import db
from model.importacion import ImportacionModel

class ImportacionReader:
    def __init__(self):
        pass

    def get_importaciones(self, cod_origen, tipo_dataset):
        stmt = db.select(
            ImportacionModel
        ).where(
            ImportacionModel.cod_origen == cod_origen,
            ImportacionModel.tipo_dataset == tipo_dataset
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return records
        