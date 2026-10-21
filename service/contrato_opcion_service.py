import os
import tempfile
import uuid
import logging
from datetime import date, datetime
from typing import Dict, Any, List, Optional
from flask import current_app
from sqlalchemy.sql.functions import func

from config.extensions import db
from model.contrato_opcion import ContratoOpcionModel
from reader.contratoopcion import ContratoOpcionReader
from reader.symbol import SymbolReader
from processor.opcion import OpcionProcessor, OpcionLoader
from api.marketdata import MarketDataAPI
from common.AppException import AppException
from schemas.contrato_opcion_schema import (
    ContratoOpcionFiltroRequest,
    ContratoOpcionChainRequest,
    ContratoOpcionCreateRequest,
    ContratoOpcionCsvLoaderRequest,
)

logger = logging.getLogger(__name__)


class ContratoOpcionService:
    def get_contratos(
        self, params: ContratoOpcionFiltroRequest
    ) -> List[ContratoOpcionModel]:
        return ContratoOpcionReader.get_contratos(
            id_contrato_opcion=params.id_contrato_opcion,
            cod_subyacente=params.cod_symbol,
            id_symbol_subyacente=params.id_symbol_subyacente,
            sentidos=params.sentidos or [],
            fch_expiracion=params.fch_expiracion,
            imp_ejercicio=params.imp_ejercicio,
            limit=params.limit or 200,
        )

    def get_by_id(self, id_contrato_opcion: int) -> Optional[ContratoOpcionModel]:
        return ContratoOpcionReader.get_by_id(id_contrato_opcion=id_contrato_opcion)

    def get_options_chain(self, params: ContratoOpcionChainRequest) -> Dict[str, Any]:
        calls = ContratoOpcionReader.get_calls(
            cod_subyacente=params.cod_symbol,
            fch_expiracion=params.fch_expiracion,
            imp_ejercicio=params.imp_ejercicio,
        )
        puts = ContratoOpcionReader.get_puts(
            cod_subyacente=params.cod_symbol,
            fch_expiracion=params.fch_expiracion,
            imp_ejercicio=params.imp_ejercicio,
        )

        call_exp_dates = [
            c.fch_vencimiento.isoformat()
            if hasattr(c.fch_vencimiento, "isoformat")
            else str(c.fch_vencimiento)
            for c in calls
            if c.fch_vencimiento
        ]
        put_exp_dates = [
            p.fch_vencimiento.isoformat()
            if hasattr(p.fch_vencimiento, "isoformat")
            else str(p.fch_vencimiento)
            for p in puts
            if p.fch_vencimiento
        ]

        exp_dates = sorted(list(set(call_exp_dates + put_exp_dates)))

        call_strikes = [
            float(c.imp_strike) for c in calls if c.imp_strike is not None
        ]
        put_strikes = [
            float(p.imp_strike) for p in puts if p.imp_strike is not None
        ]

        strikes = sorted(list(set(call_strikes + put_strikes)))

        return {
            "calls": calls,
            "puts": puts,
            "exp_dates": exp_dates,
            "strikes": strikes,
        }

    def guardar(self, data: ContratoOpcionCreateRequest) -> ContratoOpcionModel:
        subyacente = SymbolReader().get(cod_symbol=data.cod_subyacente)
        if not subyacente:
            raise AppException(msg=f"El subyacente {data.cod_subyacente} no existe")

        opcion = ContratoOpcionModel()
        opcion.cod_symbol = data.cod_symbol
        opcion.tipo_opcion = data.sentido.upper()
        opcion.id_symbol_subyacente = subyacente.id_symbol
        opcion.fch_vencimiento = data.fch_expiracion
        opcion.imp_strike = data.imp_ejercicio
        opcion.tam_contrato = data.ctd_tamano_contrato or 100
        opcion.cod_moneda = data.cod_moneda or "USD"
        opcion.descripcion = data.descripcion
        opcion.fch_audit = datetime.now()
        opcion.fch_registro = datetime.now()

        OpcionProcessor().guardar(opcion)
        db.session.commit()
        return opcion

    def get_resumen_subyacentes(self) -> List[Any]:
        results = (
            db.session.query(
                ContratoOpcionModel.cod_symbol_subyacente,
                func.max(ContratoOpcionModel.fch_registro).label("fch_registro"),
                func.max(ContratoOpcionModel.fch_vencimiento).label("fch_vencimiento"),
            )
            .group_by(ContratoOpcionModel.cod_symbol_subyacente)
            .all()
        )
        return results

    def get_expiration_dates(self, symbol: str) -> List[str]:
        if not symbol:
            raise AppException(msg="El parámetro 'symbol' es requerido")
        fch_hoy = date.today().isoformat()
        results = (
            db.session.query(ContratoOpcionModel.fch_vencimiento)
            .filter(
                ContratoOpcionModel.cod_symbol_subyacente == symbol,
                ContratoOpcionModel.fch_vencimiento >= fch_hoy,
            )
            .distinct(ContratoOpcionModel.fch_vencimiento)
            .order_by(ContratoOpcionModel.fch_vencimiento.asc())
            .all()
        )
        return [
            row.fch_vencimiento.isoformat()
            if hasattr(row.fch_vencimiento, "isoformat")
            else str(row.fch_vencimiento)
            for row in results
        ]

    def get_strikes(
        self, symbol: str, exp_date: Optional[str] = None
    ) -> List[float]:
        if not symbol:
            raise AppException(msg="El parámetro 'symbol' es requerido")

        query = db.session.query(ContratoOpcionModel.imp_strike).filter(
            ContratoOpcionModel.cod_symbol_subyacente == symbol
        )

        if not exp_date:
            query = query.filter(
                ContratoOpcionModel.fch_vencimiento >= date.today().isoformat()
            )
        else:
            query = query.filter(ContratoOpcionModel.fch_vencimiento == exp_date)

        query = query.distinct(ContratoOpcionModel.imp_strike).order_by(
            ContratoOpcionModel.imp_strike.asc()
        )

        results = query.all()
        return [float(row.imp_strike) for row in results if row.imp_strike is not None]

    def load_from_marketdata(self, cod_symbol: str, fch_expiracion: date) -> int:
        subyacente = SymbolReader().get(cod_symbol=cod_symbol)
        if not subyacente:
            raise AppException(msg=f"El symbol {cod_symbol} no existe en la base de datos")

        contratos = MarketDataAPI().get_options_chain(
            cod_subyacente=cod_symbol, fch_expiracion=fch_expiracion
        )

        loaded_count = 0
        for elem in contratos:
            contrato = ContratoOpcionReader.get_contrato(
                cod_symbol=elem.get("optionSymbol")
            )
            if contrato is None:
                exp_val = elem.get("expiration")
                if isinstance(exp_val, (int, float)):
                    fch_venc = datetime.utcfromtimestamp(exp_val)
                elif isinstance(exp_val, str):
                    fch_venc = date.fromisoformat(exp_val)
                else:
                    fch_venc = fch_expiracion

                oc = ContratoOpcionModel(
                    tam_contrato=100,
                    fch_vencimiento=fch_venc,
                    tipo_opcion=elem["side"].upper(),
                    imp_strike=elem["strike"],
                    cod_symbol=elem["optionSymbol"],
                    id_symbol_subyacente=subyacente.id_symbol,
                    fch_registro=datetime.now(),
                    fch_audit=datetime.now(),
                )
                db.session.add(oc)
                db.session.flush()
                loaded_count += 1

        db.session.commit()
        return loaded_count

    def load_from_csv(
        self, file_storage, params: ContratoOpcionCsvLoaderRequest
    ) -> bool:
        tmp_dir = current_app.config.get("RUTA_TMP", tempfile.gettempdir())
        fch_actual_iso = date.today().isoformat()
        fichero_nombre = f"tmp_cod_symbol_{uuid.uuid4().hex}_{fch_actual_iso}.csv"
        fichero_ruta = os.path.join(tmp_dir, fichero_nombre)
        file_storage.save(fichero_ruta)

        opcion_loader = OpcionLoader()
        opcion_loader.fichero = fichero_ruta
        opcion_loader.cod_moneda = params.cod_moneda
        opcion_loader.ctd_multiplicador = params.ctd_multiplicador
        opcion_loader.formato_cod_opcion = params.formato_cod_opcion
        opcion_loader.flg_excluir_errores = params.flg_excluir_errores
        opcion_loader.procesar()
        db.session.commit()
        return True
