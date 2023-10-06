# ！/usr/bin/python3
# coding:utf-8
# sys
import os.path
import pandas as pd

from __init__ import *
from sqlalchemy import create_engine


class ConnectToDB:
    def __init__(self, db_name, path):

        self.db_path = os.path.join(path, f'{db_name}.db')
        self.conn = create_engine(f'sqlite:///{self.db_path}').connect()
        self.db_name = db_name

    def save_to_sql(self, data_dict):
        df = pd.DataFrame({key: [value] for key, value in data_dict.items()})
        df.to_sql(self.db_name, self.conn, index=True, if_exists="append")

    def read_from_sql(self):
        pd.read_sql_table(self.db_name, self.conn)
        return pd
