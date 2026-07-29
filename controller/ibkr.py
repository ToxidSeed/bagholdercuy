from flask import Blueprint, request
from flask_restful import Resource, Api
from service.markets_data_providers.ibkr.ibkr_contracts_service import (
    IbkrContractsService,
)
from common.AppException import AppException
from config.extensions import db
from common.logger import logger


class IbkrContractsController(Resource):
    AUTH_REQUIRED = False

    def post(self):
        try:
            # Aceptamos tanto JSON body como query parameters
            args = request.get_json() or {}
            if not args:
                args = request.args.to_dict() or {}

            exchange = args.get("exchange")
            if not exchange:
                raise AppException(msg="El parámetro 'exchange' es requerido")

            inserted_count = IbkrContractsService().load_contracts(exchange)
            return {
                "success": True,
                "message": f"Se han cargado correctamente {inserted_count} contratos para el exchange {exchange}.",
                "data": {"inserted_count": inserted_count},
            }, 200
        except AppException as e:
            db.session.rollback()
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500


def init_module(app, url_prefix):
    bp = Blueprint("ibkr_bp", __name__)
    api = Api(bp)

    api.add_resource(IbkrContractsController, "/trsrv/load-all-conids")

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/ibkr")
