"""
Punto de entrada principal para la aplicación Flask.

Este módulo configura la aplicación Flask, la conexión a la base de datos,
las políticas de CORS y registra tanto las rutas estándar como los recursos de la API heredada.
"""

from flask import Flask, request, jsonify, send_file, session
from flask_restful import Resource, Api
from flask_cors import CORS
from common.Response import Response
from boot.loader import init_constants

import json
from dotenv import load_dotenv
import os

load_dotenv()

from common.logger import logger  # noqa: E402
from config.config import Config  # noqa: E402
from config.extensions import db  # noqa: E402
from routes.router import init_routes  # noqa: E402


class EntryAPI(Resource):
    def get(self, module_name, class_name, method_name):
        obj_loader = Loader(module_name, class_name, method_name, data=request.args)
        response = send_file(obj_loader.response["file"])
        response.headers["file_name"] = obj_loader.response["file_name"]
        return response

    def post(self, module_name, class_name, method_name):
        try:
            logger.info(f"call class_name: {class_name}, method_name: {method_name}")
            # logging.basicConfig(filename=f"logs/bagholder_post_{date.today().isoformat()}.log", level=logging.INFO)

            # solo para probar se poneuser_id
            session["user_id"] = 1

            data = None

            if request.is_json:
                data = request.json
                data["access_token"] = request.headers.get("Authorization")
            else:
                data = {
                    "files": request.files,
                    "form": request.form,
                    "access_token": request.headers.get("Authorization"),
                }

            obj_Loader = Loader(module_name, class_name, method_name, data=data)
            response = None
            if type(obj_Loader.response).__name__ == "Response":
                response = obj_Loader.response.get_answer()
            else:
                response = obj_Loader.response
            return jsonify(response)
        except Exception as e:
            response = Response().from_exception(e)
            logger.error(json.dumps(response))
            return jsonify(response)


class Loader:
    def __init__(self, module_name, class_name, method_name, data=None):
        if data is None:
            data = {}
        mod = __import__("controller." + module_name, fromlist=[class_name])
        obj_reference = getattr(mod, class_name)
        if not obj_reference.AUTH_REQUIRED:
            self.obj = obj_reference()
        else:
            self.obj = obj_reference()
            self.obj.validar_token(data.get("access_token"))

        method_to_call = getattr(self.obj, method_name)
        self.response = method_to_call(data)


class ImageLoader(Resource):
    def get(self, image_loader):
        try:
            filename = "./upload/images/" + request.args.get("image")
            return send_file(filename, mimetype="image/jpg")
        except FileNotFoundError:
            return send_file("./defaults/default.png", mimetype="image/jpg")


###############


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app = Flask(__name__)

app.config.from_object(Config)
app.config.from_object("config.constants")

CORS(app, expose_headers=["Content-Disposition", "file_name"])

db.init_app(app)

with app.app_context():
    init_constants()
    init_routes(app)


# LEGACY
api = Api(app)
api.add_resource(
    EntryAPI,
    "/{}/<string:module_name>/<string:class_name>/<string:method_name>".format(
        app.config["BAGHOLDER_APPNAME"]
    ),
)
# api.add_resource(ConfirmRegistration, '/entablar/ConfirmRegistration',endpoint="confirm")
api.add_resource(
    ImageLoader, "/{}/<string:image_loader>/".format(app.config["BAGHOLDER_APPNAME"])
)


# app.run(debug=True)
