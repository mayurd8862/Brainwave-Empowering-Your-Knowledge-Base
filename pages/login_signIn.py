import streamlit as st
import pymongo

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

myclient = pymongo.MongoClient("mongodb+srv://mayurdabade1103:HvZ2QBn2XuQYool8@brainwave.bndu2pa.mongodb.net/")
mydb = myclient["Brainwave"]
mycol = mydb["Login_Credentials"]

def save_cred(name,mail,pwd):
    info ={"Name": name, "Mail": mail, "Password" : pwd}
    mycol.insert_one(info)


if __name__ == '__main__':

    
    t1,t2 = st.columns(2)

    with t1:
        # Insert a form in the container
        with placeholder.form("registration"):
            st.markdown("#### Enter Registration credentials")
            name = st.text_input("Enter Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("registration")

        if submit:
            if not email or not password or not name:
                st.error("Please fill in all required fields.")
            else:
                save_cred(name,email,password)
                placeholder.empty()
                st.success("✔️ Registration successful")


    with t2:
            # with t2:
        # Insert a form in the container
        with placeholder.form("login"):
            st.markdown("#### Enter Login credentials")
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login")

            if submit_login:
                if not login_email or not login_password:
                    st.error("Please fill in all required fields.")
                # Query MongoDB collection to check if the provided email and password match
                else:
                    user = mycol.find_one({"Mail": login_email, "Password": login_password})
                    if user:
                        st.success("✔️ Login successful")
                    else:
                        st.error("❌ Invalid email or password")

