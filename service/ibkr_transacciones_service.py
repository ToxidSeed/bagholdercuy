from app import db
from model.transaccion import TransaccionModel
from model.ibkr_operacion_importada import IbkrOperacionImportadaModel, CodigoOperacionIBKR, CategoriaActivo
from reader.ibkr_operacion_importada import IbkrOperacionImportadaReader
from domain.contratoopcion import ContratoOpcionHumanReadable
from constants.tipo_transaccion import get_tipo_transaccion
from constants.instrumento_financiero import get_instrumento_financiero
import datetime
import uuid
from constants.indicador_apcierre import indicador_apcierre
from constants.evento_origen import evento_origen

from constants.ibkr import (
    CONST_IBKR_EVENTO_DEFAULT, 
    LIST_INDICADORES_AP_CIERRE, 
    LIST_EVENTOS_ORIGEN_IBKR,
    MAP_IBKR_TO_GENERIC_EVENT
)

class IbkrTransaccionesService:
    def categorizar_codes(self, codigo_operacion: str):
        indicador_apcierre_code = None
        evento_origen_code = None

        codes = codigo_operacion.split(";")
        for code in codes:
            if code in LIST_INDICADORES_AP_CIERRE:
                indicador_apcierre_code = code
            elif code in LIST_EVENTOS_ORIGEN_IBKR:
                evento_origen_code = code
            else:
                raise ValueError(f"No se pudo mapear el codigo de operacion: {code}")

        if evento_origen_code is None:
            evento_origen_code = CONST_IBKR_EVENTO_DEFAULT
        
        return indicador_apcierre_code, evento_origen_code

    def generar_transacciones(self, operaciones_importadas=None, id_importacion=None, id_cuenta=None):
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
                    
            indicador_apcierre_code, raw_evento_origen_code = self.categorizar_codes(op.codigo)
            evento_origen_code = MAP_IBKR_TO_GENERIC_EVENT.get(raw_evento_origen_code)
            if evento_origen_code is None:
                raise ValueError(f"No se pudo mapear el evento de origen: {raw_evento_origen_code}")
            
            id_indicador_apcierre = indicador_apcierre.get(indicador_apcierre_code).id_indicador_apcierre
            id_evento_origen = evento_origen.get(evento_origen_code).id_evento_origen

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
                fch_hr_transaccion=op.fch_hora_operacion if op.fch_hora_operacion else datetime.now(),
                id_indicador_apcierre=id_indicador_apcierre,
                id_evento_origen=id_evento_origen ,
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