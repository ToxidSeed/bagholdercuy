from distutils.log import error
from re import M
from common.AppException import AppException
from common.Response import Response
from model.CurrencyModel import CurrencyModel
from datetime import date, datetime
from app import db
from sqlalchemy import func

from model.CurrencyPairModel import CurrencyPairModel


class CurrencyManager:
    def __init__(self):
        self.currency = None

    def save(self, args={}):
        try:
            self.__val_save(args)
            self.currency = self.__collect(args)
            
            if self.__is_new():    
                self.__insert()
            else:
                self.__update()

            CurrencyPair(
                add_list=args["pairs_to_add"],
                remove_list = args["pairs_to_remove"]
            ).process_pairs()

            db.session.commit()
            return Response(msg="Se ha guardado correctamente la moneda").get()
        except AppException as e:            
            return Response().from_exception(e)

    def __is_new(self):
        if self.currency.currency_id is None:
            return True
        else:
            return False

    def __collect(self, args={}):
        currency_id = args["currency_id"]
        if currency_id in ["#","","0",0]:
            currency_id = None
        else:
            currency_id = int(currency_id)            

        currency = CurrencyModel(
            currency_id = currency_id,
            currency_symbol = args["currency_symbol"],
            currency_name = args["currency_name"],
            currency_desc = args["currency_desc"]
        )
        
        return currency

    def __val_save(self, args={}):
        errors = []
        if "currency_id" not in args:
            errors.append("El parámetro 'currency_id' no ha sido enviado")

        if "currency_symbol" not in args:
            errors.append("El parámetro 'currency_symbol' no ha sido enviado")        

        if "currency_name" not in args:
            errors.append("El parámetro 'currency_name' no ha sido enviado")

        if "currency_desc" not in args:
            errors.append("El parámetro 'currency_desc' no ha sido enviado")

        if "pairs_to_add" not in args:
            errors.append("El parámetro 'pairs_to_add' no ha sido enviado")

        if "pairs_to_remove" not in args:
            errors.append("El parámetro 'pairs_to_remove' no ha sido enviado")

        if len(errors) > 0:
            raise AppException(msg="se han encontrado errores de validación", errors=errors)

    def __insert(self):
        currency_found = self.__find_currency(self.currency.currency_symbol)
        if currency_found is not None:
            raise AppException(msg="El symbol {0} que se está intentando registrar ya existe".format(self.currency.currency_symbol))        

        self.currency.currency_id = None
        self.currency.fec_registro = date.today()
        self.currency.fec_audit = datetime.now()
        db.session.add(self.currency)

    def __find_currency(self, symbol=""):
        currency_found = CurrencyModel.query.filter(
            CurrencyModel.currency_symbol == symbol
        ).first()

        return currency_found

    def __find_currency_by_id(self, id=None):
        currency_found = CurrencyModel.query.filter(
            CurrencyModel.currency_id == id
        ).first()
        return currency_found

    def __update(self):
        currency_found = self.__find_currency_by_id(self.currency.currency_id)
        if currency_found is None:
            raise AppException(msg="La moneda con id {0} que se está intentando actualizar no existe".format(self.currency.currency_id))
        
        #Si es diferente de None
        if currency_found.currency_id != self.currency.currency_id:
            raise AppException(msg="El symbol {0} que se está intentando actualizar ya existe registrada para la moneda con id: {1}".format(self.currency.currency_symbol, currency_found.currency_id))

        #actualizar
        currency_found.currency_symbol = self.currency.currency_symbol

    def get_list(self, args={}):
        search_text = args["search_text"]

        records = CurrencyModel.query.filter(
            func.concat(CurrencyModel.currency_symbol,'').ilike("%{0}%".format(search_text))
        ).all()

        return Response().from_raw_data(records)

class CurrencyFinder:
    def __init__(self):
        pass

    def get_list(self,args={}):
        data = CurrencyModel.query.all()
        return Response().from_raw_data(data)

class CurrencyPair:
    def __init__(self, add_list=[], remove_list=[]):
        self.add_list = add_list
        self.remove_list = remove_list

    def process_pairs(self):        
        add_errors = self.__add()
        rm_errors = self.__remove()
        errors = add_errors + rm_errors
        if len(errors):
            raise AppException(msg="Han ocurrido errores al procesar los pares", errors=errors)

    def __remove(self):
        errors = []
        for pair_id in self.remove_list:
            pair_found = self.__find_pair_by_id(id = pair_id)
            if pair_found is None:
                errors.append("El par con par_id={0} no existe en base de datos".format(pair_id))
            else:
                self.__remove_pair(pair_found)
        return errors

    def __remove_pair(self, pair:CurrencyPairModel=None):
        pair.ind_activo = "N"
        pair.fec_audit = datetime.now()

    def __add(self):
        errors = []
        for pair in self.add_list:
            errors = errors + self.__val_pairs_entry(pair)

            #Si no hay errores creamos el objeto y se va agregando
            if len(errors) == 0:
                pair_found = self.__find_pair(
                    pair["base"],
                    pair["ref"]
                )
                if pair_found is not None:
                    self.__reactivate(pair_found)
                else:
                    self.__add_pair(pair)
        return errors    

    def __add_pair(self, pair={}):
        base_symbol = pair["base"]
        ref_symbol = pair["ref"]

        pair_name = "{0}/{1}".format(base_symbol, ref_symbol)
        new_pair = CurrencyPairModel(
            currency_base_symbol = base_symbol,
            currency_ref_symbol = ref_symbol,            
            pair_name = pair_name,
            ind_activo = "S",
            fec_registro = date.today(),
            fec_audit = datetime.now()
        )        

        db.session.add(new_pair)

    def __reactivate(self, pair:CurrencyPairModel =None):
        pair.fec_audit = datetime.now()
        pair.ind_activo = "S"

    def __find_pair_by_id(self, id=None):
        pair_found = CurrencyPairModel.query.filter(
            CurrencyPairModel.currency_pair_id == id 
        ).first()
        return pair_found

    def __find_pair(self, base="", ref=""):
        pair_found = CurrencyPairModel.query.filter(
            CurrencyPairModel.currency_base_symbol == base,
            CurrencyPairModel.currency_ref_symbol == ref
        ).first()
    
        return pair_found
            
    def __val_pairs_entry(self, pair={}):
        errors = []
        if "ref" not in pair:
            errors.append("Add pairs: No se ha enviado 'ref' en alguno de los pares")
        else:
            currency_ref_symbol = pair["ref"]
            currency = CurrencyModel.query.filter(
                CurrencyModel.currency_symbol == currency_ref_symbol
            ).first()

            if currency is None:
                errors.append("Add pairs: La moneda de referencia {0} no existe en la base de datos".format(currency_ref_symbol))

        return errors



    
        