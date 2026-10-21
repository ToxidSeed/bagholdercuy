import logging
from flask import Blueprint, request
from flask_restful import Resource, Api
from pydantic import ValidationError

from service.contrato_opcion_service import ContratoOpcionService
from schemas.contrato_opcion_schema import (
    ContratoOpcionFiltroRequest,
    ContratoOpcionChainRequest,
    ContratoOpcionCreateRequest,
    ContratoOpcionMarketDataLoaderRequest,
    ContratoOpcionCsvLoaderRequest,
)
from schemas.responses.contrato_opcion import (
    contrato_opcion_response_schema,
    contratos_opcion_response_schema,
    contrato_opcion_chain_response_schema,
    contrato_opcion_resumen_list_response_schema,
)
from common.AppException import AppException
from common.logger import logger
from config.extensions import db


class ContratoOpcionController(Resource):
    AUTH_REQUIRED = False

    def get(self, id_contrato_opcion=None, args=None):
        try:
            service = ContratoOpcionService()
            if id_contrato_opcion is not None:
                record = service.get_by_id(id_contrato_opcion)
                if not record:
                    return {
                        "success": False,
                        "message": f"Contrato de opción con ID {id_contrato_opcion} no encontrado.",
                    }, 404
                serialized = contrato_opcion_response_schema.dump(record)
                return {
                    "success": True,
                    "message": "Contrato de opción obtenido correctamente.",
                    "data": serialized,
                }, 200

            if args is None:
                args = request.args.to_dict() if request.args else {}
                if not args and request.is_json:
                    args = request.get_json(silent=True) or {}

            params = ContratoOpcionFiltroRequest(**args)
            records = service.get_contratos(params)
            serialized = contratos_opcion_response_schema.dump(records)
            return {
                "success": True,
                "message": "Contratos de opciones obtenidos correctamente.",
                "data": serialized,
            }, 200

        except ValidationError as e:
            errors_list = [
                f"{err['loc'][-1]}: {err['msg']}" if err.get("loc") else err["msg"]
                for err in e.errors()
            ]
            msg = "; ".join(errors_list) or "Errores de validación"
            return {"success": False, "message": msg, "errors": errors_list}, 400
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500

    def post(self, args=None):
        try:
            if args is None:
                args = request.get_json(silent=True) or {}
                if not args and request.form:
                    args = request.form.to_dict()
                if not args and request.args:
                    args = request.args.to_dict()

            params = ContratoOpcionCreateRequest(**args)
            service = ContratoOpcionService()
            opcion = service.guardar(params)
            serialized = contrato_opcion_response_schema.dump(opcion)

            return {
                "success": True,
                "message": "Se ha guardado correctamente la opcion.",
                "data": serialized,
            }, 201

        except ValidationError as e:
            db.session.rollback()
            errors_list = [
                f"{err['loc'][-1]}: {err['msg']}" if err.get("loc") else err["msg"]
                for err in e.errors()
            ]
            msg = "; ".join(errors_list) or "Errores de validación"
            return {"success": False, "message": msg, "errors": errors_list}, 400
        except AppException as e:
            db.session.rollback()
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500

    # =========================================================================
    # Métodos de compatibilidad legacy (EntryAPI / vistas anteriores)
    # =========================================================================
    def get_contratos(self, args=None):
        res, code = self.get(args=args)
        return res

    def guardar(self, args=None):
        res, code = self.post(args=args)
        return res

    def get_options_chain(self, args=None):
        chain_ctrl = ContratoOpcionChainController()
        res, code = chain_ctrl.get(args=args)
        return res

    def get_resumen_subyacentes(self, args=None):
        resumen_ctrl = ContratoOpcionResumenController()
        res, code = resumen_ctrl.get()
        return res

    def get_calls(self, args=None):
        args = args or {}
        filtro = {
            "cod_symbol": args.get("cod_symbol"),
            "sentidos": ["CALL"],
            "fch_expiracion": args.get("expiration_date") or args.get("fch_expiracion"),
            "imp_ejercicio": args.get("strike") or args.get("imp_ejercicio"),
        }
        res, code = self.get(args=filtro)
        return res.get("data", []) if isinstance(res, dict) else res

    def get_puts(self, args=None):
        args = args or {}
        filtro = {
            "cod_symbol": args.get("cod_symbol"),
            "sentidos": ["PUT"],
            "fch_expiracion": args.get("expiration_date") or args.get("fch_expiracion"),
            "imp_ejercicio": args.get("strike") or args.get("imp_ejercicio"),
        }
        res, code = self.get(args=filtro)
        return res.get("data", []) if isinstance(res, dict) else res

    def get_expiration_dates(self, args=None):
        args = args or {}
        symbol = args.get("symbol") or args.get("cod_symbol")
        service = ContratoOpcionService()
        return service.get_expiration_dates(symbol=symbol)

    def get_strikes(self, symbol="", exp_date="", args=None):
        if args and isinstance(args, dict):
            symbol = symbol or args.get("symbol") or args.get("cod_symbol")
            exp_date = exp_date or args.get("exp_date") or args.get("fch_expiracion")
        service = ContratoOpcionService()
        return service.get_strikes(symbol=symbol, exp_date=exp_date)


