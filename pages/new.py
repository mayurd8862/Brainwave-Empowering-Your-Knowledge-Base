import streamlit as st
import pymongo

# Streamlit app interface
st.title('Welcome to :violet[BrainWave] :sunglasses:')


choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

if choice == "Sign up":
    username = st.text_input('👤 Enter unique username')
    email = st.text_input('📧 Email Address')
    password = st.text_input('🔑 Password', type='password')

    st.session_state.username = username
    st.session_state.email = email
    st.session_state.password = password

    if st.button("Register"):
        # st.write(st.session_state.username)
        st.write(username)

else:
    email = st.text_input('📧 Email Address')
    password = st.text_input('🔑 Password', type='password')

    st.session_state.email_input = email
    st.session_state.password_input = password

    st.button('Login')

