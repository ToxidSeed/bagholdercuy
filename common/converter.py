from sqlalchemy import inspect
from datetime import datetime, date

def to_bool(item, raise_except=False):
    if item is None:
        return None

    if item in [True, "true","true"]:
        return True

    if item in [False, "false", "False"]:
        return False
    
    if raise_except == True:
        raise AppException(msg="El valor {0} no es un booleando".format(str(item)))
    else:
        return None

def to_dict(element, clean=True):
    output = None
    if type(element).__name__ in ['result','LegacyRow', 'Row']:
        if clean:
            return to_clean_dict(dict(element))
        else:
            return dict(element)        
    
    if any("Model" == base.__name__ for base in element.__class__.__bases__):
        output = element.__dict__
        output.pop('_sa_instance_state')

        #clean output
        if clean:
            output = to_clean_dict(output)

        return output

    return output

@DeprecationWarning
def model_to_dict(model):
    element_dict = model.__dict__
    element_dict.pop('_sa_instance_state')
    return element_dict

def to_clean_dict(element, formats={}):
    for key, value in element.items():
        if value.__class__.__name__ == "Decimal":
            element[key] = float(value)
        if value.__class__.__name__ == "date":
            element[key] = value.isoformat()
        if value.__class__.__name__ == "time":
            element[key] = value.strftime("%H:%M:%S")               

    if len(formats) > 0:
        for colname, fmt in formats.items():
            element[colname+"_fmt"] = fmt.format(element[colname])
        
    return element

def process_list(inlist=[]):
    outlist = []
    for elem in inlist:
        #outelem = to_dict(elem)
        outelem = format(elem)
        outlist.append(outelem)
    return outlist

def format(indata=None):
    if type(indata).__name__ in ["list", "ResultProxy","LegacyCursorResult"]:
        return process_list(inlist=indata)
    if type(indata).__name__ == "date":    
        return indata.isoformat()
    if type(indata).__name__ == "Decimal":
        return float(indata)
    if type(indata).__name__ == "time":
        return indata.strftime("%H:%M:%S")
    if type(indata).__name__ == "dict":
        return format_dict(indata)
    if type(indata).__name__ in ['result','LegacyRow', 'Row']:
        return format_dict(dict(indata))
    if any("Model" == base.__name__ for base in indata.__class__.__bases__):
        output = indata.__dict__
        output.pop('_sa_instance_state')
        return format_dict(output)
    
    return indata

def format_dict(element=None):
    for key, value in element.items():
        element[key] = format(value)                
    return element
