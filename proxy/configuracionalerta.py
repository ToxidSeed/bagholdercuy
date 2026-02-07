from model.configuracionalerta import ConfiguracionAlertaModel

class ConfiguracionAlertaNuevaProxy:
    def __init__(self):
        self._model = ConfiguracionAlertaModel()
        self._id_cuenta = None
        self._id_symbol = None
        self._cod_tipo_variacion_imp_accion = None
        self._ctd_variacion_imp_accion = None
        self._imp_inicial_ciclos = None

    @property
    def id_cuenta(self):
        return self._id_cuenta

    @id_cuenta.setter
    def id_cuenta(self, value):
        self._id_cuenta = value

    @property
    def id_symbol(self):
        return self._id_symbol






    def model(self):
        return self._model