from app import db
from model.transaccion import TransaccionModel
from model.ibkr_operacion_importada import IbkrOperacionImportadaModel, CodigoOperacionIBKR, CategoriaActivo
from reader.ibkr_operacion_importada import IbkrOperacionImportadaReader
from domain.contratoopcion import ContratoOpcionHumanReadable
from constants.tipo_transaccion import get_tipo_transaccion
from constants.instrumento_financiero import get_instrumento_financiero
import datetime
import uuid

class IbkrTransaccionesService:
    def __init__(self):
        pass

    def generar_transacciones(self, operaciones_importadas=None, id_importacion=None, id_cuenta=None):
        """
        Parametros de entrada:
            operaciones_importadas: List[id_importacion: int]
            id_importacion: int
            id_cuenta: int
        Proceso:
            1. Por cada operacion_importada se debe generar una transaccion (TransaccionModel)
            2. Una vez creada la transaccion actualizar la operacion importada con el id de la transaccion
            3. por cada id_importacion, obtener los otros datos desde IbkrImportacionModel
            4. 
        """
        if not id_cuenta:
            raise ValueError("El parametro id_cuenta es requerido")

        if id_importacion is not None and not operaciones_importadas:
            operaciones_importadas_objs = IbkrOperacionImportadaReader.get_por_importacion(id_importacion)
        elif operaciones_importadas:
            operaciones_importadas_objs = IbkrOperacionImportadaReader.get_por_ids(operaciones_importadas)
        else:
            operaciones_importadas_objs = []

        if not operaciones_importadas_objs:
            return

        tipo_transaccion = get_tipo_transaccion()
        instrumento_financiero = get_instrumento_financiero()

        #OPEN: C
        #CLOSE: V        

        equivalencias_categoria_instrumento = {
            CategoriaActivo.ACCIONES.value: instrumento_financiero.STOCK,
            CategoriaActivo.OPCIONES.value: instrumento_financiero.OPTION
        }

        for op in operaciones_importadas_objs:
            if op.procesado:
                continue

            if op.cantidad > 0:
                id_tipo_transaccion = tipo_transaccion.C
            else:
                id_tipo_transaccion = tipo_transaccion.V

            if op.categoria_activo == CategoriaActivo.ACCIONES.value:
                cod_symbol = op.cod_symbol
            elif op.categoria_activo == CategoriaActivo.OPCIONES.value:
                contrato_opcion = ContratoOpcionHumanReadable(op.cod_symbol)
                cod_symbol = contrato_opcion.get_codigo_occ_extendido()
            else:
                cod_symbol = op.cod_symbol

            transaccion = TransaccionModel(                
                id_cuenta=id_cuenta,
                cod_symbol=cod_symbol,
                id_tipo_transaccion=id_tipo_transaccion,
                id_instrumento_financiero=equivalencias_categoria_instrumento[op.categoria_activo],
                fch_transaccion=op.fch_hora_operacion.date() if op.fch_hora_operacion else datetime.date.today(),
                orden_fifo=0,
                cantidad=op.cantidad,
                imp_unitario=op.precio_trade if op.precio_trade is not None else 0,
                imp_transaccion=op.importe_bruto if op.importe_bruto is not None else 0,
            )
            db.session.add(transaccion)
            db.session.flush()

            op.id_transaccion = transaccion.id_transaccion
            op.procesado = True
            op.fch_procesado = datetime.datetime.utcnow()

        db.session.commit()