import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

class EmailSender:

    def __init__(self):
        load_dotenv()
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")

    def send_email(self, existing_new_in_stock, new_new_in_stock, existing_out_stock):
        self.smtp.starttls()
        # Authentication
        self.smtp.login(self.api_key, self.api_secret)

        msg = self.get_message(existing_new_in_stock, new_new_in_stock, existing_out_stock)

        # sending the mail
        self.smtp.sendmail(self.api_key, os.getenv('EMAIL_RECIPIENTS').split(','), msg.as_string())
        # terminating the session
        self.smtp.quit()

    def get_message(self, existing_new_in_stock, new_new_in_stock, existing_out_stock):
        # msg = ('NEW In-Stock:\n' + str(new_new_in_stock) + '\n\n\n'
        #        + 'Restocked Products:\n' + existing_new_in_stock + '\n\n\n' +
        #        'Newly Out of Stock Products:\n' + str(existing_out_stock))

        final_msg =("<h3>NEW In-Stock:</h3><br>" + new_new_in_stock + "<br>"+
                    "<h3>Restocked Products:</h3><br>" + existing_new_in_stock + "<br>" +
                    "<h3>Newly Out of Stock Products:</h3><br>" + existing_out_stock + "<br>")

        final_msg = MIMEText(final_msg, 'html')
        msg = MIMEMultipart('alternative')
        msg.attach(final_msg)
        msg['Subject'] = "Daily Disc Golf Stock Alert"
        msg['From'] = self.api_key
        msg['To'] = os.getenv('EMAIL_RECIPIENTS')
        return msg