from flask import request
from flask_restful import Resource
from controller.base import Base
from reader.transaccion import TransaccionReader
from common.Response import Response
from common.AppException import AppException
from pydantic import ValidationError
from schemas.transaccion import TransaccionAgrupadaSearchRequest
from schemas.responses.transaccion import transacciones_agrupadas_schema            
from flask import Blueprint
from flask_restful import Api


class TransaccionController(Base):
    AUTH_REQUIRED = False

    def get_fechas_con_transacciones(self, args=None):
        id_cuenta = args.get("id_cuenta")
        cod_symbol = args.get("cod_symbol")
        fch_ini = args.get("fch_ini")
        fch_fin = args.get("fch_fin")
        results = TransaccionReader.get_fechas_con_transacciones(id_cuenta, cod_symbol, fch_ini, fch_fin)
        return Response().from_raw_data(results)

    def get_transacciones_x_fecha(self, args=None):
        id_cuenta = args.get("id_cuenta")
        cod_symbol = args.get("cod_symbol")
        fch_hr_transaccion = args.get("fch_hr_transaccion")
        results = TransaccionReader.get_transacciones_x_fecha(id_cuenta, cod_symbol, fch_hr_transaccion)
        return Response().from_raw_data(results)

    def get_transacciones_x_symbol(self, args=None):
        id_cuenta = args.get("id_cuenta")
        cod_symbol = args.get("cod_symbol")
        results = TransaccionReader.get_transacciones_x_symbol(id_cuenta, cod_symbol)
        return Response().from_raw_data(results)

    def get_max_fechas_agroupadas_x_symbol(self, args=None):
        id_cuenta = args.get("id_cuenta")
        results = TransaccionReader.get_max_fechas_agroupadas_x_symbol(id_cuenta)
        return Response().from_raw_data(results)


class TransaccionAgrupadaSearch(Resource):
    AUTH_REQUIRED = False

    def post(self, args=None):
        if args is None:
            args = request.get_json() or {}
        try:
            params = TransaccionAgrupadaSearchRequest(**args)
        except ValidationError as e:
            errors_list = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            raise AppException(msg="Errores de validación", errors=errors_list)

        results = TransaccionReader.get_max_fechas_agroupadas_x_symbol(params.id_cuenta)
        response = transacciones_agrupadas_schema.dump(results)
        return response, 200


def init_module(app, url_prefix):
    bp = Blueprint("transaccion_bp", __name__)
    api = Api(bp)

    api.add_resource(TransaccionAgrupadaSearch, "/transaccion-agrupada-search")

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/transaccion")
