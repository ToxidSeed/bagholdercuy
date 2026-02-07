from model.operacion import OperacionModel
from model.StockSymbol import StockSymbol as StockSymbolModel
from model.OptionContract import OptionContractModel

from app import db
from sqlalchemy.sql.functions import func

class OperacionReader:

    def get_max_num_orden(id_cuenta, fch_operacion, id_symbol, id_contrato_opcion=None):
        query = db.select(
            func.max(OperacionModel.num_orden_operacion).label('num_orden_operacion')
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.fch_operacion == fch_operacion,
            OperacionModel.id_symbol == id_symbol,
            OperacionModel.id_contrato_opcion == id_contrato_opcion
        )

        result = db.session.execute(query)
        record = result.first()

        if record is None:
            return 0
        
        if record.num_orden_operacion is None:
            return 0
        
        return record.num_orden_operacion

    @staticmethod
    def get(id_operacion):
        query = db.select(
            OperacionModel
        ).where(
            OperacionModel.id_operacion == id_operacion
        )

        result = db.session.execute(query)
        record = result.scalars().first()
        return record
        
    def get_operacion_key_2(self, id_cuenta, id_symbol, id_contrato_opcion, fch_operacion, num_operacion):
        query = db.select(
            OperacionModel
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.fch_operacion == fch_operacion,
            OperacionModel.id_symbol == id_symbol,
            OperacionModel.id_contrato_opcion == id_contrato_opcion,
            OperacionModel.num_orden_operacion == num_operacion
        )

        result = db.session.execute(query)
        return result.scalars().first()
    
    def get_ultima_operacion_x_fecha(self, id_cuenta, id_symbol, id_contrato_opcion, fch_operacion):
        max_num_operacion = self.get_max_num_operacion(id_cuenta, id_symbol, id_contrato_opcion, fch_operacion)
        operacion = self.get_operacion_key_2(id_cuenta, id_symbol, id_contrato_opcion, fch_operacion, max_num_operacion)
        return operacion
    
    def get_ultima_operacion_hasta_fecha(self, id_cuenta, id_symbol, id_contrato_opcion, fch_operacion, incluir_fecha=True):
        query = db.select(
            func.max(OperacionModel.fch_operacion).label("fch_operacion"),
            func.max(OperacionModel.num_operacion).label("num_operacion")
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.id_symbol == id_symbol,
            OperacionModel.id_contrato_opcion == id_contrato_opcion
        )

        if incluir_fecha is True:
            query = query.where(
                OperacionModel.fch_operacion <= fch_operacion
            )
        else:
            query = query.where(
                OperacionModel.fch_operacion < fch_operacion
            )

        result = db.session.execute(query)
        record_aux = result.first()
        if record_aux is None:
            return None

        operacion = self.get_operacion_key_2(id_cuenta, id_symbol, id_contrato_opcion, record_aux.fch_operacion, record_aux.num_operacion)
        return operacion    
    
    def get_max_num_operacion(self, id_cuenta, id_symbol, id_contrato_opcion, fch_operacion):
        query = db.select(
            func.max(OperacionModel.num_operacion).label("max_num_operacion")
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.fch_operacion == fch_operacion,
            OperacionModel.id_symbol == id_symbol,
            OperacionModel.id_contrato_opcion == id_contrato_opcion,
        )

        result = db.session.execute(query)                
        record = result.scalars().first()
        if record is None:
            return None
        
        if record.max_num_operacion is None:
            return None
        
        return record.max_num_operacion

    def get_ultima_fecha_operacion(id_cuenta, id_symbol, id_contrato_opcion):
        query = db.select(
            func.max(OperacionModel.fch_operacion).label("fch_operacion")
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.id_symbol == id_symbol,
            OperacionModel.id_contrato_opcion == id_contrato_opcion
        )

        result = db.session.execute(query)
        record = result.first()

        if record is None:
            return None
        
        if record.fch_operacion is None:
            return None
        
        return record.fch_operacion

    def get_operaciones(id_cuenta, id_symbol=None, flg_opciones=False, id_contrato_opcion=None, orden_resultados="asc"):

        query = db.select(
            OperacionModel.id_operacion,
            OperacionModel.id_cuenta,
            OperacionModel.fch_operacion,
            OperacionModel.num_orden,
            OperacionModel.id_tipo_operacion,
            OperacionModel.id_symbol,
            OperacionModel.id_contrato_opcion,
            OperacionModel.cantidad,
            OperacionModel.ctd_posicion,
            OperacionModel.dsc_glosa_operacion,
            OperacionModel.fch_registro,
            StockSymbolModel.symbol.label("cod_symbol"),
            OptionContractModel.symbol.label("cod_contrato_opcion")
        ).select_from(
            OperacionModel
        ).join(
            StockSymbolModel, OperacionModel.id_symbol == StockSymbolModel.id
        ).outerjoin(
            OptionContractModel, OperacionModel.id_contrato_opcion == OptionContractModel.id
        ).where(
            OperacionModel.id_cuenta == id_cuenta
        )

        if id_symbol is not None:
            query = query.where(
                OperacionModel.id_symbol == id_symbol
            )

        if flg_opciones is False:
            query = query.where(
                OperacionModel.id_contrato_opcion == None
            )

        if flg_opciones is True and id_contrato_opcion is not None:
            query = query.where(
                OperacionModel.id_contrato_opcion == id_contrato_opcion
            )                  

        if orden_resultados == "asc":
            query = query.order_by(
                OperacionModel.id_cuenta,
                OperacionModel.fch_operacion.asc(),
                OperacionModel.num_orden.asc()
            )
        if orden_resultados == "desc":
            query = query.order_by(
                OperacionModel.id_cuenta,
                OperacionModel.fch_operacion.desc(),
                OperacionModel.num_orden.desc()
            )
        
        result = db.session.execute(query)
        records = result.all()
        return records

    def get_operaciones_x_posicion_desde_fecha(self, id_cuenta, id_symbol, id_contrato_opcion, fch_operacion, incluir_fecha=True):
        query = db.select(
            OperacionModel
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.id_symbol == id_symbol,
            OperacionModel.id_contrato_opcion == id_contrato_opcion            
        )

        if incluir_fecha is True:
            query = query.where(
                OperacionModel.fch_operacion >= fch_operacion
            )
        else:
            query = query.where(
                OperacionModel.fch_operacion > fch_operacion
            )
        
        result = db.session.execute(query)
        return result.scalars().all()

    def get_siguiente_fch_operacion(self, id_cuenta, fch_operacion):
        query = db.select(
            OperacionModel.id_cuenta,
            func.min(OperacionModel.fch_operacion).label("fch_operacion")
        ).where(
            OperacionModel.id_cuenta == id_cuenta,
            OperacionModel.fch_operacion > fch_operacion
        ).group_by(
            OperacionModel.id_cuenta,
            OperacionModel.fch_operacion
        )

        result = db.session.execute(query)
        record = result.first()
        return record