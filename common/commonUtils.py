import string
import random

def getTempPassword():
    ret = ''
    number_pool=string.digits
    string_pool=string.ascii_lowercase
    for i in range(5):
        ret+=random.choice(string_pool)
        ret+=random.choice(number_pool)

    return ret


#이메일 발송을 위한 것

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

#SMTP접속을 위한 서버 포트
SMTP_SERVER ='smtp.gmail.com'
SMTP_PORT = 465

#보내는 메일
SMTP_USER = 'zzcjs123@gmail.com'
SMTP_PASSWORD = 'chb658458'

#받는사람,제목,내용
def send_email(addr,subject,password):

    content = "변경된 비밀번호는 " +password + " 입니다."

    msg = MIMEMultipart("alternative")

    msg["From"] = SMTP_USER
    msg["To"] = addr
    msg["Subject"] = subject

    contents = content
    text = MIMEText(_text=contents, _charset="utf-8")
    msg.attach(text)

    smtp = smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT)

    smtp.login(SMTP_USER, SMTP_PASSWORD)

    smtp.sendmail(SMTP_USER,addr,msg.as_string())

    smtp.close()