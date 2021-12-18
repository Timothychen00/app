import os
import smtplib
import imghdr
from email.message import EmailMessage
import dotenv
dotenv.load_dotenv()

EMAIL_ADDRESS = os.environ.get('HOST')
EMAIL_PASSWORD = os.environ.get('PASS')

contacts = ['timothychenpc@gmail.com', 'timothychenpc@gmail.com']

msg = EmailMessage()
msg['Subject'] = 'Check out Bronx as a puppy!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'timothychenpc@gmail.com'

msg.set_content('This is a plain text email')

msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <table style='width:100%;text-align: center;'>
            <tr>
                <td style='width:100px'></td ><td style='width:250px;background-color:SlateGray;'><img src='https://flaskwebb.azurewebsites.net/static/logo-nb.ico' style='height:40px;'></img><h3 style='margin-bottom:5px;color:white'>創造娛樂工作室</h3></td><td style='width:100px'></td>
            </tr>
            <tr>
                <td style='width:100px'></td><td style='width:200px;'></td><td style='width:100px'></td>
            </tr>
            <tr>
                <td style='width:100px'></td><td style='width:200px;'></td><td style='width:100px'></td>
            </tr>
        </table>
    </body>
</html>
""", subtype='html')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)