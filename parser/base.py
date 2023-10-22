from common.AppException import AppException

from datetime import datetime, date
class BaseParser:
    def __init__(self, args={}):
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
    
    def parse_boolean(param):
        if param in [None, "", "false", "False", False]:
            return False
        else:
            return True
    
    def parse_orden_resultados(param):
        if param in [None,""]:
            return None
        
        if param not in ["asc","desc"]:
            raise AppException(msg="orden_resultados solo puede ser asc o desc")