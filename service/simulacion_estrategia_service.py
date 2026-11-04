from typing import List, Optional

from sqlalchemy.orm import joinedload

from config.extensions import db
from common.AppException import AppException
from model.contrato_opcion import ContratoOpcionModel
from model.simulacion_estrategia import SimulacionEstrategiaModel
from model.simulacion_grupo import SimulacionGrupoModel
from model.simulacion_pata import SimulacionPataModel
from model.symbol import SymbolModel
from schemas.simulacion_estrategia_schema import (
    SimulacionEstrategiaCreateRequest,
)


class SimulacionEstrategiaService:
    def guardar(
        self, id_usuario: int, params: SimulacionEstrategiaCreateRequest
    ) -> SimulacionEstrategiaModel:
        subyacente = self._obtener_subyacente(params)
        estrategia = SimulacionEstrategiaModel(
            id_usuario=id_usuario,
            id_subyacente_symbol=subyacente.id_symbol,
            nombre=params.nombre.strip(),
            etiqueta=params.etiqueta.strip(),
            notas=params.notas.strip() if params.notas else None,
            moneda_id=params.moneda_id.upper(),
        )

        for grupo_data in params.grupos:
            grupo = SimulacionGrupoModel(
                orden=grupo_data.orden,
                nombre=grupo_data.nombre.strip(),
                tipo=grupo_data.tipo.strip().upper(),
            )
            for orden_pata, pata_data in enumerate(grupo_data.contratos, start=1):
                contrato = self._obtener_contrato(pata_data.id_contrato_opcion, pata_data.cod_symbol)
                grupo.patas.append(
                    SimulacionPataModel(
                        orden=orden_pata,
                        id_contrato_opcion=(
                            contrato.id_contrato_opcion if contrato else None
                        ),
                        cod_symbol=pata_data.cod_symbol.strip().upper(),
                        tipo_opcion=pata_data.tipo_opcion,
                        fecha_vencimiento=pata_data.fecha_vencimiento,
                        strike=pata_data.strike,
                        posicion=pata_data.posicion,
                        cantidad=pata_data.cantidad,
                        multiplicador=pata_data.multiplicador,
                        precio_apertura=pata_data.precio_apertura,
                        moneda_id=pata_data.moneda_id.upper(),
                    )
                )
            estrategia.grupos.append(grupo)

        try:
            db.session.add(estrategia)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return self.obtener_por_id(id_usuario, estrategia.id_simulacion_estrategia)

    def listar(self, id_usuario: int) -> List[SimulacionEstrategiaModel]:
        return (
            SimulacionEstrategiaModel.query.options(
                joinedload(SimulacionEstrategiaModel.subyacente),
                joinedload(SimulacionEstrategiaModel.grupos)
                .joinedload(SimulacionGrupoModel.patas),
            )
            .filter(SimulacionEstrategiaModel.id_usuario == id_usuario)
            .order_by(SimulacionEstrategiaModel.fec_creacion.desc())
            .all()
        )

    def obtener_por_id(
        self, id_usuario: int, id_simulacion_estrategia: int
    ) -> Optional[SimulacionEstrategiaModel]:
        return (
            SimulacionEstrategiaModel.query.options(
                joinedload(SimulacionEstrategiaModel.subyacente),
                joinedload(SimulacionEstrategiaModel.grupos)
                .joinedload(SimulacionGrupoModel.patas),
            )
            .filter_by(
                id_usuario=id_usuario,
                id_simulacion_estrategia=id_simulacion_estrategia,
            )
            .first()
        )

    def eliminar(self, id_usuario: int, id_simulacion_estrategia: int) -> bool:
        estrategia = self.obtener_por_id(id_usuario, id_simulacion_estrategia)
        if not estrategia:
            return False
        try:
            db.session.delete(estrategia)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return True

    @staticmethod
    def _obtener_subyacente(params):
        query = SymbolModel.query
        if params.id_subyacente_symbol is not None:
            subyacente = query.filter_by(
                id_symbol=params.id_subyacente_symbol
            ).first()
        else:
            subyacente = query.filter(
                db.func.upper(SymbolModel.symbol)
                == params.cod_subyacente.strip().upper()
            ).first()
        if not subyacente:
            raise AppException(msg="No se encontró el instrumento subyacente en tb_symbol.")
        return subyacente

    @staticmethod
    def _obtener_contrato(id_contrato_opcion, cod_symbol):
        if id_contrato_opcion is not None:
            contrato = ContratoOpcionModel.query.filter_by(
                id_contrato_opcion=id_contrato_opcion
            ).first()
            if not contrato:
                raise AppException(
                    msg=f"No se encontró el contrato de opción con ID {id_contrato_opcion}."
                )
            return contrato
        return ContratoOpcionModel.query.filter(
            db.func.upper(ContratoOpcionModel.cod_symbol)
            == cod_symbol.strip().upper()
        ).first()
