from flask import Blueprint, request
from flask_restful import Resource, Api
from reader.symbol_type import SymbolTypeReader
from common.Response import Response
from common.AppException import AppException


class SymbolTypeController(Resource):
    AUTH_REQUIRED = False

    def get(self, args=None):
        try:
            records = SymbolTypeReader.get_list()
            return Response().from_raw_data(records), 200
        except Exception as e:
            response = Response().from_exception(e)
            return response, 400 if isinstance(e, AppException) else 500


def init_module(app, url_prefix):
    bp = Blueprint("symbol_type_bp", __name__)
    api = Api(bp)

    api.add_resource(SymbolTypeController, "", "/", "/list")

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/symbol-type")