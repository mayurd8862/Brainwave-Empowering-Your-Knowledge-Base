import streamlit as st
from otp_test import generateOTP,send_otp



@st.experimental_dialog("🔑 Reset Your Password")
def verify_popup(mail,otp_generated):
    
    st.write(f"Verification OTP sent on your mail '{mail}' please Enter OTP and update your password {otp_generated}")
    
    otp = st.text_input("Enter Your OTP: ")
    if otp:
        if otp == otp_generated:
            st.success("✔️ OTP verified successfully")
            pass1 = st.text_input("Enter New Password:", type='password')
            pass2 = st.text_input("Enter Password once again:", type='password')

        else:
            st.error("❌ Please enter correct OTP")

    if st.button("Submit"):
        if pass1 != pass2 :
            st.warning("Please enter same passwords!!!")
        # pass
        


choice = st.selectbox('Login/Signup', ['Sign up','Login', 'forgot password'])

if choice == "Sign up":
    username = st.text_input('👤 Enter unique username')
    email = st.text_input('📧 Email Address')
    password = st.text_input('🔑 Password', type='password')

    if st.button("Register"):
        pass


elif choice == "Login":
    email = st.text_input('📧 Email Address')
    password = st.text_input('🔑 Password', type='password')

    st.session_state.email_input = email
    st.session_state.password_input = password

    # st.button('Login', on_click=handle_login)

else:
    otp_generated = generateOTP()

    sender_email = "mayurdabade1103@gmail.com"
    # receiver_email = "savitadabade1604@gmail.com"
    password = st.secrets['mail_pwd'] # Your App Password
    subject = "BrainWave password recovery"
    body = f"Verification OTP for password recovery - {otp_generated}."


    if "reset_mail" not in st.session_state:
        reset_mail = st.text_input("Enter your registered mail: ")
        # st.write("Vote for your favorite")
    if st.button("NEXT"):
        send_otp(sender_email,reset_mail, password, subject, body)
        verify_popup(reset_mail, otp_generated)





