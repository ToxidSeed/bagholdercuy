## Especificación

# Generalidades

* Los controladores tienen que heredar de **Resource** (from flask_restful import Resource)
* Los controladores tienen que tener sufijo "Controller"
* El Blueprint tiene que tener el nombre del modulo con prefijo "bp" 
* Al hacer register_blueprint el argumento **url_prefix** tiene que concatenarse con el nombre del modulo.
* Los controladores deben devolver los datos y/o respuesta mas el código de de la respuesta, ya que estamos usando **Resource**, por ejemplo:
* Si el modulo no existe se tiene que añadir a **routes/router.py**

```python
return {"success": False, "message": e.msg, "errors": e.errors}, 400
```

* Tienen que tener autoregistro en un módulo:

En el ejemplo:

* Nombre del Modulo: ibkr.py
* Nombre del Blueprint: "ibkr_bp"
* Nombre del resource: IbkrContractsController
* url_prefix del registro: "/ibkr"
* Endpoint: "/contracts", donde contracts tiene que ver con la categoria de datos que se van a cargar. 
* La ruta final es: /api/v2/ibkr/contracts/

```python
def init_module(app, url_prefix):
    bp = Blueprint("ibkr_bp", __name__)
    api = Api(bp)

    api.add_resource(IbkrContractsController, "/contracts")

    app.register_blueprint(bp, url_prefix=f"{url_prefix}/ibkr")
```

### Resources que muestran datos

* El flujo de datos debe ser Resource(Controller) -> Service -> Reader (en caso de que se necesite un modelo) -> Models(SQLAlchemy)
* La respuesta del Resource cuando se hace lecturas de tablas o si se va a devolver datos es con un esquema definido en Marshmallow (from flask_marshmallow import Marshmallow)

