import streamlit as st
import os

# Function to create a contributor card
def contributor_card(image_url="", name="", linkedin_url="", github_url="",instagram_url=""):
    """
    Creates a contributor card with profile image, name, role, and LinkedIn profile link.
    """

    card = f"""
        <div style="border-radius: 10px; padding: 1rem; background-color: #484c63; display: flex; align-items: center; margin-bottom: 0.5rem; color: #fff;">
            <img src="{image_url}" alt="Profile picture" style="border-radius: 50%; width: 60px; height: 60px; margin-right: 1rem;">
            <div style="line-height: 1;">
                <div style="font-weight: bold; margin-bottom: 0.7rem;">{name}</div>
                <a href="{linkedin_url}" target="_blank" style="font-size: 1.5rem; margin-right: 0.3rem; text-decoration: none; color: #0f77a8;">
                    <i class="fab fa-linkedin"></i>
                </a>
                <a href="{github_url}" target="_blank" style="font-size: 1.5rem;margin-right: 0.3rem; text-decoration: none; color: #333;">
                    <i class="fab fa-github"></i>
                </a>
                <a href="{instagram_url}" target="_blank" style="font-size: 1.5rem; text-decoration: none; color: #e1316d;">
                    <i class="fab fa-instagram"></i>
                </a>
            </div>
        </div>
    """


    return card

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)
# st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)


enric_info = {
    "name": "Mayur Dabade :)",
    "image_url": "https://media.licdn.com/dms/image/D5603AQHqV8w2fEdBaw/profile-displayphoto-shrink_400_400/0/1704638155564?e=1724284800&v=beta&t=0VXSh7ciLfqCo6VPiAJBWh9cUO0jPSNtNX7OufwXYag",
    "linkedin_url": "https://www.linkedin.com/in/mayur-dabade-b527a9230",
    "github_url": "https://github.com/mayurd8862",
    "instagram_url":"#"
}