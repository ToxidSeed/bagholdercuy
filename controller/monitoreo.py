from flask import Blueprint, request
from flask_restful import Resource, Api
from pydantic import ValidationError
from schemas.monitoreo_schema import (
    MonitoreoGetRequest,
    MonitoreoRegistrarRequest,
)
from reader.monitoreo import MonitoreoReader
from manager.monitoreo import MonitoreoManager
from common.Response import Response
from common.AppException import AppException
from common.logger import logger
from config.extensions import db


class MonitoreoController(Resource):
    AUTH_REQUIRED = False

    def get(self, args=None):
        try:
            if args is None:
                args = request.args.to_dict() if request.args else {}
                if not args and request.is_json:
                    args = request.get_json(silent=True) or {}

            params = MonitoreoGetRequest(**args)
            records = MonitoreoReader().get_monitoreo_activo(
                id_cuenta=params.id_cuenta, opcionales=params.to_opcionales()
            )

            raw_response = Response().from_raw_data(records)
            return {
                "success": True,
                "message": "Monitoreo activo obtenido correctamente.",
                "data": raw_response.get("data", []),
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
                if not args:
                    args = request.args.to_dict() if request.args else {}

            params = MonitoreoRegistrarRequest(**args)
            monitoreo_nuevo = params.to_model()
            MonitoreoManager().registrar(monitoreo_nuevo=monitoreo_nuevo)

            db.session.commit()
            return {
                "success": True,
                "message": "Se ha registrado el monitoreo correctamente.",
                "data": {
                    "id_monitoreo": monitoreo_nuevo.id_monitoreo,
                    "id_symbol": monitoreo_nuevo.id_symbol,
                    "id_contrato_opcion": monitoreo_nuevo.id_contrato_opcion,
                    "id_symbol_type": monitoreo_nuevo.id_symbol_type,
                    "id_cuenta": monitoreo_nuevo.id_cuenta,
                },
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


def init_module(app, url_prefix):
    bp = Blueprint("monitoreos_bp", __name__)
    api = Api(bp)

    api.add_resource(
        MonitoreoController,
        "",
        "/",
    )
    app.register_blueprint(bp, url_prefix=f"{url_prefix}/monitoreos")
