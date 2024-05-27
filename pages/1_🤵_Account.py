import streamlit as st
import pymongo

# Function to sign up a new user
def sign_up(name, mail, pwd):
    if not name or not mail or not pwd:
        return False, "⚠️All fields are required."

    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["Brainwave"]
    mycol = mydb["Login_Credentials"]

    if mycol.find_one({"Mail": mail}):
        return False, "Email already exists."
    
    info = {"Name": name, "Mail": mail, "Password": pwd}
    mycol.insert_one(info)
    return True, "Account created successfully!"

# Function to sign in an existing user
def sign_in(mail, pwd):

    if not mail or not pwd:
        return None

    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["Brainwave"]
    mycol = mydb["Login_Credentials"]

    user = mycol.find_one({"Mail": mail, "Password": pwd})
    if user:
        return user
    else:
        return None

# Function to handle user login
def handle_login():
    userinfo = sign_in(st.session_state.email_input, st.session_state.password_input)
    if userinfo:
        st.session_state.username = userinfo['Name']
        st.session_state.useremail = userinfo['Mail']
        st.session_state.signedout = True
        st.session_state.signout = True
    else:
        st.warning('⚠️Login Failed')

# Function to handle user logout
def handle_logout():
    st.session_state.signout = False
    st.session_state.signedout = False
    st.session_state.username = ''
    st.session_state.useremail = ''
    del st.session_state.username

# Streamlit app interface
st.title('Welcome to :violet[BrainWave] :sunglasses:')

# Initialize session state variables
# if 'username' not in st.session_state:
#     st.session_state.username = ''
if 'useremail' not in st.session_state:
    st.session_state.useremail = ''
if "signedout" not in st.session_state:
    st.session_state["signedout"] = False
if 'signout' not in st.session_state:
    st.session_state['signout'] = False

if not st.session_state["signedout"]:
    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

    if choice == "Sign up":
        username = st.text_input('👤 Enter unique username')
        email = st.text_input('📧 Email Address')
        password = st.text_input('🔑 Password', type='password')

        if st.button("Register"):
            success, message = sign_up(username, email, password)
            if success:
                st.success(message)
                st.balloons()
            else:
                st.warning(message)

    else:
        email = st.text_input('📧 Email Address')
        password = st.text_input('🔑 Password', type='password')

        st.session_state.email_input = email
        st.session_state.password_input = password

        st.button('Login', on_click=handle_login)

if st.session_state.signout:
    st.success(f"✔️ logged in as :- **{st.session_state.username}**")

    st.markdown("### ✨ Explore the features of our project ")
    st.write("1) 📂 **Project Management** : Organize your notes and documents project-wise.")
    st.write("2) 💬 **Chat with Documents** : Interact with your PDFs and CSVs through an intuitive chat interface.")
    st.write("3) 📝 **Document Summarization** : Generate concise summaries of your PDF documents.")


    # st.text('Name: ' + st.session_state.username)
    # st.text('Email id: ' + st.session_state.useremail)
    st.button('Sign out', on_click=handle_logout)




