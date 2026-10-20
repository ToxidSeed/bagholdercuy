from flask import Blueprint, request
from flask_restful import Resource, Api
from pydantic import ValidationError

from service.cotizacion_service import CotizacionService
from schemas.cotizacion_schema import CotizacionGetRequest
from schemas.responses.cotizacion import (
    cotizacion_response_schema,
    cotizaciones_response_schema,
)
from common.AppException import AppException
from common.logger import logger


class CotizacionController(Resource):
    AUTH_REQUIRED = False

    def get(self, args=None):
        if args is None:
            args = request.args.to_dict() if request.args else {}
        return self._procesar_cotizacion(args)

    def post(self, args=None):
        if args is None:
            args = request.get_json(silent=True) or {}
            if not args and request.form:
                args = request.form.to_dict()
            if not args and request.args:
                args = request.args.to_dict()
        return self._procesar_cotizacion(args)

    def _procesar_cotizacion(self, args: dict):
        try:
            params = CotizacionGetRequest(**args)
            service = CotizacionService()

            if params.is_bulk_request:
                items = service.resolve_items_to_quote(
                    symbol_ids=params.get_symbol_ids(),
                    contrato_ids=params.get_contrato_opcion_ids(),
                    cod_symbols=(
                        params.get_cod_symbols()
                        if not (params.id_symbol or params.id_contrato_opcion)
                        else []
                    ),
                )
                quotes = service.get_cotizaciones(
                    items=items,
                    provider=params.provider,
                )
                serialized_data = cotizaciones_response_schema.dump(quotes)

                return {
                    "success": True,
                    "message": "Cotizaciones obtenidas correctamente.",
                    "data": serialized_data,
                }, 200
            else:
                cod_syms = params.get_cod_symbols()
                cod_sym = cod_syms[0] if cod_syms else params.cod_symbol

                quote_data = service.get_cotizacion(
                    cod_symbol=cod_sym,
                    provider=params.provider,
                )
                serialized_data = cotizacion_response_schema.dump(quote_data)

                return {
                    "success": True,
                    "message": "Cotización obtenida correctamente.",
                    "data": serialized_data,
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


def init_module(app, url_prefix):
    bp = Blueprint("cotizacion_bp", __name__)
    api = Api(bp)

    api.add_resource(
        CotizacionController,
        "",
        "/",
    )

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/cotizaciones")
