from flask import Blueprint, request
from flask_restful import Resource, Api
from parser.monitoreo import MonitoreoParser
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

            monitoreo_parser = MonitoreoParser()
            monitoreo_reader = MonitoreoReader()

            requeridos, opcionales = monitoreo_parser.parse_args_get_lista_seguimiento(
                args=args
            )
            records = monitoreo_reader.get_monitoreo_activo(
                id_cuenta=requeridos.get("id_cuenta"), opcionales=opcionales
            )

            raw_response = Response().from_raw_data(records)
            return {
                "success": True,
                "message": "Monitoreo activo obtenido correctamente.",
                "data": raw_response.get("data", []),
            }, 200
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

            monitoreo_parser = MonitoreoParser()
            monitoreo_nuevo = monitoreo_parser.parse_args_registrar(args=args)
            MonitoreoManager().registrar(monitoreo_nuevo=monitoreo_nuevo)

            db.session.commit()
            return {
                "success": True,
                "message": "Se ha registrado el monitoreo correctamente.",
                "data": {
                    "id_monitoreo": monitoreo_nuevo.id_monitoreo,
                    "id_symbol": monitoreo_nuevo.id_symbol,
                    "id_cuenta": monitoreo_nuevo.id_cuenta,
                },
            }, 201
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
