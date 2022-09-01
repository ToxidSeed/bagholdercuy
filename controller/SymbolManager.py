from distutils.log import error
from app import db
import inspect
from datetime import datetime, date

from model.StockSymbol import StockSymbol as SymbolModel
from model.OptionContract import OptionContractModel

from common.AppException import AppException
from common.Response import Response
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

            if "symbol" not in args:
                raise AppException(msg="El parámetro 'symbol' no ha sido enviado")

            symbol = args["symbol"]

            stock = SymbolModel.query.filter(
                SymbolModel.symbol == symbol
            ).first()    

            if stock is not None:
                rsp = {
                    "stock":stock
                }
                return Response().from_raw_data(rsp)

            contrato = OptionContractModel.query.filter(
                OptionContractModel.symbol == symbol
            ).first() 

            if contrato is not None:
                rsp = {
                    "contrato":contrato
                }
                return Response().from_raw_data(rsp)
            
            return Response(msg="No se ha recuperado información para el symbol {0}".format(symbol))
        except Exception as e:
            return Response().from_exception(e)

class DataLoader:
    def __init__(self):        
        pass

    def do(self, args={}):
        try:
            list_symbols = self.__get_api_symbols()
            self._procesar(list_symbols)
            db.session.commit()
            return Response(msg="Se ha realizado la carga de symbols correctamente")
        except Exception as e:
            db.session.rollback()
            raise e    

    def __get_api_symbols(self):
        api_market = iexcloud()
        data = api_market.symbols()
        return data

    def _procesar(self, list_symbol=[]):
        for symbol in list_symbol:
            self._procesar_elemento(symbol)

    def _existe_symbol(self, symbol=""):
        symbolbd = SymbolModel.query.filter(
            SymbolModel.symbol == symbol
        ).first()

        if symbolbd is not None:
            return True
        else:
            return False

    def _procesar_elemento(self, elem=None):
        symbol = elem.get("symbol")
        if self._existe_symbol(symbol)==True:
            return

        newsymbol = SymbolModel(
            symbol=symbol,
            name=elem.get("name"),
            region=elem.get("region"),
            exchange=elem.get("exchange"),            
            fec_registro=date.today(),
            fec_audit=datetime.now(),
            moneda_id=elem.get("currency")
        )
        db.session.add(newsymbol)

