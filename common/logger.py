import logging

"""enable=True

def register(data=None):   
    try:    
        if enable:
            logging.basicConfig(filename="./log/work.log", filemode="w")        
            logging.warning(data)
    except:
        print("errors")

def stop():
    enable=False

def start():
    enable=True"""

def create_basic_logger():
    handle = "console"
    logging.basicConfig(level=logging.NOTSET)
    return logging.getLogger(handle)

logger = create_basic_logger()
