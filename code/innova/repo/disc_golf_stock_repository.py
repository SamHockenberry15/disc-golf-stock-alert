import sqlite3
from datetime import date, timedelta

import pandas
from pandas import DataFrame


class DiscGolfStockRepository:

    def __init__(self):
        self.sqliteConnection = sqlite3.connect('C:\\Users\\samho\\Documents\\GIT\\Disc-Golf-Stock-Alert\\data\\DiscGolfStock.db')
        self.cursor = self.sqliteConnection.cursor()


    def insert_new_stock(self, dataframe: DataFrame):
        dataframe.to_sql('Product', self.sqliteConnection, if_exists='append', index=False)

    def get_todays_stock(self):
        today = date.today().strftime('%Y%m%d')
        return pandas.read_sql('SELECT * FROM Product where Created_Timestamp=?', con=self.sqliteConnection, params=(today,))

    def get_yesterdays_stock(self):
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y%m%d')
        return pandas.read_sql('SELECT * FROM Product where Created_Timestamp=?', con=self.sqliteConnection, params=(yesterday,))