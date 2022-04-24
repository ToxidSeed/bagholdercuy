import traceback, sys
from sqlalchemy import inspect
from common.AppException import AppException
from common.Transformer import Transformer
import common.Converter as Converter
from flask import jsonify
import json


class Response:
    def __init__(self,success=True, code=0, data=None, msg="", raw_data=None, formatter=None, extradata={},errors=[], stacktrace=None):
        self.answer = {
            "success":success,
            "code":code,
            "data":data,            
            "message":msg,
            "extradata":extradata,
            "errors":errors,
            "stacktrace":stacktrace
        }
        self.raw_data = raw_data
        self.formatter = formatter
        self.formats = {}

    def from_raw_data(self, rawdata=None, formats={}):
        self.formats = formats
        if rawdata is not None:
            self.raw_data = rawdata
            self.__process()
        return self.answer

    def from_error(self,error=None):
        self.answer["errors"] = error.errors
        self.answer["message"] = error.msg
        return self.answer

    def from_errors_list(self, errors=[]):
        self.answer["success"] = False
        self.answer["errors"] = errors
        return self.answer        

    def from_exception(self, exception = None):
        if type(exception) is AppException:
            self.answer["success"] = False
            self.answer["message"] = exception.msg
            self.answer["errors"] = exception.errors
            self.answer["stacktrace"] = traceback.format_tb(sys.exc_info()[2])

        else:        
            errortype = type(exception).__name__
            self.answer["success"] = False
            self.answer["message"] = "Error no controlado, tipo:{0}, msg: {1}".format(errortype,exception)
            self.answer["stacktrace"] = traceback.format_tb(sys.exc_info()[2])        

        return self.answer

    def add_extradata(self, key, value):
        self.answer["extradata"][key] = value
    
    def get(self):
        if self.raw_data is not None:
            self.__process()
        return self.answer
    
    def __process(self):
        #Si se ingresa un formateador 
        if self.formatter is not None:
            self.answer["data"] = self.formatter.format(self.raw_data)
        else:             
            if any("Model" == base.__name__ for base in self.raw_data.__class__.__bases__):
                self.answer["data"] = self.__process_model(self.raw_data)

            if type(self.raw_data).__name__ in ["dict"]:
                self.answer["data"] = self.raw_data

            if type(self.raw_data).__name__ in ["list", "ResultProxy","LegacyCursorResult"]:
                self.answer["data"] = self.__process_list()

            if type(self.raw_data).__name__ in ["Row"]:
                self.answer["data"] = self.__process_element(self.raw_data)    

    def __process_model(self, element=None):
        #return {c.key: str(getattr(element, c.key)) for c in inspect(element).mapper.column_attrs}
        element_dict = element.__dict__
        element_dict.pop('_sa_instance_state')

        element_dict = Converter.to_clean_dict(element=element_dict,formats=self.formats)
        return element_dict

    def __process_list(self):
        data = []
        for element in self.raw_data:
            record = self.__process_element(element)
            data.append(record)
        return data

    def __process_element(self, element=None):
        record = element
        if any("Model" == base.__name__ for base in element.__class__.__bases__):
            record = self.__process_model(element)            
        if element.__class__.__name__ in ['result','LegacyRow', 'Row']:
            """record = Transformer(element._asdict()).to_parseable_json_dict(formats=self.formats)"""
            record = Converter.to_dict(element)
        if element.__class__.__name__ == 'RowProxy':
            record = Transformer(dict(element.items())).to_parseable_json_dict(formats=self.formats)
        if element.__class__.__name__ == 'dict':            
            record = Converter.to_clean_dict(element=element,formats=self.formats)
        
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
