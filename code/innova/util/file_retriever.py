
import urllib.request
import os

from code.innova.util import constants
from code.innova.util.util_functions import UtilFunctions
from code.innova.util.file_parser import FileParser as fp

class FileRetriever:

    innova_filepath = "../" + UtilFunctions.today_year_month_day() +"-" + constants.INNOVA + ".xlsx"

    def __init__(self, discCompany):
        self.discCompany = discCompany


    def retrieve_data(self):
        if self.discCompany == constants.INNOVA:
            if not os.path.exists(self.innova_filepath):
                self.__retrieve_file_for_innova()
            return fp.parse_innova_file()


    def delete_file(self):
        if self.discCompany == constants.INNOVA:
            if os.path.exists(self.innova_filepath):
                os.remove(self.innova_filepath)

    def __retrieve_file_for_innova(self):
        urllib.request.urlretrieve(constants.INNOVA_LINK, self.innova_filepath)