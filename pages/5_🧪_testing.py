# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build

# # Load OAuth 2.0 credentials from a file or some secure storage
# creds = Credentials.from_authorized_user_file('credentials.json')

# # Build the Drive service
# drive_service = build('drive', 'v3', credentials=creds)

# def upload_file_to_drive(file_path, file_name):
#     file_metadata = {'name': file_name}
#     media = MediaFileUpload(file_path, mimetype='application/pdf')
#     file = drive_service.files().create(body=file_metadata,
#                                         media_body=media,
#                                         fields='id').execute()
#     return file.get('id')

# def generate_shareable_link(file_id):
#     permission = {
#         'type': 'anyone',
#         'role': 'reader',
#     }
#     drive_service.permissions().create(fileId=file_id, body=permission).execute()
#     return f'https://drive.google.com/file/d/{file_id}/view?usp=sharing'

# # Example usage
# file_path = '/path/to/your/summary.pdf'
# file_name = 'summary.pdf'
# file_id = upload_file_to_drive(file_path, file_name)
# shareable_link = generate_shareable_link(file_id)
# print("Shareable link:", shareable_link)

    
import pymongo
import streamlit as st
from datetime import datetime

myclient = pymongo.MongoClient("mongodb+srv://mayurdabade1103:HvZ2QBn2XuQYool8@brainwave.bndu2pa.mongodb.net/")
mydb = myclient["Brainwave"]

def save_content(proj_name,title,content,time_data):
    # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # mydb = myclient["Brainwave"]
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
        print(mydb.list_collection_names())
        
        selected_folder = st.selectbox("Select a folder:", mydb.list_collection_names())
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





### Saving notes to local directory


# import streamlit as st
# import os
# from datetime import datetime
# st.title("✏️📓Create Notes")

# def save_notes(notes, folder_name):
#     notes_folder = "Notes"
#     if not os.path.exists(notes_folder):
#         os.makedirs(notes_folder)
#     folder_path = os.path.join(notes_folder, folder_name)
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Add timestamp to filename
#     file_path = os.path.join(folder_path, f"notes_{timestamp}.txt")  # Use timestamp in filename
#     with open(file_path, 'w') as file:  
#         file.write(notes)


# def read_files_from_folder(selected_folder):
#     folder_contents = os.listdir(selected_folder)
#     files = [f for f in folder_contents if os.path.isfile(os.path.join(selected_folder, f))]
#     return files


# t1,t2 = st.tabs(['Create Notes','Show Saved Notes'])

# with t1:

#     # Ask user for folder name
#     folder_name = st.text_input("📁Enter project name to save it as a folder:")
    
#     # Display notes section only if folder name is provided
#     if folder_name:
#         notes = st.text_area("📝Enter your notes here:")
#         save_button = st.button("Save")

#         if save_button:
#             save_notes(notes, folder_name)
#             st.success(f"Notes saved successfully in folder: {folder_name}👍")

# with t2:

#     # Ask user to select a folder
#     notes_folder = "Notes"
#     selected_folder = st.selectbox("Select a folder:", os.listdir(notes_folder))

#     if selected_folder:
#         folder_path = os.path.join(notes_folder, selected_folder)
        
#         # Display files and folders in the selected folder
#         folder_contents = os.listdir(folder_path)
#         files = [f for f in folder_contents if os.path.isfile(os.path.join(folder_path, f))]
        
#         # Show files in dropdown
#         selected_file = st.selectbox("Select a file:", files)

#         if selected_file:
#             file_path = os.path.join(folder_path, selected_file)
#             with open(file_path, 'r', encoding='utf-8') as file:

#             # with open(file_path, 'r') as file:
#                 file_contents = file.read()
#                 st.subheader(f"Contents of {selected_file}:")
#                 st.write(file_contents)
        
#         share = st.button("share")
    
    
