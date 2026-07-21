import mysql.connector
import json
import os

def __connect():    
    
    return mysql.connector.connect(user=os.getenv("BAGHOLDER_MYSQL_USERNAME"),
                                    password=os.getenv("BAGHOLDER_MYSQL_PASSWORD"),
                                    host=os.getenv('BAGHOLDER_MYSQL_HOST'),
                                    database=os.getenv('BAGHOLDER_MYSQL_DATABASE'))

def execute_query(stmt, params=None, show_last_executed=False):
    stmt_str = _get_query(stmt)
    cnx = __connect()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(stmt_str, params)

    if show_last_executed:
        print(cursor._executed)

    data = cursor.fetchall()
    cursor.close()
    cnx.close()
    return data

def _get_query(stmt_file_name):
    querys_path = './model/scripts/'
    with open(querys_path+stmt_file_name+'.sql', 'r') as myfile:
        query_str = myfile.read()
        return query_str
