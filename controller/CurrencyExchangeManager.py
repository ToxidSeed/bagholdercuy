from distutils.log import error
from app import db
from config import *
from common.AppException import AppException
from model.CurrencyExchangeModel import CurrencyExchangeModel
from common.api.iexcloud import iexcloud
from common.Response import Response
from datetime import datetime, date

class CurrencyExchangeManager:

    def __init__(self):
        pass

class CurrencyExchangeFinder:
    def __init__(self):
        pass

    def get_historic_rates(self, args={}):
        data = CurrencyExchangeModel.query.all()
        return Response().from_raw_data(data)

class DataLoader:
    def __init__(self):
        bridges = {
            "IEXCLOUD":IEXCloud_Bridge
        }
        self.bridge = bridges[MARKET_API]()

    def do(self, args={}):
        self.bridge.load(args)

class IEXCloud_Bridge:
    def __init__(self):
        self.loaded_dates = []        
    
    def load(self, args={}):
        try:
            pairs = self.__fx_historical(args)
            data = []
            if len(pairs) > 0:
                data = pairs[0]

            self.__save(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def __save(self, data=[]):
        for elem in data:
            self.__single_save(elem)

    def __single_save(self, elem):  
        if elem["date"] in self.loaded_dates:
            return None
        else:
            self.loaded_dates.append(elem["date"])

        symbol = elem["symbol"]
        moneda_base_symbol = symbol[:3]
        moneda_ref_symbol = symbol[3:]

        par_name = '{0}/{1}'.format(moneda_base_symbol,moneda_ref_symbol)

        new_rate = CurrencyExchangeModel(
            fecha_cambio = date.fromisoformat(elem["date"]),
            moneda_base_symbol= moneda_base_symbol,
            moneda_ref_symbol = moneda_ref_symbol,
            ind_activo = 'S',
            par_name = par_name,
            importe_compra = elem["rate"],
            importe_venta = elem["rate"],
            fecha_registro = date.today(),
            fecha_audit = datetime.now()
        )
        db.session.add(new_rate)

    def __fx_historical(self, params={}):        
        errors = []
        if "from" not in params:
            errors.append("El parámetro 'from' es obligatorio")
        
        if "symbols" not in params:
            errors.append("El parámetro 'symbols' es obligatorio")

        if len(errors) > 0:
            raise AppException(msg="No se han ingresado los parámetros obligatorios", errors=errors)

        api = iexcloud()        
        return api.fx_historical(params)
