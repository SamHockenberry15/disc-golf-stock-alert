import datetime

class UtilFunctions:

    @staticmethod
    def today_year_month_day():
        return datetime.date.today().strftime("%Y%m%d")