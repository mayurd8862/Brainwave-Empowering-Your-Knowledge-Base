# import pymongo
# import streamlit as st
# from datetime import datetime

# myclient = pymongo.MongoClient("mongodb+srv://mayurdabade1103:HvZ2QBn2XuQYool8@brainwave.bndu2pa.mongodb.net/")
# mydb = myclient["Brainwave"]

# def save_content(proj_name, title, content, time_data):
#     info = {"Title": title, "Content": content, "time_date": time_data}
#     mycol = mydb[proj_name]
#     mycol.insert_one(info)

# # Initialize session state variables
# if 'project_name' not in st.session_state:
#     st.session_state.project_name = ''
# if 'title' not in st.session_state:
#     st.session_state.title = ''
# if 'note_content' not in st.session_state:
#     st.session_state.note_content = ''
# if 'selected_folder' not in st.session_state:
#     st.session_state.selected_folder = None
# if 'selected_title' not in st.session_state:
#     st.session_state.selected_title = None

# if __name__ == '__main__':
#     t1, t2 = st.tabs(['Create Notes', 'Show Saved Notes'])

#     with t1:
#         st.session_state.project_name = st.text_input("📁Enter project name to save it as a folder:", st.session_state.project_name)
#         st.session_state.title = st.text_input("Enter title", st.session_state.title)
#         st.session_state.note_content = st.text_area("📝Enter your notes here:", st.session_state.note_content)
#         save_button = st.button("Save")

#         current_time = datetime.now()
#         time_data = current_time.strftime("%A, %d %B %Y %I:%M:%S %p")

#         if save_button:
#             if st.session_state.project_name and st.session_state.title and st.session_state.note_content:
#                 save_content(st.session_state.project_name, st.session_state.title, st.session_state.note_content, time_data)
#                 st.success("✔️ Saved successfully")
#             else:
#                 st.error("Please fill in all fields before saving.")

#     with t2:
#         collections = mydb.list_collection_names()
#         filtered_collections = [collection for collection in collections if collection != "Login_Credentials"]

#         st.session_state.selected_folder = st.selectbox("Select a folder:", filtered_collections, index=filtered_collections.index(st.session_state.selected_folder) if st.session_state.selected_folder else 0)
#         st.session_state.selected_title = st.selectbox("Select a title:", mydb[st.session_state.selected_folder].distinct("Title") if st.session_state.selected_folder else [])

#         if st.session_state.selected_title:
#             document = mydb[st.session_state.selected_folder].find_one({"Title": st.session_state.selected_title})

#             if document:
#                 st.write("Content:", document["Content"])
#                 st.write("Time Date:", document["time_date"])
#             else:
#                 st.write("No information found for selected title.")



import pymongo
import streamlit as st
from datetime import datetime

# myclient = pymongo.MongoClient("mongodb+srv://mayurdabade1103:HvZ2QBn2XuQYool8@brainwave.bndu2pa.mongodb.net/")
# mydb = myclient["Brainwave"]

def save_content(proj_name,title,content,time_data):
    myclient = pymongo.MongoClient("mongodb+srv://mayurdabade1103:HvZ2QBn2XuQYool8@brainwave.bndu2pa.mongodb.net/")
    mydb = myclient["Brainwave"]
    info ={"Title": title, "Content": content, "time_date" : time_data}
    mycol = mydb[proj_name]
    mycol.insert_one(info)

if __name__ == '__main__':

    
    t1,t2 = st.tabs(['Create Notes','Show Saved Notes'])

    with t1:
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
        myclient = pymongo.MongoClient("mongodb+srv://mayurdabade1103:HvZ2QBn2XuQYool8@brainwave.bndu2pa.mongodb.net/")
        mydb = myclient["Brainwave"]
        collections = mydb.list_collection_names()

        # Filter out the collections you don't want
        filtered_collections = [collection for collection in collections if collection != "Login_Credentials"]
        
        selected_folder = st.selectbox("Select a folder:", filtered_collections)
        selected_title = st.selectbox("Select a title:", mydb[selected_folder].distinct("Title"))
        st.write("Hello")

        if selected_title:
            # Query MongoDB collection to retrieve document based on selected title
            document = mydb[selected_folder].find_one({"Title": selected_title})

            # Display content and time_data of selected title
            if document:
                st.write("Content:", document["Content"])
                st.write("Time Date:", document["time_date"])
            else:
                st.write("No information found for selected title.")


   