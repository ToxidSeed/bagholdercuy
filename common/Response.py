import traceback, sys
from sqlalchemy import inspect
from common.AppException import AppException
#from common.Transformer import Transformer
import common.Converter as Converter
from common.Formatter import Formatter
from flask import jsonify
import json




class Response:
    def __init__(self,success=True, code=0, data=None, msg="", raw_data=None, formatter=None, extradata={},errors=[], stacktrace=None):
        self.answer = {
            "success":success,
            "code":code,
            "data":data,            
            "message":msg,
            "expired":False,
            "extradata":extradata,
            "errors":errors,
            "stacktrace":stacktrace
        }
        self.raw_data = raw_data
        self.formatter = formatter
        self.formats = {}

    def elem(self, key="",element=None):
        if self.answer["data"] is None:
            self.answer["data"]={}

        self.answer["data"][key]=element
        
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
        elif type(exception).__name__ == "ExpiredSignatureError":
            self.answer["success"] = False
            self.answer["message"] = "El acceso del usuario ha expirado, volver a conectarse"
            self.answer["expired"] = True
        else:        
            errortype = type(exception).__name__
            self.answer["success"] = False
            self.answer["message"] = "Error no controlado, {0}, msg: {1}".format(errortype,exception)
            self.answer["stacktrace"] = traceback.format_tb(sys.exc_info()[2])        
        return self.answer

    def add_extradata(self, key, value):
        self.answer["extradata"][key] = value
    
    def get(self):
        if self.raw_data is not None:
            self.__process()
        return self.answer

    def get_answer(self):
        return self.answer
    
    def __process(self):
        #Si se ingresa un formateador 
        self.answer["data"] = Formatter(custom=self.formats).format(indata=self.raw_data)
