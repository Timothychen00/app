from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
content = MIMEMultipart()  #建立MIMEMultipart物件
content["subject"] = "Learn Code With Mike"  #郵件標題
content["from"] = "timothychenpc@gmail.com"  #寄件者
content["to"] = "timothychenpc@gmail.com" #收件者
content.attach(MIMEText("Demo python send email"))  #郵件內容

import smtplib
with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
    try:
        smtp.ehlo()  # 驗證SMTP伺服器
        smtp.starttls()  # 建立加密傳輸
        smtp.login("timothychenpc@gmail.com", "jsamanwwevgfgbsq")  # 登入寄件者gmail
        smtp.send_message(content)  # 寄送郵件
        print("Complete!")
    except Exception as e:
        print("Error message: ", e)