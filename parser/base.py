from datetime import datetime, date
class BaseParser:
    def __init__(args={}):
        self.args = args

    def parse_id_cuenta(id_cuenta):
        if id_cuenta in [None, ""]:
            return None

        return int(id_cuenta)

    def parse_date(fecha):
        if fecha in [None,""]:
            return None

        return date.fromisoformat(fecha)

    def parse_int(param):
        if param in [None,""]:
            return None

        return int(param)

        
