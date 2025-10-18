# -*- coding: utf-8 -*-

"""
descr: 查询impala所有字段信息
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: impala_chema_execute.py
"""

from datetime import datetime
from impala.dbapi import connect
import getpass
import pandas as pd


if __name__ == '__main__':
    host = '10.53.0.71'
    port = 21050
    user = 'root'
    password = ''
    database = 'bi_ods'

    conn = connect(host=host, port=port, user=user, password=password, database=database)
    cursor = conn.cursor()

    cursor.execute('show databases')
    database_list = cursor.fetchall()

    schemas = []

    for database in database_list:
        if database[0] == "bi_ods":
            cursor.execute(f'use {database[0]}')
            cursor.execute('show tables')
            tables = cursor.fetchall()

            for table in tables:
                # print(table[0])
                cursor.execute(f'DESCRIBE {table[0]}')
                columns_list = cursor.fetchall()

                for columns in columns_list:
                    column_name = columns[0]
                    filed_type = columns[1]
                    comment = columns[2]
                    schema = database[0] + "|" + table[0]  + "|" + columns[0]  + "|" + columns[1]  + "|" + columns[2]
                    print(schema)
                    schemas.append(schema)

        if database[0] == "bi_data":
            cursor.execute(f'use {database[0]}')
            cursor.execute('show tables')
            tables = cursor.fetchall()

            for table in tables:
                # print(table[0])
                cursor.execute(f'DESCRIBE {table[0]}')
                columns_list = cursor.fetchall()

                for columns in columns_list:
                    column_name = columns[0]
                    filed_type = columns[1]
                    comment = columns[2]
                    schema = database[0] + "|" + table[0]  + "|" + columns[0]  + "|" + columns[1]  + "|" + columns[2]
                    print(schema)
                    schemas.append(schema)

        if database[0] == "bi_ads":
            cursor.execute(f'use {database[0]}')
            cursor.execute('show tables')
            tables = cursor.fetchall()

            for table in tables:
                # print(table[0])
                cursor.execute(f'DESCRIBE {table[0]}')
                columns_list = cursor.fetchall()

                for columns in columns_list:
                    column_name = columns[0]
                    filed_type = columns[1]
                    comment = columns[2]
                    schema = database[0] + "|" + table[0]  + "|" + columns[0]  + "|" + columns[1]  + "|" + columns[2]
                    print(schema)
                    schemas.append(schema)

    cursor.close()
    conn.close()

    arrays = [s.split('|') for s in schemas]
    df = pd.DataFrame(arrays)
    df.columns = ['database', 'table', 'column_name', 'filed_type', 'comment']
    df.to_csv('impala_schema.csv', index=False)



