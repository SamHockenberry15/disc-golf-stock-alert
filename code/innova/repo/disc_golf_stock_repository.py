import os
import sqlite3
from datetime import date, timedelta

import pandas
from pandas import DataFrame

from dotenv import load_dotenv


class DiscGolfStockRepository:

    def __init__(self):
        load_dotenv()
        self.sqliteConnection = sqlite3.connect(os.getenv("DB_FILE_LOCATION"))
        self.cursor = self.sqliteConnection.cursor()


    def insert_new_stock(self, dataframe: DataFrame):
        dataframe.to_sql('Product', self.sqliteConnection, if_exists='append', index=False)

    def get_todays_stock(self):
        today = date.today().strftime('%Y%m%d')
        return pandas.read_sql('SELECT * FROM Product where Created_Timestamp=?', con=self.sqliteConnection, params=(today,))

    def get_yesterdays_stock(self):
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y%m%d')
        return pandas.read_sql('SELECT * FROM Product where Created_Timestamp=?', con=self.sqliteConnection, params=(yesterday,))