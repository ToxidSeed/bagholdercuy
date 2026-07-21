import logging
import mysql.connector
from datetime import datetime
import json
import os

class MySQLHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.table = 'app_logs'
        self.conn = mysql.connector.connect(
            host='localhost',
            user='alone',
            password=os.getenv("BAGHOLDER_MYSQL_PASSWORD"),
            database='bagholdercuy'
        )
        self.cursor = self.conn.cursor()   

    def create_log_record(self, log_data):
        """Convert logging record dict to database record format"""
        return {
            'created': log_data['created'],
            'asctime': datetime.strptime(log_data['asctime'], '%Y-%m-%d %H:%M:%S,%f'),
            'name': log_data['name'],
            'levelname': log_data['levelname'],
            'levelno': log_data['levelno'],
            'message': log_data['message'],
            'pathname': log_data['pathname'],
            'filename': log_data['filename'],
            'module': log_data['module'],
            'lineno': log_data['lineno'],
            'funcName': log_data['funcName'],
            'thread': log_data['thread'],
            'threadName': log_data['threadName'],
            'process': log_data['process'],
            'processName': log_data['processName'],
            'msecs': log_data['msecs'],
            'relativeCreated': log_data['relativeCreated'],
            'exc_info': str(log_data['exc_info']) if log_data['exc_info'] else None,
            'exc_text': log_data['exc_text'],
            'stack_info': log_data['stack_info'],
            'args': json.dumps(log_data['args']),
            'extra_data': json.dumps({})  # Can be populated with additional context
        }     

    def emit(self, record):
        try:
            self.format(record)
            log_entry = self.create_log_record(record.__dict__)
            insert_query = """
            INSERT INTO app_logs (
                created, asctime, name, levelname, levelno, message,
                pathname, filename, module, lineno, funcName,
                thread, threadName, process, processName,
                msecs, relativeCreated, exc_info, exc_text, stack_info, args, extra_data
            ) VALUES (
                %(created)s, %(asctime)s, %(name)s, %(levelname)s, %(levelno)s, %(message)s,
                %(pathname)s, %(filename)s, %(module)s, %(lineno)s, %(funcName)s,
                %(thread)s, %(threadName)s, %(process)s, %(processName)s,
                %(msecs)s, %(relativeCreated)s, %(exc_info)s, %(exc_text)s, %(stack_info)s, 
                %(args)s, %(extra_data)s
            )
            """
            self.cursor.execute(insert_query, log_entry)
            self.conn.commit()
        except Exception as e:
            print(f"Failed to log to MySQL: {e}")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

mysql_handler = MySQLHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
mysql_handler.setFormatter(formatter)

logger.addHandler(mysql_handler)