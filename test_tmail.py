from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import smtplib
load_dotenv()
def send_email():
    html="""
<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    </head>
    <body>
        <table stye=\'width:200px\'>
            <tr>
                <td>123</td><td>123</td>
            </tr>
            <tr>
                <td>345</td><td>345</td>
            </tr>
        </table>
    </body>
</html>
    """
    
    
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "sdgjhfgjsh"  #郵件標題
    content["from"] = os.getenv("HOST",'123123123123')  #寄件者  os.environ['HOST_EMAIL']
    content["to"] = os.getenv("HOST",'123123123123') #收件者
    content.attach(MIMEText(html,'html'))  #郵件內容
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("timothychenpc@gmail.com", "")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
send_email()