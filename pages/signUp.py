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

if __name__ == '__main__':
    st.title("🔐Enter Registration Credentials")

    placeholder = st.empty()
    with placeholder.form("registration"):
        # st.markdown("#### Enter Registration credentials")
        name = st.text_input("👤 Enter Name")
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        st.write("Otp sent successfully on your mail check mail andn enter otp for verification")
        otp = st.text_input("🛡️ Verify OTP sent on your mail", type="password")
        
        submit = st.form_submit_button(" REGISTER ")

    if submit:
        if not email or not password or not name or not otp:
            st.error("Please fill in all required fields.")
        else:
            if(otp==123):
                save_cred(name,email,password)
                placeholder.empty()
                st.success("✔️ Registration successful")
            else:
                st.error("❌ Enter correct OTP")
