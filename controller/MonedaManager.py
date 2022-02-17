from re import M
from common.AppException import AppException
from common.Response import Response
from model.MonedaModel import MonedaModel
from datetime import date
from app import db
from sqlalchemy import func


class MonedaManager:
    def __init__(self):
        self.moneda = None

    def save(self, args={}):
        try:
            self.__val_save(args)
            self.moneda = self.__collect(args)
            
            if self.__is_new():    
                self.__insert()
            else:
                self.__update()

            db.session.commit()
            return Response(msg="Se ha guardado correctamente la moneda").get()
        except AppException as e:            
            return Response().from_exception(e)

    def __is_new(self):
        if self.moneda.moneda_id not in ["","0",0]:    
            return False
        else:
            return True

    def __collect(self, args={}):
        moneda = MonedaModel(
            moneda_id = args["moneda_id"],
            symbol = args["symbol"]
        )
        
        return moneda

    def __val_save(self, args={}):
        errors = []
        if "symbol" not in args:
            errors.append("El parámetro 'symbol' no ha sido enviado")        
    
        if "moneda_id" not in args:
            errors.append("El parámetro 'moneda_id' no ha sido enviado")        
        
        if len(errors) > 0:
            raise AppException(msg="se han encontrado errores de validación", errors=errors)

    def __insert(self):
        moneda_found = self.__find_moneda(self.moneda.symbol)
        if moneda_found is not None:
            raise AppException(msg="El symbol {0} que se está intentando registrar ya existe".format(self.moneda.symbol))        

        self.moneda.moneda_id = None
        self.moneda.fec_registro = date.today()
        db.session.add(self.moneda)

    def __find_moneda(self, symbol=""):
        moneda_found = MonedaModel.query.filter(
            MonedaModel.symbol == symbol
        ).first()

        return moneda_found

    def __find_moneda_by_id(self, id=None):
        moneda_found = MonedaModel.query.filter(
            MonedaModel.moneda_id == id
        ).first()
        return moneda_found

    def __update(self):
        moneda_found = self.__find_moneda_by_id(self.moneda.moneda_id)
        if moneda_found is None:
            raise AppException(msg="La moneda con id {0} que se está intentando actualizar no existe".format(self.moneda.moneda_id))
        
        #Si es diferente de None
        if moneda_found.moneda_id != self.moneda.moneda_id:
            raise AppException(msg="El symbol {0} que se está intentando actualizar ya existe registrada para la moneda con id: {1}".format(self.moneda.symbol, moneda_found.moneda_id))

        #actualizar
        moneda_found.symbol = self.moneda.symbol

    def get_list(self, args={}):
        search_text = args["search_text"]
        import logging

        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        records = MonedaModel.query.filter(
            func.concat(MonedaModel.symbol,'').ilike("%{0}%".format(search_text))
        ).all()

        return Response().from_raw_data(records)
