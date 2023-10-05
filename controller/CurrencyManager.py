from distutils.log import error
from re import M
from common.AppException import AppException
from common.Response import Response
from controller.base import Base
#from model.CurrencyModel import CurrencyModel
from model.MonedaModel import MonedaModel
from model.MonedaParModel import MonedaParModel
from model.bussiness.moneda_par_handler import MonedaParHandler 
from datetime import date, datetime
from app import db
from sqlalchemy import func


class CurrencyManager(Base):
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

            """
            CurrencyPair(
                add_list=args["pairs_to_add"],
                remove_list = args["pairs_to_remove"]
            ).process_pairs()
            """
            extradata = {
                "moneda_id":self.currency.moneda_id
            }

            db.session.commit()
            return Response(msg="Se ha guardado correctamente la moneda",extradata=extradata).get()
        except AppException as e:            
            return Response().from_exception(e)

    def __is_new(self):
        if self.currency.moneda_id is None:
            return True
        else:
            return False

    def __collect(self, args={}):
        moneda_id = args["moneda_id"]
        if moneda_id in ["#","","0",0]:
            moneda_id = None        

        moneda = MonedaModel(
            moneda_id = moneda_id.upper(),
            codigo_iso = args["codigo_iso"].upper(),
            simbolo = args["simbolo"],
            nombre = args["nombre"],
            descripcion = args["descripcion"]
        )
        
        return moneda

    def __val_save(self, args={}):
        errors = []
        if "moneda_id" not in args:
            errors.append("El parámetro 'moneda_id' no ha sido enviado")

        if "simbolo" not in args:
            errors.append("El parámetro 'simbolo' no ha sido enviado")

        if "codigo_iso" not in args:
            errors.append("El parámetro 'codigo_iso' no ha sido enviado")        

        if "nombre" not in args:
            errors.append("El parámetro 'nombre' no ha sido enviado")

        if "descripcion" not in args:
            errors.append("El parámetro 'descripcion' no ha sido enviado")

        """
        if "pairs_to_add" not in args:
            errors.append("El parámetro 'pairs_to_add' no ha sido enviado")

        if "pairs_to_remove" not in args:
            errors.append("El parámetro 'pairs_to_remove' no ha sido enviado")
        """

        if len(errors) > 0:
            raise AppException(msg="se han encontrado errores de validación", errors=errors)

    def __insert(self):
        moneda = self.__find_currency(self.currency.codigo_iso)
        if moneda is not None:
            raise AppException(msg="El symbol {0} que se está intentando registrar ya existe".format(self.currency.codigo_iso))        

        self.currency.moneda_id = self.currency.codigo_iso
        self.currency.fec_registro = date.today()
        self.currency.fec_audit = datetime.now()
        db.session.add(self.currency)

    def __find_currency(self, symbol=""):
        moneda = MonedaModel.query.filter(
            MonedaModel.moneda_id == symbol
        ).first()

        return moneda

    def __find_currency_by_id(self, id=None):
        moneda = MonedaModel.query.filter(
            CurrencyModel.moneda_id == id
        ).first()
        return moneda

    def __update(self):
        moneda = self.__find_currency_by_id(self.currency.moneda_id)
        if moneda is None:
            raise AppException(msg="La moneda con id {0} que se está intentando actualizar no existe".format(self.currency.moneda_id))
        
        #Si es diferente de None
        if moneda.moneda_id != self.currency.moneda_id:
            raise AppException(msg="El symbol {0} que se está intentando actualizar ya existe registrada para la moneda con id: {1}".format(self.currency.codigo_iso, moneda.moneda_id))

        #actualizar
        #moneda.moneda_id = self.currency.moneda
        moneda.nombre = self.currency.nombre
        moneda.descripcion = self.currency.descripcion
        moneda.simbolo = self.currency.simbolo

    def get_list(self, args={}):
        search_text = args["search_text"]

        records = MonedaModel.query.filter(
            func.concat(MonedaModel.codigo_iso,MonedaModel.nombre).ilike("%{0}%".format(search_text))
        ).all()

        return Response().from_raw_data(records)

class CurrencyFinder:
    def __init__(self):
        pass

    def get_list(self,args={}):
        data = MonedaModel.query.all()
        return Response().from_raw_data(data)

    def get_data(self, args={}):
        if "moneda_id" not in args:
            raise AppException(msg="No se ha enviado el parámetro 'moneda_id'")

        moneda_id = args["moneda_id"]
        data = MonedaModel.query.filter_by(moneda_id=moneda_id).first()

        if data is None:
            raise AppException(msg="No se ha logrado recuperar los datos de la moneda para 'moneda_id='{0}".format(moneda_id))

        return Response().from_raw_data(data)

class ParFinder:
    def __init__(self):
        pass

    def get_list_x_mon(self, args={}):
        try:
            if "moneda_id" not in args:
                raise AppException("No se ha enviado 'moneda_id'")

            moneda_id = args["moneda_id"]
            pares = MonedaParModel.query.filter(
                MonedaParModel.mon_base_id == moneda_id
            ).all()

            return Response().from_raw_data(pares)
        except Exception as e:
            raise AppException().from_exception(e)

class MonedaParAddController:   
    def __init__(self):
        pass

    def add(self,args={}):
        try:
            self._val(args)
            par = self._collect(args)
            MonedaParHandler().add(par)                            
            db.session.commit()       
            return Response(msg="El par se ha agregado correctamente")
        except Exception as e:
            return Response().from_exception(e)

    def _val(self, args={}):
        errors = []
        if "base" not in args:
            errors.append("No se ha enviado el parámetro 'base'")

        if "ref" not in args:
            errors.append("No se ha enviado 'ref'")

        if "operacion" not in args:
            errors.append("No se ha enviado 'operacion'")
                
        return errors

    def _collect(self, args={}):
        base = args["base"]
        ref = args["ref"]

        par = MonedaParModel(
            mon_base_id = base,
            mon_ref_id = ref,
            nombre = "{0}/{1}".format(base, ref),
            operacion = args["operacion"],            
        )
        return par

class xxx:

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

    def __remove_pair(self, pair:MonedaParModel=None):
        pair.ind_activo = "N"
        pair.fch_audit = datetime.now()

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

    def __reactivate(self, pair:MonedaParModel =None):
        pair.fec_audit = datetime.now()
        pair.ind_activo = "S"

    def __find_pair_by_id(self, id=None):
        pair_found = MonedaParModel.query.filter(
            MonedaParModel.par_id == id 
        ).first()
        return pair_found

    def __find_pair(self, base="", ref=""):
        pair_found = MonedaParModel.query.filter(
            MonedaParModel.mon_base_id == base,
            MonedaParModel.mon_ref_id == ref
        ).first()
    
        return pair_found
            
    def __val_pairs_entry(self, pair={}):
        errors = []
        if "base" not in pair:
            errors.append("No se ha enviado el parámetro 'base'")

        if "ref" not in pair:
            errors.append("Add pairs: No se ha enviado 'ref'")
        else:
            currency_ref_symbol = pair["ref"]
            currency = CurrencyModel.query.filter(
                CurrencyModel.currency_symbol == currency_ref_symbol
            ).first()

            if currency is None:
                errors.append("Add pairs: La moneda de referencia {0} no existe en la base de datos".format(currency_ref_symbol))

        return errors



    
        