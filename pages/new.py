# import streamlit as st
# import pymongo

# # Streamlit app interface
# st.title('Welcome to :violet[BrainWave] :sunglasses:')


# choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

# if choice == "Sign up":
#     username = st.text_input('👤 Enter unique username')
#     email = st.text_input('📧 Email Address')
#     password = st.text_input('🔑 Password', type='password')

#     st.session_state.username = username
#     st.session_state.email = email
#     st.session_state.password = password

#     if st.button("Register"):
#         # st.write(st.session_state.username)
#         st.write(username)

# else:
#     email = st.text_input('📧 Email Address')
#     password = st.text_input('🔑 Password', type='password')

#     st.session_state.email_input = email
#     st.session_state.password_input = password

#     st.button('Login')



import streamlit as st
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Brainwave"]
mycol = mydb["notes"]

myquery = {"project_name" : "hello "}

mydoc = mycol.find(myquery)

# for x in mydoc:
#   print(x)

# if "useremail" in st.session_state:
#     user_email = st.session_state.useremail
#     st.write("Welcome u logged in as",user_email)

if "useremail" not in st.session_state:
    st.warning("you need to sign in first.")
    if st.button("Login/Register"):
        st.switch_page("pages/1_🤵_Account.py")

# proj_name = st.selectbox("Select a project name:", mycol.distinct("project_name",{"username": user_email}))

proj_name = st.selectbox("Select a project name:", mycol.distinct("project_name"))
titles = mycol.distinct("title", {"project_name": proj_name})
title = st.selectbox("Select a title:", titles)

st.write("Hello")

if title:

    document = mycol.find_one({"title": title})

    if document:
        st.write("content:\n", document["content"])
        st.write("time_date:", document["time_date"])
    else:
        st.write("No information found for selected title.")
