import smtplib
from email.message import EmailMessage
import streamlit as st
import math, random
 
# function to generate OTP
def generateOTP() :
    digits = "0123456789"
    OTP = ""

    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP
 
# Email parameters
# sender_email = "mayurdabade1103@gmail.com"
# receiver_email = "savitadabade1604@gmail.com"
# password = st.secrets['mail_pwd'] # Your App Password
# subject = "BrainWave password recovery"
# body = f"Verification OTP for password recovery - {generateOTP()}."

def send_otp(sender,receiver, app_password, subject, body):
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(sender, app_password)  # Log in to the server using the App Password
            server.send_message(msg)  # Send the email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# send_otp(sender_email,receiver_email, password, subject, body)