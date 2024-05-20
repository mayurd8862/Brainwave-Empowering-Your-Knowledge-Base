import os
import math
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

import streamlit as st

# mail_app_pwd = st.secrets.mail_app_password

digits = "0123456789"
OTP = ""

for i in range (6):
    OTP += digits[math.floor(random.random()*10)]
    
# Construct the email message with a subject
subject = "Your OTP Verification Code"

message = f"""
🚀 Thank you for choosing Brainwave as your ultimate companion for project management and data interaction.

Your OTP Code: {OTP}
"""

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
sender_email = "ironmantony8862@gmail.com"
receiver_email = input("Enter your email: ")
# receiver_email = "mayurdabade1103@gmail.com"
s.login(sender_email, st.secrets.mail_pwd)


msg = MIMEMultipart()
# msg['From'] = Header(sender_email, 'utf-8')
# msg['To'] = Header(receiver_email, 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')
msg.attach(MIMEText(message, 'plain', 'utf-8'))

s.sendmail(sender_email,receiver_email,msg.as_string())

# sender_email, receiver_email, msg.as_string()

a = input("Enter your OTP >>: ")
if a == OTP:
    print("Verified")
else:
    print("Please Check your OTP again")