class ContratoOpcionChainController(Resource):
    AUTH_REQUIRED = False

    def get(self, args=None):
        return self._procesar(args)

    def post(self, args=None):
        return self._procesar(args)

    def _procesar(self, args=None):
        try:
            if args is None:
                args = request.args.to_dict() if request.args else {}
                if not args and request.is_json:
                    args = request.get_json(silent=True) or {}
                if not args and request.form:
                    args = request.form.to_dict()

            params = ContratoOpcionChainRequest(**args)
            service = ContratoOpcionService()
            chain_data = service.get_options_chain(params)
            serialized = contrato_opcion_chain_response_schema.dump(chain_data)

            return {
                "success": True,
                "message": "Cadena de opciones obtenida correctamente.",
                "data": serialized,
            }, 200

        except ValidationError as e:
            errors_list = [
                f"{err['loc'][-1]}: {err['msg']}" if err.get("loc") else err["msg"]
                for err in e.errors()
            ]
            msg = "; ".join(errors_list) or "Errores de validación"
            return {"success": False, "message": msg, "errors": errors_list}, 400
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500


class ContratoOpcionResumenController(Resource):
    AUTH_REQUIRED = False

    def get(self):
        try:
            service = ContratoOpcionService()
            results = service.get_resumen_subyacentes()
            serialized = contrato_opcion_resumen_list_response_schema.dump(results)
            return {
                "success": True,
                "message": "Resumen de subyacentes obtenido correctamente.",
                "data": serialized,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500

    def post(self, args=None):
        return self.get()


class ContratoOpcionLoaderMarketDataController(Resource):
    AUTH_REQUIRED = False

    def post(self, args=None):
        try:
            if args is None:
                args = request.get_json(silent=True) or {}
                if not args and request.form:
                    args = request.form.to_dict()
                if not args and request.args:
                    args = request.args.to_dict()

            params = ContratoOpcionMarketDataLoaderRequest(**args)
            service = ContratoOpcionService()
            count = service.load_from_marketdata(
                cod_symbol=params.cod_symbol, fch_expiracion=params.fch_expiracion
            )
            return {
                "success": True,
                "message": f"Se han cargado correctamente {count} contratos para {params.cod_symbol}.",
                "data": {"count": count, "cod_symbol": params.cod_symbol},
            }, 200

        except ValidationError as e:
            errors_list = [
                f"{err['loc'][-1]}: {err['msg']}" if err.get("loc") else err["msg"]
                for err in e.errors()
            ]
            msg = "; ".join(errors_list) or "Errores de validación"
            return {"success": False, "message": msg, "errors": errors_list}, 400
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500


class ContratoOpcionLoaderCsvController(Resource):
    AUTH_REQUIRED = False

    def post(self, args=None):
        try:
            files = request.files if request.files else {}
            form = request.form.to_dict() if request.form else {}
            if args and isinstance(args, dict):
                files = args.get("files") or files
                form = args.get("form") or form

            tmp_fichero = files.get("fichero") if hasattr(files, "get") else None
            if tmp_fichero is None:
                return {
                    "success": False,
                    "message": "No se ha proporcionado el archivo 'fichero'.",
                }, 400

            params = ContratoOpcionCsvLoaderRequest(**form)
            service = ContratoOpcionService()
            service.load_from_csv(tmp_fichero, params)

            return {
                "success": True,
                "message": "Se ha procesado correctamente el fichero con los codigos de opcion.",
            }, 200

        except ValidationError as e:
            errors_list = [
                f"{err['loc'][-1]}: {err['msg']}" if err.get("loc") else err["msg"]
                for err in e.errors()
            ]
            msg = "; ".join(errors_list) or "Errores de validación"
            return {"success": False, "message": msg, "errors": errors_list}, 400
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500


# =============================================================================
# Clases de compatibilidad para EntryAPI (Loader legacy)
# =============================================================================
class SymbolLoader:
    AUTH_REQUIRED = False

    def load(self, args=None):
        ctrl = ContratoOpcionLoaderMarketDataController()
        res, code = ctrl.post(args=args)
        return res


class CsvLoader:
    AUTH_REQUIRED = False

    def procesar(self, args=None):
        ctrl = ContratoOpcionLoaderCsvController()
        res, code = ctrl.post(args=args)
        return res


OpcionesContratoManager = ContratoOpcionController


def init_module(app, url_prefix):
    bp = Blueprint("contrato_opcion_bp", __name__)
    api = Api(bp)

    api.add_resource(
        ContratoOpcionController,
        "",
        "/",
        "/<int:id_contrato_opcion>",
    )
    api.add_resource(
        ContratoOpcionChainController,
        "/chain",
        "/cadena",
    )
    api.add_resource(
        ContratoOpcionResumenController,
        "/resumen-subyacentes",
    )
    api.add_resource(
        ContratoOpcionLoaderMarketDataController,
        "/loader/marketdata",
    )
    api.add_resource(
        ContratoOpcionLoaderCsvController,
        "/loader/csv",
    )

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/contratos-opcion")
