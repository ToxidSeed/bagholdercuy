from sqlalchemy import inspect
from helper.Transformer import Transformer
from flask import jsonify
import json


class Response:
    def __init__(self,success=True, code=0, data=None, msg="", input_data=None, formatter=None, extradata={}):
        self.answer = {
            "success":success,
            "code":code,
            "data":data,            
            "message":msg,
            "extradata":extradata
        }
        self.input_data = input_data
        self.formatter = formatter

    def add_extradata(self, key, value):
        self.answer["extradata"][key] = value
    
    def get(self):
        if self.input_data is not None:
            self.__process()
        return self.answer
    
    def __process(self):
        #Si se ingresa un formateador 
        if self.formatter is not None:
            self.answer["data"] = self.formatter.format(self.input_data)
        else:             
            if any("Model" == base.__name__ for base in self.input_data.__class__.__bases__):
                self.answer["data"] = self.__process_model(self.input_data)

            if type(self.input_data).__name__ in ["dict"]:
                self.answer["data"] = self.input_data

            if type(self.input_data).__name__ in ["list", "ResultProxy","LegacyCursorResult"]:
                self.answer["data"] = self.__process_list()

            if type(self.input_data).__name__ in ["Row"]:
                self.answer["data"] = self.__process_element(self.input_data)

    def __process_model(self, element=None):
        return {c.key: str(getattr(element, c.key)) for c in inspect(element).mapper.column_attrs}

    def __process_list(self):
        data = []
        for element in self.input_data:
            record = self.__process_element(element)
            data.append(record)
        return data

    def __process_element(self, element=None):
        record = element
        if any("Model" == base.__name__ for base in element.__class__.__bases__):
            record = self.__process_model(element)            
        if element.__class__.__name__ in ['result','LegacyRow', 'Row']:
            record = Transformer(element._asdict()).to_parseable_json_dict()
        if element.__class__.__name__ == 'RowProxy':
            record = Transformer(dict(element.items())).to_parseable_json_dict()            
        return record    
        
class JsonResponse:
    def __init__(self, result_set, formatter=None):
        self.result_set = result_set
        self.formatter = formatter
        self.response_result_set = []

    def make(self, raw=True):        
        if type(self.result_set).__name__ in ["list", "ResultProxy"]:
            self.process_list()

        if any("Model" == base.__name__ for base in self.result_set.__class__.__bases__):
            return self.process_model(self.result_set)

        #Si se ingresa un formateador 
        if self.formatter is not None:
            response_dict = self.formatter.format(self.response_result_set)
        else: 
            response_dict = self.response_result_set

        #De acuerdo a esto se envia o no como un JSON
        if not raw:
            return jsonify(response_dict)        
        else:
            return response_dict

    def process_list(self):
        for element in self.result_set:
            self.process_element(element)

    def process_element(self, element):
        record = element
        if any("Model" == base.__name__ for base in element.__class__.__bases__):
            record = self.process_model(element)            
        if element.__class__.__name__ == 'result':
            record = self.to_parseable_json_dict(element._asdict())            
        if element.__class__.__name__ == 'RowProxy':
            record = self.to_parseable_json_dict(dict(element.items()))

        self.response_result_set.append(record)

    def process_model(self, element):
        record = self.model_to_dict(element)
        return record

    def model_to_dict(self, element):
        return {c.key: str(getattr(element, c.key)) for c in inspect(element).mapper.column_attrs}

    def to_parseable_json_dict(self, raw_dict):
        for key, value in raw_dict.items():
            if value.__class__.__name__ == "Decimal":
                raw_dict[key] = float(value)
        return raw_dict
