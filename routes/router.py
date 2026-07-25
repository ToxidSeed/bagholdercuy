# routes/router.py

def init_routes(app):
    prefix = f"/{app.config['BAGHOLDER_APPNAME']}/api/v2"

    # Lista de módulos a inicializar
    modules = [
        "controller.transaccion",
        "controller.reportes",
        "controller.SerieManager"
    ]

    for mod_name in modules:
        module = __import__(mod_name, fromlist=["init_module"])

        if hasattr(module, "init_module"):
            module.init_module(app, prefix)
