import jwt
from flask import Blueprint, request
from flask_restful import Api, Resource
from pydantic import ValidationError

from common.AppException import AppException
from common.logger import logger
from config.extensions import db
from controller.base import Base
from schemas.responses.simulacion_estrategia import (
    simulacion_estrategia_response_schema,
    simulacion_estrategias_response_schema,
)
from schemas.simulacion_estrategia_schema import (
    SimulacionEstrategiaCreateRequest,
    SimulacionEstrategiaIdRequest,
)
from service.simulacion_estrategia_service import SimulacionEstrategiaService


class SimulacionEstrategiaController(Resource):
    AUTH_REQUIRED = True

    def get(self, id_simulacion_estrategia=None):
        try:
            id_usuario = self._usuario_autenticado()
            service = SimulacionEstrategiaService()
            if id_simulacion_estrategia is not None:
                id_params = SimulacionEstrategiaIdRequest(
                    id_simulacion_estrategia=id_simulacion_estrategia
                )
                estrategia = service.obtener_por_id(
                    id_usuario, id_params.id_simulacion_estrategia
                )
                if not estrategia:
                    return {
                        "success": False,
                        "message": "Estrategia guardada no encontrada.",
                    }, 404
                data = simulacion_estrategia_response_schema.dump(estrategia)
                return {
                    "success": True,
                    "message": "Estrategia obtenida correctamente.",
                    "data": data,
                }, 200

            estrategias = service.listar(id_usuario)
            data = simulacion_estrategias_response_schema.dump(estrategias)
            return {
                "success": True,
                "message": "Estrategias obtenidas correctamente.",
                "data": data,
            }, 200
        except ValidationError as e:
            errors = [
                f"{err['loc'][-1]}: {err['msg']}" if err.get("loc") else err["msg"]
                for err in e.errors()
            ]
            return {
                "success": False,
                "message": "; ".join(errors) or "Errores de validación.",
                "errors": errors,
            }, 400
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 401
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": "No se pudieron obtener las estrategias."}, 500

    def post(self):
        try:
            id_usuario = self._usuario_autenticado()
            payload = request.get_json(silent=True) or {}
            params = SimulacionEstrategiaCreateRequest(**payload)
            estrategia = SimulacionEstrategiaService().guardar(id_usuario, params)
            data = simulacion_estrategia_response_schema.dump(estrategia)
            return {
                "success": True,
                "message": "Estrategia guardada correctamente.",
                "data": data,
            }, 201
        except ValidationError as e:
            errors = [
                f"{err['loc'][-1]}: {err['msg']}" if err.get("loc") else err["msg"]
                for err in e.errors()
            ]
            db.session.rollback()
            return {
                "success": False,
                "message": "; ".join(errors) or "Errores de validación.",
                "errors": errors,
            }, 400
        except AppException as e:
            db.session.rollback()
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(e, exc_info=True)
            return {"success": False, "message": "No se pudo guardar la estrategia."}, 500

    def delete(self, id_simulacion_estrategia):
        try:
            id_usuario = self._usuario_autenticado()
            id_params = SimulacionEstrategiaIdRequest(
                id_simulacion_estrategia=id_simulacion_estrategia
            )
            deleted = SimulacionEstrategiaService().eliminar(
                id_usuario, id_params.id_simulacion_estrategia
            )
            if not deleted:
                return {
                    "success": False,
                    "message": "Estrategia guardada no encontrada.",
                }, 404
            return {
                "success": True,
                "message": "Estrategia eliminada correctamente.",
                "data": {"id_simulacion_estrategia": id_params.id_simulacion_estrategia},
            }, 200
        except ValidationError as e:
            errors = [
                f"{err['loc'][-1]}: {err['msg']}" if err.get("loc") else err["msg"]
                for err in e.errors()
            ]
            return {
                "success": False,
                "message": "; ".join(errors) or "Errores de validación.",
                "errors": errors,
            }, 400
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 401
        except Exception as e:
            db.session.rollback()
            logger.error(e, exc_info=True)
            return {"success": False, "message": "No se pudo eliminar la estrategia."}, 500

    @staticmethod
    def _usuario_autenticado():
        token = request.headers.get("Authorization")
        if not token:
            raise AppException(msg="Debe iniciar sesión para guardar estrategias.")
        try:
            usuario = Base().validar_token(token)
            return int(usuario.id)
        except Exception as e:
            raise AppException(msg="El token de acceso es inválido o ha expirado.") from e


def init_module(app, url_prefix):
    bp = Blueprint("simulacion_estrategia_bp", __name__)
    api = Api(bp)
    api.add_resource(
        SimulacionEstrategiaController,
        "",
        "/",
        "/<int:id_simulacion_estrategia>",
    )
    app.register_blueprint(bp, url_prefix=f"{url_prefix}/simulacion-estrategias")
