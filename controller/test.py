from common.api.iexcloud import iexcloud
from common.Response import Response

class IEXCLOUDTester:
    def __init__(self):
        pass

    def get_quote(self, args={}):
        api = iexcloud()
        results = api.get_quote(args)
        return Response().from_raw_data(results)
        