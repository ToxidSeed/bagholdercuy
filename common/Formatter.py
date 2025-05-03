from sqlalchemy import inspect
from datetime import datetime, date

class Formatter:
    def __init__(self, custom={}):
        self.custom = custom
        self.exclude_fields = []

    def process_list(self, inlist=[]):
        outlist = []
        for elem in inlist:
            #outelem = to_dict(elem)
            outelem = self.format(elem)
            outlist.append(outelem)
        return outlist

    def format(self,indata=None):                
        if type(indata).__name__ in ["list", "ResultProxy","LegacyCursorResult"]:
            return self.process_list(inlist=indata)
        if self.is_namedtuple(indata):
            return self.process_namedtuple(indata)
        if type(indata).__name__ == "date":    
            #return indata.isoformat()
            return indata.strftime("%Y-%m-%d")
        if type(indata).__name__ == "Decimal":
            return float(indata)
        if type(indata).__name__ == "time":
            return indata.strftime("%H:%M:%S")
        if type(indata).__name__ == "dict":
            return self.format_dict(indata)
        if type(indata).__name__ in ['result','LegacyRow', 'Row']:
            return self.format_dict(dict(indata))
        if any("Model" == base.__name__ for base in indata.__class__.__bases__):
            output = indata.__dict__
            if "_sa_instance_state" in output:
                output.pop('_sa_instance_state')
            return self.format_dict(output)
        
        return indata

    def is_namedtuple(self, node=None):
        if isinstance(node, tuple) and hasattr(node, "_fields"):
            return True
        else:
            return False

    def process_namedtuple(self, node):
        return node._asdict()

    def format_dict(self, element=None):
        for key, value in element.items():
            element[key] = self.format(value)
    
        element.update(self.get_custom_formats(element))
        return element

    def format_pandas_dataframe(self, df):
        lista_index = list(df.index)

        records = df.to_dict(orient="records")
        for rowindex, elem in enumerate(records, start=0):
            elem["index"] = lista_index[rowindex]

        return records



    def get_custom_formats(self, element=None):
        custom_fields = {}
        for key, value in element.items():
            if key in self.custom:
                custom_fields[key+"_fmt"] = self.custom[key].format(value)

        return custom_fields






