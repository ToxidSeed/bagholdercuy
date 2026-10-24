# routes/router.py


def init_routes(app):
    prefix = f"/{app.config['BAGHOLDER_APPNAME']}/api/v2"

    # Lista de módulos a inicializar
    modules = [
        "controller.transaccion",
        "controller.reportes",
        "controller.serie_controller",
        "controller.ibkr",
        "controller.symbol_type",
        "controller.monitoreo",
        "controller.cotizacion_controller",
        "controller.contrato_opcion_controller",
        "controller.ibkr_contract_map_controller",
    ]

    for mod_name in modules:
        module = __import__(mod_name, fromlist=["init_module"])

        if hasattr(module, "init_module"):
            module.init_module(app, prefix)
