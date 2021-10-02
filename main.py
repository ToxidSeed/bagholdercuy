import sys, json

from app import app
from common.Response import Response
#app.run(debug=False)
try:        
    app.run(debug=False)    
except Exception:
    rsp = json.dumps(Response(msg="Error no controlado del programa", success=False, code=-1).get())
    print(rsp)

    
