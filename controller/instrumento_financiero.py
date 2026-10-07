from flask import Blueprint, request
from flask_restful import Resource, Api
from reader.instrumento_financiero import InstrumentoFinancieroReader
from common.Response import Response
from common.AppException import AppException


class InstrumentoFinancieroController(Resource):
    AUTH_REQUIRED = False

    def get(self, args=None):
        try:
            records = InstrumentoFinancieroReader.get_list()
            return Response().from_raw_data(records), 200
        except Exception as e:
            response = Response().from_exception(e)
            return response, 400 if isinstance(e, AppException) else 500


def init_module(app, url_prefix):
    bp = Blueprint("instrumento_financiero_bp", __name__)
    api = Api(bp)

    api.add_resource(InstrumentoFinancieroController, "")

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/instrumento-financiero")