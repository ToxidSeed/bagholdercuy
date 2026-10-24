from flask import Blueprint, request
from flask_restful import Resource, Api
from pydantic import ValidationError

from service.ibkr_contract_map_service import IbkrContractMapService
from schemas.ibkr_contract_map_schema import (
    IbkrContractMapSyncRequest,
    IbkrContractMapFilterRequest,
)
from schemas.responses.ibkr_contract_map import (
    ibkr_contract_map_response_schema,
    ibkr_contract_maps_response_schema,
)
from common.AppException import AppException
from common.logger import logger


class IbkrContractMapController(Resource):
    AUTH_REQUIRED = False

    def get(self, id_ibkr_contract_map: int = None, args=None):
        try:
            service = IbkrContractMapService()

            if id_ibkr_contract_map is not None:
                record = service.get_by_id(id_ibkr_contract_map)
                if not record:
                    return {
                        "success": False,
                        "message": f"Mapeo de contrato con ID {id_ibkr_contract_map} no encontrado.",
                    }, 404
                serialized = ibkr_contract_map_response_schema.dump(record)
                return {
                    "success": True,
                    "message": "Mapeo de contrato obtenido correctamente.",
                    "data": serialized,
                }, 200

            if args is None:
                args = request.args.to_dict() if request.args else {}
                if not args and request.is_json:
                    args = request.get_json(silent=True) or {}

            params = IbkrContractMapFilterRequest(**args)

            if params.id_symbol and not (
                params.conid or params.cod_symbol or params.id_contrato_opcion
            ):
                record = service.get_by_symbol_id(params.id_symbol)
                if not record:
                    return {
                        "success": False,
                        "message": f"No se encontró mapeo para el símbolo con ID {params.id_symbol}.",
                    }, 404
                serialized = ibkr_contract_map_response_schema.dump(record)
                return {
                    "success": True,
                    "message": "Mapeo de contrato obtenido correctamente.",
                    "data": serialized,
                }, 200

            records = service.get_mappings(params)
            serialized = ibkr_contract_maps_response_schema.dump(records)
            return {
                "success": True,
                "message": "Mapeos de contratos obtenidos correctamente.",
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

            params = IbkrContractMapSyncRequest(**args)
            service = IbkrContractMapService()

            result = service.sync_symbol_mapping(
                id_symbol=params.id_symbol,
                cod_symbol=params.cod_symbol,
                exchange=params.exchange,
            )

            serialized = ibkr_contract_map_response_schema.dump(result)
            return {
                "success": True,
                "message": "Contrato sincronizado y mapeado correctamente.",
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


def init_module(app, url_prefix):
    bp = Blueprint("ibkr_contract_map_bp", __name__)
    api = Api(bp)

    api.add_resource(
        IbkrContractMapController,
        "",
        "/",
        "/<int:id_ibkr_contract_map>",
        "/sync",
    )

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/ibkr-contract-map")
