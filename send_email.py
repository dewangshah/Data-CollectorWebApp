from email.mime.text import MIMEText
import smtplib

def send_email(email,height,average_height, count):
    from_email="dbs20381613@gmail.com"
    from_password="xyz123"
    to_email=email#User entered email value

    subject="Height Data"
    message="Hey there, your height is <strong>%s</strong>. <br>Average height of all is <strong>%s</strong>, out of <strong>%s</strong> users. <br>Thanks!" % (height, average_height, count)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To'] =to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
