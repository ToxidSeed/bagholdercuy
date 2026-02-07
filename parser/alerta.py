from parser.base import BaseParser


class AlertaParser:
    def parse_args_get_alertas_x_configuracion(self, args=None):
        parser = BaseParser(args=args)

        args["id_config_alerta"] = parser.get("id_config_alerta", requerido=True, datatype=int)
        return args
