from helper.Response import Response

class StatusMessage:
    def __init__(self):
        self.success=True
        self.message=""
        self.data={}

    def error(self,message="",data={}):
        self.success=False
        self.message = message
        self.data = data
        return self

    def success(self, message="", data={}):
        self.success=True
        self.message = message
        self.data = data
        return self

    def make_response(self):
        return Response(success=self.success, msg=self.message, extradata=self.data).get()
