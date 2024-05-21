# import os
# import math
# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.header import Header

# import streamlit as st

# # mail_app_pwd = st.secrets.mail_app_password
# def opt_verify(user_mail):

#     digits = "0123456789"
#     OTP = ""

#     for i in range (6):
#         OTP += digits[math.floor(random.random()*10)]

#     s = smtplib.SMTP('smtp.gmail.com', 587)
#     s.starttls()
#     sender_email = "ironmantony8862@gmail.com"
#     s.login(sender_email, st.secrets.mail_pwd)
        
#     # Construct the email message with a subject
#     subject = "Your OTP Verification Code"

#     message = f"""
#     🚀 Thank you for choosing Brainwave as your ultimate companion for project management and data interaction.

#     Your OTP Code: {OTP}
#     """

#     msg = MIMEMultipart()
#     msg['Subject'] = Header(subject, 'utf-8')
#     msg.attach(MIMEText(message, 'plain', 'utf-8'))

#     s.sendmail(sender_email,user_mail,msg.as_string())

#     return OTP


# @st.experimental_dialog("Cast your vote")
# def verify(mail,otp):
#     st.write(f"Enter OTP send on your mail:")
#     reason = st.text_input("Enter OTP send on your mail:")
#     if st.button("Submit"):
#         st.session_state.otp_info = {"mail": mail, "otp": otp}
#         st.rerun()

# if "otp" not in st.session_state:
#     # st.write("Vote for your favorite")
#     mail = st.text_input("Enter user mail: ")
#     btn = st.button("Register")
#     if btn:
#         otp = opt_verify(mail)
#         verify(mail,otp)



import os
import math
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

import streamlit as st

# Function to generate and send OTP
def opt_verify(user_mail):
    digits = "0123456789"
    OTP = "".join(random.choice(digits) for i in range(6))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    sender_email = "ironmantony8862@gmail.com"
    s.login(sender_email, st.secrets["mail_pwd"])
    
    # Construct the email message with a subject
    subject = "Your OTP Verification Code"

    message = f"""
    🚀 Thank you for choosing Brainwave as your ultimate companion for project management and data interaction.

    Your OTP Code: {OTP}
    """

    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    s.sendmail(sender_email, user_mail, msg.as_string())
    s.quit()

    return OTP

# OTP verification dialog
def verify_otp(mail, generated_otp):
    st.write(f"Enter the OTP sent to {mail}:")
    entered_otp = st.text_input("Enter OTP", type='password')
    if st.button("Submit OTP"):
        if entered_otp == generated_otp:
            st.session_state.verified = True
            st.success("OTP verified successfully!")
        else:
            st.error("Invalid OTP. Please try again.")

# Main application logic
st.title("OTP Verification Example")

if "verified" not in st.session_state:
    st.session_state.verified = False

if not st.session_state.verified:
    mail = st.text_input("Enter your email address:")
    if st.button("Register"):
        if mail:
            generated_otp = opt_verify(mail)
            st.session_state.generated_otp = generated_otp
            st.session_state.user_mail = mail
            verify_otp(mail, generated_otp)
        else:
            st.warning("Please enter your email address to receive the OTP.")
else:
    st.write("Your email has been verified successfully!")
