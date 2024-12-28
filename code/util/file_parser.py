from util_functions import UtilFunctions
import pandas as pd
import constants

class FileParser:

    @staticmethod
    def parse_innova_file():
        file = pd.read_excel("../../data/"+UtilFunctions.today_year_month_day()+"-"+constants.INNOVA+".xlsx")
        print(file.iloc[16::,8:14])
        #for discs only, filter by FlightNumber Column
        # Innova weight classes: 140-150, 151-159, 160-164, 165-169, 170-172, 173-175
        return