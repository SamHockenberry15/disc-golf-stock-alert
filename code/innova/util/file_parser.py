from code.innova.util.constants import INNOVA_DISC_PROCDUCT_NUMBER_END, INNOVA_BLACK_LIST_STOCK, INNOVA
from code.innova.util.util_functions import UtilFunctions
import pandas as pd
import datetime

class FileParser:

    @staticmethod
    def parse_innova_file():
        file = pd.read_excel("../" + UtilFunctions.today_year_month_day() +"-" + INNOVA + ".xlsx")
        innova_data = file.iloc[:,[2,7,8,9]]
        innova_data = innova_data.set_axis(['Product_Number', 'Current_In_Stock', 'Product_Name', 'Flight_Numbers'], axis=1)

        # Filter the Current Data for only the discs we want
        innova_data = innova_data[innova_data['Product_Number'].notnull()]
        innova_data = innova_data[~innova_data['Product_Number'].isin(INNOVA_BLACK_LIST_STOCK)]
        innova_data = innova_data[innova_data['Product_Number'] < INNOVA_DISC_PROCDUCT_NUMBER_END]
        innova_data = innova_data[innova_data['Current_In_Stock'].notnull() & ~innova_data['Current_In_Stock'].isin(['Ordered'])]

        # Add two new columns for metadata
        innova_data['Product_Brand'] = "Innova Champion Discs"
        innova_data['Created_Timestamp'] = datetime.datetime.now().strftime('%Y%m%d')

        # Reorder columns
        innova_data = innova_data[['Product_Number','Product_Brand', 'Product_Name', 'Flight_Numbers', 'Current_In_Stock', 'Created_Timestamp']]

        # Change datatypes
        innova_data['Current_In_Stock'] = innova_data['Current_In_Stock'] != 'out'
        innova_data['Product_Number'] = innova_data['Product_Number'].astype(int)
        innova_data['Current_In_Stock'] = innova_data['Current_In_Stock'].astype(bool)
        innova_data['Current_In_Stock'] = innova_data['Current_In_Stock'].astype(str)

        # Debug
        # innova_data.to_csv("tempInnova.csv", index=False)
        # print(innova_data.to_string())

        return innova_data
