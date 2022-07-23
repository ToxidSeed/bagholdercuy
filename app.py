from flask import Flask, request, jsonify, send_file, session
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import traceback
import sys, os
import json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
app = Flask(__name__)

app.config.from_object("config.general")
#app.secret_key = "4CE30D91FB0487BCAF5858A822D66C4C40897BB397D7D26AE651CD78BF1BB8FD"


CORS(app,expose_headers=["Content-Disposition", "file_name"])

db = SQLAlchemy(app)
api = Api(app)

class EntryAPI(Resource):
    def get(self, module_name, class_name, method_name):
        obj_loader = Loader(module_name, class_name, method_name, data=request.args)
        response = send_file(filename_or_fp=obj_loader.response['file'])
        response.headers["file_name"] = obj_loader.response['file_name']
        return response

    def post(self, module_name, class_name, method_name):        
        #solo para probar se poneuser_id        
        print(app)        
        session["user_id"] = 1

        data = None

        if request.is_json:
            data = request.json
        else:
            data = {
                "files": request.files,
                "form": request.form
            }

        obj_Loader = Loader(module_name, class_name, method_name, data=data)
        response = None
        if type(obj_Loader.response).__name__ == "Response":
            response = obj_Loader.response.get_answer()
        else:
            response = obj_Loader.response
        return jsonify(response)

class Loader:
    def __init__(self, module_name, class_name, method_name, data={}):
        mod =  __import__("controller."+module_name, fromlist=[class_name])
        obj_reference = getattr(mod, class_name)
        self.obj = obj_reference()
        method_to_call = getattr(self.obj, method_name)
        self.response = method_to_call(data)


class ImageLoader(Resource):
    def get(self, image_loader):
        try:
            filename = "./upload/images/" + request.args.get('image')
            return send_file(filename, mimetype='image/jpg')
        except FileNotFoundError:
            return send_file("./defaults/default.png", mimetype='image/jpg')

"""class ConfirmRegistration(Resource):
    def get(self):
        from controller.SessionManager import SessionManager
        token = request.args.get('token')
        SessionManager().confirm(token)
"""

api.add_resource(EntryAPI, "/{}/<string:module_name>/<string:class_name>/<string:method_name>".format(app.config["APPNAME"]))
#api.add_resource(ConfirmRegistration, '/entablar/ConfirmRegistration',endpoint="confirm")
api.add_resource(ImageLoader, "/{}/<string:image_loader>/".format(app.config["APPNAME"]))


#app.run(debug=True)