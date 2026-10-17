from flask import Blueprint, request
from flask_restful import Resource, Api
from service.markets_data_providers.ibkr.ibkr_contract_service import (
    IbkrContractService,
)
from service.markets_data_providers.ibkr.ibkr_options_service import (
    IbkrOptionsService,
)
from common.AppException import AppException
from config.extensions import db
from common.logger import logger
import json
import requests


class IbkrContractsController(Resource):
    AUTH_REQUIRED = False

    def get(self):
        try:
            args = request.args

            try:
                conid = args.get("conid", type=int)
                page = int(args.get("page", 1))
                page_size = int(args.get("page_size", 100))
            except (ValueError, TypeError):
                raise AppException(
                    msg="Los parámetros 'conid', 'page' y 'page_size' deben ser numéricos"
                )

            if args.get("conid") and conid is None:
                raise AppException(msg="El parámetro 'conid' debe ser numérico")

            try:
                result = IbkrContractService().get_contracts(
                    conid=conid,
                    cod_symbol=args.get("cod_symbol"),
                    exchange=args.get("exchange"),
                    page=page,
                    page_size=page_size,
                )
            except ValueError as e:
                raise AppException(msg=str(e))

            return {
                "success": True,
                "message": f"Se encontraron {result['total']} contratos.",
                "data": result,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500

    def post(self):
        try:
            # Aceptamos tanto JSON body como query parameters
            args = request.get_json(silent=True) or {}
            if not args:
                args = request.args.to_dict() or {}

            exchange = args.get("exchange")
            if not exchange:
                raise AppException(msg="El parámetro 'exchange' es requerido")

            inserted_count = IbkrContractService().load_contracts(exchange)
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


class IbkrExpirationDatesController(Resource):
    AUTH_REQUIRED = False

    def get(self):
        try:
            cod_symbol = request.args.get("cod_symbol") or request.args.get("symbol")
            if not cod_symbol or not str(cod_symbol).strip():
                raise AppException(msg="El parámetro 'cod_symbol' es requerido")

            try:
                result = IbkrOptionsService().get_expiration_months(
                    cod_symbol=str(cod_symbol).strip()
                )
            except ValueError as e:
                raise AppException(msg=str(e))

            return {
                "success": True,
                "message": f"Se encontraron {len(result)} fechas de expiración.",
                "data": result,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True)
            return {
                "success": False,
                "message": f"Error de comunicación con IBKR Gateway: {str(e)}",
            }, 502
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500

    def post(self):
        try:
            args = request.get_json(silent=True) or {}
            if not args:
                args = request.args.to_dict() or {}

            cod_symbol = args.get("cod_symbol") or args.get("symbol")
            if not cod_symbol or not str(cod_symbol).strip():
                raise AppException(msg="El parámetro 'cod_symbol' es requerido")

            try:
                result = IbkrOptionsService().get_expiration_months(
                    cod_symbol=str(cod_symbol).strip()
                )
            except ValueError as e:
                raise AppException(msg=str(e))

            return {
                "success": True,
                "message": f"Se encontraron {len(result)} fechas de expiración.",
                "data": result,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True)
            return {
                "success": False,
                "message": f"Error de comunicación con IBKR Gateway: {str(e)}",
            }, 502
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500


class IbkrStrikesController(Resource):
    AUTH_REQUIRED = False

    def get(self):
        try:
            cod_subyacente = (
                request.args.get("cod_subyacente")
                or request.args.get("cod_symbol")
                or request.args.get("symbol")
            )
            if not cod_subyacente or not str(cod_subyacente).strip():
                raise AppException(msg="El parámetro 'cod_subyacente' es requerido")

            expiracion = (
                request.args.get("expiracion")
                or request.args.get("expiration")
                or request.args.get("month")
            )
            if not expiracion or not str(expiracion).strip():
                raise AppException(msg="El parámetro 'expiracion' es requerido")

            exchange = request.args.get("exchange")

            try:
                result = IbkrOptionsService().get_strikes(
                    cod_subyacente=str(cod_subyacente).strip(),
                    expiracion=str(expiracion).strip(),
                    exchange=str(exchange).strip() if exchange else None,
                )
            except ValueError as e:
                raise AppException(msg=str(e))

            return {
                "success": True,
                "message": "Strikes obtenidos correctamente.",
                "data": result,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True)
            return {
                "success": False,
                "message": f"Error de comunicación con IBKR Gateway: {str(e)}",
            }, 502
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500

    def post(self):
        try:
            args = request.get_json(silent=True) or {}
            if not args:
                args = request.args.to_dict() or {}

            cod_subyacente = (
                args.get("cod_subyacente")
                or args.get("cod_symbol")
                or args.get("symbol")
            )
            if not cod_subyacente or not str(cod_subyacente).strip():
                raise AppException(msg="El parámetro 'cod_subyacente' es requerido")

            expiracion = (
                args.get("expiracion")
                or args.get("expiration")
                or args.get("month")
            )
            if not expiracion or not str(expiracion).strip():
                raise AppException(msg="El parámetro 'expiracion' es requerido")

            exchange = args.get("exchange")

            try:
                result = IbkrOptionsService().get_strikes(
                    cod_subyacente=str(cod_subyacente).strip(),
                    expiracion=str(expiracion).strip(),
                    exchange=str(exchange).strip() if exchange else None,
                )
            except ValueError as e:
                raise AppException(msg=str(e))

            return {
                "success": True,
                "message": "Strikes obtenidos correctamente.",
                "data": result,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True)
            return {
                "success": False,
                "message": f"Error de comunicación con IBKR Gateway: {str(e)}",
            }, 502
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500

class IbkrOptionsChainController(Resource):
    AUTH_REQUIRED = False

    def get(self):
        try:
            cod_subyacente = request.args.get("cod_subyacente")
            if not cod_subyacente or not str(cod_subyacente).strip():
                raise AppException(msg="El parámetro 'cod_subyacente' es requerido")

            fch_expiracion = request.args.get("fch_expiracion")

            num_strikes = request.args.get("num_strikes")
            parsed_num_strikes = 50
            if num_strikes is not None and str(num_strikes).strip() != "":
                if str(num_strikes).strip().lower() in ("todos", "all"):
                    parsed_num_strikes = 0
                else:
                    try:
                        parsed_num_strikes = int(num_strikes)
                    except (ValueError, TypeError):
                        raise AppException(
                            msg="El parámetro 'num_strikes' debe ser un número entero válido"
                        )

            try:
                result = IbkrOptionsService().get_options_chain(
                    cod_subyacente=str(cod_subyacente).strip(),
                    fch_expiracion=str(fch_expiracion).strip() if fch_expiracion else None,
                    num_strikes=parsed_num_strikes,
                )
            except (json.decoder.JSONDecodeError, requests.exceptions.JSONDecodeError) as e:
                logger.error(e, exc_info=True)
                raise AppException(
                    msg="Error de comunicación con IBKR Gateway: la respuesta no es un JSON válido o la sesión no está autenticada."
                )
            except ValueError as e:
                raise AppException(msg=str(e))

            return {
                "success": True,
                "message": "Cadena de opciones obtenida correctamente.",
                "data": result,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True)
            return {
                "success": False,
                "message": f"Error de comunicación con IBKR Gateway: {str(e)}",
            }, 502
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500

    def post(self):
        try:
            args = request.get_json(silent=True) or {}
            if not args:
                args = request.args.to_dict() or {}

            cod_subyacente = args.get("cod_subyacente")
            if not cod_subyacente or not str(cod_subyacente).strip():
                raise AppException(msg="El parámetro 'cod_subyacente' es requerido")

            fch_expiracion = args.get("fch_expiracion")

            num_strikes = args.get("num_strikes")
            parsed_num_strikes = 50
            if num_strikes is not None and str(num_strikes).strip() != "":
                if str(num_strikes).strip().lower() in ("todos", "all"):
                    parsed_num_strikes = 0
                else:
                    try:
                        parsed_num_strikes = int(num_strikes)
                    except (ValueError, TypeError):
                        raise AppException(
                            msg="El parámetro 'num_strikes' debe ser un número entero válido"
                        )

            try:
                result = IbkrOptionsService().get_options_chain(
                    cod_subyacente=str(cod_subyacente).strip(),
                    fch_expiracion=str(fch_expiracion).strip() if fch_expiracion else None,
                    num_strikes=parsed_num_strikes,
                )
            except (json.decoder.JSONDecodeError, requests.exceptions.JSONDecodeError) as e:
                logger.error(e, exc_info=True)
                raise AppException(
                    msg="Error de comunicación con IBKR Gateway: la respuesta no es un JSON válido o la sesión no está autenticada."
                )
            except ValueError as e:
                raise AppException(msg=str(e))

            return {
                "success": True,
                "message": "Cadena de opciones obtenida correctamente.",
                "data": result,
            }, 200
        except AppException as e:
            return {"success": False, "message": e.msg, "errors": e.errors}, 400
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True)
            return {
                "success": False,
                "message": f"Error de comunicación con IBKR Gateway: {str(e)}",
            }, 502
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"success": False, "message": f"Error no controlado: {str(e)}"}, 500


def init_module(app, url_prefix):
    bp = Blueprint("ibkr_bp", __name__)
    api = Api(bp)

    api.add_resource(
        IbkrContractsController, "/trsrv/load-all-conids", "/trsrv/contracts"
    )
    api.add_resource(
        IbkrExpirationDatesController,
        "/contracts/expiration-dates",
        "/expiration-dates",
    )
    api.add_resource(
        IbkrStrikesController,
        "/options/strikes",
        "/contracts/strikes",
        "/strikes",
    )
    api.add_resource(
        IbkrOptionsChainController,
        "/options/chain",
        "/contracts/options-chain",
        "/options-chain",
    )

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/ibkr")
