from sqlalchemy import inspect
from datetime import datetime

def to_dict(element, clean=True):
    output = None
    if type(element).__name__ == "Row":
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

    if len(formats) > 0:
        for colname, fmt in formats.items():
            element[colname+"_fmt"] = fmt.format(element[colname])
        
    return element

def process_list(inlist=[]):
    outlist = []
    for elem in inlist:
        outelem = to_dict(elem)
        outlist.append(outelem)
    return outlist