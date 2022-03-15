from sqlalchemy import inspect

class Transformer:
    def __init__(self, input_data=None):
        self.input_data = input_data

    def model_to_dict(self):
        return {c.key: str(getattr(self.input_data, c.key)) for c in inspect(self.input_data).mapper.column_attrs}

    def to_parseable_json_dict(self, formats={}):
        for colname, value in self.input_data.items():
            if value.__class__.__name__ == "Decimal":
                self.input_data[colname] = float(value)
            
        if len(formats) > 0:
            for colname, fmt in formats.items():
                self.input_data[colname+"_fmt"] = fmt.format(self.input_data[colname])
            
        return self.input_data
