import pandas as pd

from email_sender import EmailSender
from file_retriever import FileRetriever
from constants import INNOVA
from disc_golf_stock_repository import DiscGolfStockRepository

if __name__ == '__main__':
    # Download Latest File to Local
    innova_data = FileRetriever(INNOVA).retrieve_data()

    # Add new rows to sqlite db
    repo = DiscGolfStockRepository()
    # repo.insert_new_stock(innova_data)


    #Get both sets of data
    todays_data = repo.get_todays_stock()
    yesterdays_data = repo.get_yesterdays_stock()


    #we need to know what is new in stock, and what has gone out of stock
    existing_products = todays_data.merge(yesterdays_data, how='inner', on='Product_Name')

    existing_products_now_in_stock = existing_products.loc[(existing_products['Current_In_Stock_x'] == 'True') & (existing_products['Current_In_Stock_y'] == 'False')]
    existing_products_now_in_stock_final = existing_products_now_in_stock[['Product_Number_x','Product_Brand_x','Product_Name', 'Flight_Numbers_x']].set_axis(['Product_Number','Product_Brand', 'Product_Name', 'Flight_Numbers'], axis=1)

    existing_products_now_out_stock = existing_products.loc[(existing_products['Current_In_Stock_x'] == 'False') & (existing_products['Current_In_Stock_y'] == 'True')]
    existing_products_now_out_stock_final = existing_products_now_out_stock[
        ['Product_Number_x', 'Product_Brand_x', 'Product_Name', 'Flight_Numbers_x']].set_axis(
        ['Product_Number', 'Product_Brand', 'Product_Name', 'Flight_Numbers'], axis=1)




    new_products = todays_data.merge(yesterdays_data, how='left', on='Product_Name')
    new_products_in_stock = new_products.loc[(new_products['Current_In_Stock_x'] == 'True') & (new_products['Current_In_Stock_y'].isnull())]

    new_products_in_stock_final = new_products_in_stock[
        ['Product_Number_x', 'Product_Brand_x', 'Product_Name', 'Flight_Numbers_x']].set_axis(
        ['Product_Number', 'Product_Brand', 'Product_Name', 'Flight_Numbers'], axis=1)


    email = EmailSender()
    email.send_email(existing_products_now_in_stock_final.to_html(index=False),
                     new_products_in_stock_final.to_html(index=False),
                     existing_products_now_out_stock_final.to_html(index=False))
    # Run query to complete an outer join to see what has changed day-by-day

    # Maybe app can do a 1 day, 7 day, and 30 day comparison
