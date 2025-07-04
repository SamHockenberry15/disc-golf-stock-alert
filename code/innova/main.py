from util.email_sender import EmailSender
from util.file_retriever import FileRetriever
from util.constants import INNOVA
from repo.disc_golf_stock_repository import DiscGolfStockRepository

if __name__ == '__main__':
    # Download Latest File to Local
    print("Download Latest Innova File...")
    innova_file_retriever = FileRetriever(INNOVA)
    innova_data = innova_file_retriever.retrieve_data()

    # Add new rows to sqlite db
    print("Insert new data to database...")
    repo = DiscGolfStockRepository()
    repo.insert_new_stock(innova_data)


    #Get both sets of data
    todays_data = repo.get_todays_stock()
    yesterdays_data = repo.get_yesterdays_stock()


    #calculate email contents... should be moved to an aggregation class
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


    #send comms
    print("Send comms...")
    email = EmailSender()
    email.send_email(existing_products_now_in_stock_final.to_html(index=False),
                     new_products_in_stock_final.to_html(index=False),
                     existing_products_now_out_stock_final.to_html(index=False))

    #remove original file
    innova_file_retriever.delete_file()
