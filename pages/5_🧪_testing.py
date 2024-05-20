import streamlit as st
import pymongo

# Create an empty container
# placeholder = st.empty()

myclient = pymongo.MongoClient("mongodb+srv://mayurdabade1103:HvZ2QBn2XuQYool8@brainwave.bndu2pa.mongodb.net/")
mydb = myclient["Brainwave"]
mycol = mydb["Login_Credentials"]

def save_cred(name,mail,pwd):
    info ={"Name": name, "Mail": mail, "Password" : pwd}
    mycol.insert_one(info)


@st.experimental_dialog("🔐Enter Registration Credentials")
def main():
    name = st.text_input("👤 Enter Name")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    st.write("Otp sent successfully on your mail check mail andn enter otp for verification")

    # if email and password:
        
    #     otp = st.text_input("🛡️ Verify OTP sent on your mail", type="password")
    # reason = st.text_input("Because...")
    if st.button("Submit"):
        
        st.session_state.main = {"email": email, "password": password}
        st.rerun()
        
st.write("hello")

if __name__ == '__main__':
    main()

