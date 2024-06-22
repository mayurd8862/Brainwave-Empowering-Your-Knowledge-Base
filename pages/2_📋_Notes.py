import streamlit as st
import pymongo
from streamlit_lottie import st_lottie
import json
from datetime import datetime

mongodb_connect = st.secrets.mongodb_atlas
# Function to load the Lottie file
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Load the Lottie file
lottie_coding = load_lottiefile("images/alert.json")

def save_content(proj_name,title,content,time_data):

    # myclient = pymongo.MongoClient("mongodb://localhost:27017")
    myclient = pymongo.MongoClient(mongodb_connect)
    
    mydb = myclient["Brainwave"]
    mycol = mydb["notes"]

    username= st.session_state.username

    info ={"username":username,
            "project_name":proj_name,
           "title": title, 
           "content": content, 
           "time_date" : time_data}
    
    mycol.insert_one(info)


if __name__ == '__main__':

    # Check if the user is logged in
    if "username" not in st.session_state:
        st.warning("You need to sign in first to use NOTES functionality.")
        st_lottie(lottie_coding, speed=1, loop=True, quality="high", height=300, width=300)

        if st.button("Login / Register"):
            st.switch_page("pages/1_🤵_Account.py")

    else:
    
        t1,t2 = st.tabs(['Create Notes','Show Saved Notes'])

        with t1:
            username= st.session_state.username
            st.success(f"🥳 Welcome, you are logged in as '{username}'")
            project_name = st.text_input("📁Enter project name to save it as a folder:")
            title = st.text_input("Enter title")
            note_content = st.text_area("📝Enter your notes here:")
            save_button = st.button("Save")

            current_time = datetime.now()
            # Format the date and time in a human-readable format
            time_data = current_time.strftime("%A, %d %B %Y %I:%M:%S %p")

            if save_button:
                save_content(project_name,title,note_content,time_data)
            
                st.success("✔️ Saved successfully")

        with t2:

            
            # myclient = pymongo.MongoClient("mongodb://localhost:27017")
            myclient = pymongo.MongoClient(mongodb_connect)

            mydb = myclient["Brainwave"]
            mycol = mydb["notes"]
            collections = mydb.list_collection_names()

            user_name = st.session_state.username
            # st.write("Welcome, you are logged in as", user_name)

            # Select a project name
            project_names = mycol.distinct("project_name", {"username": user_name})
            if project_names:
                proj_name = st.selectbox("Select a project name:", project_names)

                # Select a title based on the selected project name
                if proj_name:
                    titles = mycol.distinct("title", {"project_name": proj_name, "username": user_name})
                    if titles:
                        title = st.selectbox("Select a title:", titles)
                        
                        if title:
                            # Fetch and display the document content and date
                            document = mycol.find_one({"title": title, "project_name": proj_name, "username": user_name})
                            
                            if document:
                                st.markdown(f"## {title}")
                                st.write("Content:\n", document["content"])
                                st.write("⏰", document["time_date"])
                            else:
                                st.write("No information found for the selected title.")
                    else:
                        st.write("No titles found for the selected project.")
            else:
                st.write("No projects found.")
    

# st.session_state