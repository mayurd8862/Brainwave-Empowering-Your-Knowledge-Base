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


@st.experimental_dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

# if "vote" not in st.session_state:
#     st.write("Vote for your favorite")
#     if st.button("A"):
#         vote("A")
#     if st.button("B"):
#         vote("B")
# else:
#     f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

def main():
    st.write("Hello Mayur!!")


if __name__ == '__main__':
    vote("A")
    main()
