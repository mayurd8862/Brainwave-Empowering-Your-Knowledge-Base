import streamlit as st
import os
from datetime import datetime
st.title("✏️📓Create Notes")

def save_notes(notes, folder_name):
    notes_folder = "Notes"
    if not os.path.exists(notes_folder):
        os.makedirs(notes_folder)
    folder_path = os.path.join(notes_folder, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Add timestamp to filename
    file_path = os.path.join(folder_path, f"notes_{timestamp}.txt")  # Use timestamp in filename
    with open(file_path, 'w') as file:  
        file.write(notes)


def read_files_from_folder(selected_folder):
    folder_contents = os.listdir(selected_folder)
    files = [f for f in folder_contents if os.path.isfile(os.path.join(selected_folder, f))]
    return files


t1,t2 = st.tabs(['Create Notes','Show Saved Notes'])

with t1:

    # Ask user for folder name
    folder_name = st.text_input("📁Enter project name to save it as a folder:")
    
    # Display notes section only if folder name is provided
    if folder_name:
        notes = st.text_area("📝Enter your notes here:")
        save_button = st.button("Save")

        if save_button:
            save_notes(notes, folder_name)
            st.success(f"Notes saved successfully in folder: {folder_name}👍")

with t2:

    # Ask user to select a folder
    notes_folder = "Notes"
    selected_folder = st.selectbox("Select a folder:", os.listdir(notes_folder))

    if selected_folder:
        folder_path = os.path.join(notes_folder, selected_folder)
        
        # Display files and folders in the selected folder
        folder_contents = os.listdir(folder_path)
        files = [f for f in folder_contents if os.path.isfile(os.path.join(folder_path, f))]
        
        # Show files in dropdown
        selected_file = st.selectbox("Select a file:", files)

        if selected_file:
            file_path = os.path.join(folder_path, selected_file)
            with open(file_path, 'r', encoding='utf-8') as file:

            # with open(file_path, 'r') as file:
                file_contents = file.read()
                st.subheader(f"Contents of {selected_file}:")
                st.write(file_contents)
        
        share = st.button("share")
    
    
   
   