import logging

enable=True

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
    enable=True