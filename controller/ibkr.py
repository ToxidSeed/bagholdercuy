from flask import Blueprint, request
from flask_restful import Resource, Api
from service.markets_data_providers.ibkr.ibkr_contracts_service import (
    IbkrContractsService,
)
from api.ibkr import InteractiveBrokersClient
from common.AppException import AppException
from config.extensions import db
from common.logger import logger
from schemas.responses.ibkr import ibkr_contracts_schema


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

    def get(self):
        try:
            # Aceptamos tanto JSON body como query parameters
            args = request.args.to_dict() or {}

            exchange = args.get("exchange")

            contracts = IbkrContractsService().get_all_contracts(exchange)
            ibkr_contracts_response = ibkr_contracts_schema.dump(contracts)
            print(ibkr_contracts_response)
            response_data = {
                "success": True,
                "message": f"Se han obtenido correctamente {len(contracts)} contratos para el exchange {exchange or 'todos'}.",
                "data": {
                    "contracts": ibkr_contracts_response,
                    "count": len(contracts),
                    "exchange": exchange,
                },
            }
            return response_data, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500


class IbkrSymbolController(Resource):
    AUTH_REQUIRED = False

    def get(self):
        try:
            args = request.args.to_dict() or {}
            if not args and request.is_json:
                args = request.get_json() or {}

            symbol = args.get("symbol") or args.get("ticker")
            if not symbol:
                raise AppException(msg="El parámetro 'symbol' es requerido")

            name = args.get("name")
            if isinstance(name, str):
                name = name.lower() in ("true", "1", "yes")

            sec_type = args.get("sec_type") or args.get("secType")
            more = args.get("more")
            if isinstance(more, str):
                more = more.lower() in ("true", "1", "yes")

            contracts = InteractiveBrokersClient.secdef_search(
                symbol=symbol,
                name=name,
                sec_type=sec_type,
                more=more,
            )

            count = len(contracts) if isinstance(contracts, list) else 0

            return {
                "success": True,
                "message": f"Se han obtenido correctamente {count} resultados para el símbolo '{symbol}'.",
                "data": contracts,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500


def init_module(app, url_prefix):
    bp = Blueprint("ibkr_bp", __name__)
    api = Api(bp)

    api.add_resource(IbkrContractsController, "/contracts")
    api.add_resource(IbkrSymbolController, "/symbol", "/symbols")

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/ibkr")
