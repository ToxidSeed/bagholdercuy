from distutils.log import error
from app import db
#from config import *
from common.AppException import AppException
from model.TipoCambio import TipoCambioModel
from common.api.iexcloud import iexcloud
from common.api.Alphavantage import Alphavantage
from common.Response import Response
from datetime import datetime, date
from config.general import MARKET_API, DEFAULT_LIMIT
from config.negocio import IND_ACTIVO
from controller.base import Base

class CurrencyExchangeManager:
    def __init__(self):
        pass

class CurrencyExchangeFinder(Base):
    AUTH_REQUIRED=True

    def get_historic_rates(self, args={}):
        data = db.session.query(
            TipoCambioModel    
        ).order_by(TipoCambioModel.fch_cambio.desc())\
        .limit(DEFAULT_LIMIT)\
        .all()

        return Response().from_raw_data(data)

class DataLoader:
    def __init__(self):
        bridges = {
            "IEXCLOUD":IEXCloud_Bridge
        }
        self.bridge = bridges[MARKET_API]()

    def do(self, args={}):
        try:
            self._val_do_params(args)
            pares = args["pares"].split(",")
            for par in pares:
                self.process_elem(par=par)
            db.session.commit()
            return Response(msg="Se han cargado correctamente los pares")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def process_elem(self, par=""):
        par_comps = par.split('/')

        base = par_comps[0]
        ref = par_comps[1]

        data = AlphavantageBridge().fx_daily(base, ref)
        for elem in data:
            db.session.add(elem)

    def _val_do_params(self, args={}):
        errors = []        
        if "pares" not in args:
            errors.append("El parámetro 'pares' no ha sido enviado en la petición")

        if len(errors) > 0:
            raise AppException(msg="Se han encontrado errores de validación", errors=errors)    
    

class AlphavantageBridge:
    def __init__(self):
        pass

    def fx_daily(self,base="",ref=""):    
        params = {
            "outputsize":"full",
            "from_symbol":base,
            "to_symbol":ref
        }

        parname = "{0}/{1}".format(base, ref)

        results = Alphavantage().fx_daily(params=params)
        series = results["Time Series FX (Daily)"]
        objlist = []    

        for key, elem in series.items():
            newobj = TipoCambioModel(
                fch_cambio = key,
                mon_base_id = base,
                mon_ref_id = ref,
                ind_activo = IND_ACTIVO,
                par_nombre = parname,
                imp_compra = float(elem["4. close"]),
                imp_venta = float(elem["4. close"]),
                fch_registro = date.today(),
                fch_audit = datetime.today()
            )
            objlist.append(newobj)

        return objlist

class IEXCloud_Bridge:
    def __init__(self):
        self.loaded_dates = []        
    
    def load(self, args={}):
        pairs = self.__fx_historical(args)
        data = []
        if len(pairs) > 0:
            data = pairs[0]

        self.__save(data)            

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

        new_rate = TipoCambioModel(
            """
            fecha_cambio = date.fromisoformat(elem["date"]),
            moneda_base_symbol= moneda_base_symbol,
            moneda_ref_symbol = moneda_ref_symbol,
            ind_activo = 'S',
            par_name = par_name,
            importe_compra = elem["rate"],
            importe_venta = elem["rate"],
            fecha_registro = date.today(),
            fecha_audit = datetime.now()
            """
        )
        db.session.add(new_rate)

    def __fx_historical(self, args={}):                
        params={}
        #params["from"] = args["desde"]
        #params["from"] = 
        #
        #params["from"] = "2022-01-01"
        #params["symbols"] = args["pares"]
        api = iexcloud()        
        return api.fx_historical(params)


