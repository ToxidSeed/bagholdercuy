from app import app
from datetime import date, datetime


class Fecha:
    def __init__(self, fecha: date = None):
        self.valor = fecha

    @staticmethod
    def from_client(strdate):
        fecha = datetime.strptime(strdate, app.config.get("CLIENT_DATE_FORMAT"))
        return Fecha(fecha=fecha)


