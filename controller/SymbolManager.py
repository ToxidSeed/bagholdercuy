from distutils.log import error
from app import db
import inspect
from common.AppException import AppException
from model.StockSymbol import StockSymbol as SymbolModel
from model.OptionContract import OptionContract
from common.Response import Response
from datetime import datetime, date
from common.api.iexcloud import iexcloud
import common.logger as logger


class SymbolManager:
    def __init__(self):
        self.symbol = None

    def save(self, args={}):
        try:
            self.__val_save(args)            
            if self.__is_new(args):
                symbol = self.__collect(args)
                self.__append(symbol)
            else:
                self.__update(args)
            db.session.commit()
            return Response(msg="Se ha guardado correctamente el symbol").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)


    def __append(self,symbol_obj):
        db.session.add(symbol_obj)

    def __update(self, args={}):
        symbol_to_update = SymbolModel.query.filter(
            SymbolModel.id == args["symbol_id"]
        ).first()

        if symbol_to_update is None:
            raise AppException(msg="El symbol con id {0} no se puede actualizar por que no se encuentra en la base de datos".format(args["symbol_id"]))

        #update if no exception
        symbol_to_update.fec_audit = datetime.now()
        symbol_to_update.name = args["symbol_name"]
        symbol_to_update.exchange = args["exchange"]
        symbol_to_update.asset_type = args["asset_type"]

    def __is_new(self,args={}):
        if args["symbol_id"] in ["","#","0",None,0]:
            return True
        else:
            return False

    def __val_save(self, args={}):
        errors = []
        if "symbol_id" not in args:
            errors.append("El paámetro 'symbol_id' no se ha enviado")

        if "symbol" not in args:
            errors.append("El parámetro 'symbol' no se ha enviado")

        if "symbol_name" not in args:
            errors.append("El parámetro 'symbol_name' no se ha enviado" )

        if "region" not in args:
            errors.append("El parámetro 'region' no se ha enviado")

        if "exchange" not in args:
            errors.append("El parámetro 'exchange' no se ha enviado")
        
        if "asset_type" not in args:
            errors.append("El parámetro 'asset_type' no se ha enviado")

        if len(errors) > 0:
            raise AppException(msg="Se ha encontrado errores al procesa la petición", errors=errors)

    def __collect(self, args={}):        
        symbol_obj = SymbolModel(
            id=None,
            symbol=args["symbol"],
            name=args["symbol_name"],
            region=args["region"],            
            exchange=args["exchange"],
            asset_type=args["asset_type"],
            fec_registro=date.today(),
            fec_audit=datetime.now()
        )
        return symbol_obj

class SymbolFinder:
    def __init__(self):
        pass

    def get_list(self, args={}):
        data = SymbolModel.query.order_by(
            SymbolModel.fec_audit.desc(),
            SymbolModel.symbol.asc()
        ).limit(100).all()
        return Response().from_raw_data(data)

    def buscar_por_texto(self, args={}):
        texto = "%{0}%".format(args["texto"])
        data = SymbolModel.query.filter(
            SymbolModel.symbol.ilike(texto)
        ).order_by(
            SymbolModel.fec_audit.desc(),
            SymbolModel.symbol.asc()
        ).limit(100).all()
        return Response().from_raw_data(data)

    def get_datos_symbol(self, args={}):
        try:
            data = {
                "asset_type":"",
                "name":""
            }

            if "symbol" not in args:
                raise AppException(msg="El parámetro 'symbol' no ha sido enviado")

            symbol = args["symbol"]

            datos = SymbolModel.query.filter(
                SymbolModel.symbol == symbol
            ).first()    

            if datos is not None:
                data["asset_type"] = datos.asset_type
                data["name"] = datos.name
                data["symbol"] = datos.symbol
            
            #si no hay respuesta buscamos en los contratos
            if datos is None:
                datos = OptionContract.query.filter(
                    OptionContract.symbol == symbol
                ).first()

                if datos is not None:
                    data["asset_type"] = "option contract"
                    data["name"] = datos.description
                    data["symbol"] = datos.symbol

            return Response().from_raw_data(data)
        except Exception as e:
            return Response().from_exception(e)

class DataLoader:
    def __init__(self):        
        bridges = {
            "IEXCLOUD":IEXCloud_Bridge            
        }
        self.bridge = bridges["IEXCLOUD"]()

    def do(self, args={}):
        try:
            tipos = []
            if "tipos" in args:
                tipos = args["tipos"]

            self.bridge.load(tipos)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

class IEXCloud_Bridge:
    asset_a_iex_equiv = {
        "equity":"cs",
        "etf":"et"
    }

    iex_a_asset_equiv = {
        "cs":"equity",
        "et":"etf"
    }

    def __init__(self):
        self.tipos = []
        self.fec_audit = None

    def load(self, tipos=[]):                
        self.tipos = tipos
        self.tipos_iex = self.__obt_tipos_iex_permitidos()
        self.fec_audit = datetime.now()        
        data = self.__symbols()
        self.__save(data)

    def __obt_tipos_iex_permitidos(self):    
        resp = []
        for tipo in self.tipos:
            if tipo in self.asset_a_iex_equiv:
                resp.append(self.asset_a_iex_equiv[tipo])
        return resp


    def __save(self, data=[], tipos=[]):
        for elem in data:
            if elem["type"] in self.tipos_iex:
                self.__single_save(elem)

    def __save_etf(self, data=[]):
        for elem in data:
            print(elem)

    def __single_save(self, elem={}):
        tipo_activo = self.iex_a_asset_equiv[elem["type"]]

        #logger.register(elem)
        symbol = SymbolModel(
            symbol=elem["symbol"],
            name=elem["name"],
            region=elem["region"],
            exchange=elem["exchange"],
            asset_type=tipo_activo,
            fec_registro=date.today(),
            fec_audit=self.fec_audit
        )
        db.session.add(symbol)

    def __symbols(self, params={}):
        api_market = iexcloud()
        data = api_market.symbols()
        return data

    def __etf_symbols(self, params={}):
        api_market = iexcloud()
        data = api_market.etf_symbols()
        return data
