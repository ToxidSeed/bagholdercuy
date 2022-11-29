
import os, configparser
app_path = os.path.dirname(__file__)
app_ini_file_path = os.path.join(app_path,"config/app.ini")

def read_config():
    config = configparser.ConfigParser()
    config.read(app_ini_file_path)
    return config
    
config = read_config()



