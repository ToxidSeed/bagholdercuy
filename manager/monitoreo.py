from model.monitoreo import MonitoreoModel
from model.contrato_opcion import ContratoOpcionModel
from reader.monitoreo import MonitoreoReader
from reader.symbol import SymbolReader
from reader.contratoopcion import ContratoOpcionReader
from config.extensions import db
from datetime import date, datetime
from common.AppException import AppException


class MonitoreoManager:
    def registrar(self, monitoreo_nuevo: MonitoreoModel) -> MonitoreoModel:
        monitoreo_reader = MonitoreoReader()

        # Si viene información de un contrato de opción para crear/obtener
        if (
            hasattr(monitoreo_nuevo, "contrato_opcion_data")
            and monitoreo_nuevo.contrato_opcion_data
        ):
            data = monitoreo_nuevo.contrato_opcion_data
            id_subyacente = data.get("id_symbol_subyacente") or data.get("id_symbol")
            if not id_subyacente:
                raise AppException(
                    msg="Debe indicar el símbolo subyacente para el contrato de opción"
                )

            subyacente = SymbolReader().get(id_symbol=id_subyacente)
            if not subyacente:
                raise AppException(
                    msg=f"No se ha encontrado el símbolo subyacente con id {id_subyacente}"
                )

            fch_venc = data.get("fch_vencimiento")
            if isinstance(fch_venc, str):
                try:
                    fch_venc = date.fromisoformat(fch_venc[:10])
                except (ValueError, TypeError):
                    fch_venc = date.today()
            elif not isinstance(fch_venc, (date, datetime)):
                fch_venc = date.today()

            tipo_opcion = str(data.get("tipo_opcion", "CALL")).upper()
            try:
                imp_strike = float(data.get("imp_strike", 0.0) or 0.0)
            except (ValueError, TypeError):
                imp_strike = 0.0

            sub_ticker = (subyacente.symbol or "").strip().upper()
            cod_symbol = data.get("cod_symbol")

            # Garantizar que cod_symbol sea el ticker OSI y nunca solo el símbolo subyacente
            if (
                not cod_symbol
                or (sub_ticker and cod_symbol.strip().upper() == sub_ticker)
                or (sub_ticker and len(cod_symbol.strip()) <= len(sub_ticker))
            ):
                d_str = fch_venc.strftime("%y%m%d")
                t_char = "C" if tipo_opcion.startswith("C") else "P"
                strike_str = f"{int(round(imp_strike * 1000)):08d}"
                cod_symbol = f"{sub_ticker}{d_str}{t_char}{strike_str}"

            opcion = ContratoOpcionReader.get_contrato(cod_symbol=cod_symbol)
            if opcion is None:
                opcion = ContratoOpcionModel(
                    id_symbol_subyacente=id_subyacente,
                    cod_symbol=cod_symbol,
                    tipo_opcion=tipo_opcion,
                    fch_vencimiento=fch_venc,
                    imp_strike=imp_strike,
                    tam_contrato=data.get("tam_contrato", 100) or 100,
                    cod_moneda=data.get("cod_moneda", "USD") or "USD",
                    descripcion=data.get("descripcion") or f"{sub_ticker} {fch_venc.isoformat()} ${imp_strike} {tipo_opcion}",
                )
                db.session.add(opcion)
                db.session.flush()

            monitoreo_nuevo.id_contrato_opcion = opcion.id_contrato_opcion
            monitoreo_nuevo.id_symbol_type = 2
            monitoreo_nuevo.id_symbol = None

        # Caso 1: Monitoreo de Opción (id_symbol_type = 2)
        if monitoreo_nuevo.id_contrato_opcion is not None:
            monitoreo_nuevo.id_symbol_type = 2
            monitoreo_nuevo.id_symbol = None

            opcion = ContratoOpcionReader.get_by_id(
                monitoreo_nuevo.id_contrato_opcion
            )
            if opcion is None:
                raise AppException(
                    msg=f"No se ha encontrado un contrato de opción con id {monitoreo_nuevo.id_contrato_opcion}"
                )

            monitoreo = monitoreo_reader.get_by_option(
                id_contrato_opcion=monitoreo_nuevo.id_contrato_opcion,
                id_cuenta=monitoreo_nuevo.id_cuenta,
            )
            if monitoreo is not None:
                if getattr(monitoreo, "flg_activo", 1) == 0:
                    monitoreo.flg_activo = 1
                    monitoreo.fch_registro = date.today()
                    return monitoreo
                raise AppException(
                    f"El monitoreo para la opción {opcion.cod_symbol} y cuenta {monitoreo_nuevo.id_cuenta} ya existe en la base de datos"
                )

            # Registrar en tb_ibkr_contract_map
            conid = None
            if (
                hasattr(monitoreo_nuevo, "contrato_opcion_data")
                and monitoreo_nuevo.contrato_opcion_data
            ):
                conid = monitoreo_nuevo.contrato_opcion_data.get("conid")
            if not conid and hasattr(monitoreo_nuevo, "conid"):
                conid = monitoreo_nuevo.conid

            if not conid:
                try:
                    from service.markets_data_providers.ibkr.ibkr_cotizacion_service import (
                        IbkrCotizacionService,
                    )
                    conid = IbkrCotizacionService()._resolve_conid(opcion.cod_symbol)
                except Exception:
                    pass

            if conid:
                from model.ibkr_contract_map import IbkrContractMapModel
                IbkrContractMapModel.set_mapping(
                    conid=conid,
                    id_contrato_opcion=monitoreo_nuevo.id_contrato_opcion,
                )

        # Caso 2: Monitoreo de Símbolo estándar (Stock, ETF, Index, etc. id_symbol_type != 2)
        else:
            if monitoreo_nuevo.id_symbol is None:
                raise AppException(
                    msg="Debe indicar id_symbol o id_contrato_opcion para registrar el monitoreo"
                )

            symbol = SymbolReader().get(id_symbol=monitoreo_nuevo.id_symbol)
            if symbol is None:
                raise AppException(
                    msg=f"No se ha encontrado un symbol con id {monitoreo_nuevo.id_symbol}"
                )

            monitoreo_nuevo.id_contrato_opcion = None
            if not monitoreo_nuevo.id_symbol_type or monitoreo_nuevo.id_symbol_type == 2:
                monitoreo_nuevo.id_symbol_type = symbol.id_symbol_type or 1

            monitoreo = monitoreo_reader.get_by_symbol(
                id_symbol=monitoreo_nuevo.id_symbol,
                id_cuenta=monitoreo_nuevo.id_cuenta,
            )
            if monitoreo is not None:
                if getattr(monitoreo, "flg_activo", 1) == 0:
                    monitoreo.flg_activo = 1
                    monitoreo.fch_registro = date.today()
                    return monitoreo
                raise AppException(
                    f"El monitoreo con symbol {symbol.symbol} y id cuenta {monitoreo_nuevo.id_cuenta} ya existe en la base de datos"
                )

            conid = getattr(monitoreo_nuevo, "conid", None)
            if conid:
                from model.ibkr_contract_map import IbkrContractMapModel
                IbkrContractMapModel.set_mapping(
                    conid=conid,
                    id_symbol=monitoreo_nuevo.id_symbol,
                )

        if not monitoreo_nuevo.fch_registro:
            monitoreo_nuevo.fch_registro = date.today()

        if not getattr(monitoreo_nuevo, "flg_activo", None):
            monitoreo_nuevo.flg_activo = 1

        db.session.add(monitoreo_nuevo)
        return monitoreo_nuevo

    def desactivar(self, id_monitoreo: int) -> MonitoreoModel:
        monitoreo = MonitoreoReader().get(id_monitoreo=id_monitoreo)
        if monitoreo is None:
            raise AppException(
                msg=f"No se ha encontrado el monitoreo con id {id_monitoreo}"
            )
        monitoreo.flg_activo = 0
        return monitoreo

