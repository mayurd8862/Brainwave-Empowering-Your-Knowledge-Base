import streamlit as st
import json
from streamlit_lottie import st_lottie

# from st_social_media_links import SocialMediaIcons

# social_media_links = [
#     "https://www.linkedin.com/in/mayur-dabade-b527a9230",
#     "https://www.instagram.com/ThisIsAnExampleLink",
#     "https://www.github.com/jlnetosci/st-social-media-links",
# ]

# social_media_icons = SocialMediaIcons(social_media_links)

# social_media_icons.render(sidebar=True)

from utils import contributor_card, enric_info
with st.sidebar:

    st.divider()

    st.write("### 👨‍💻 Developed by:")
    st.markdown(contributor_card(
        **enric_info,
        ), 
        unsafe_allow_html=True)
    
st.title("🧠 Brainwave: 🤖 Empowering Your Knowledge Base")

st.write("""
Brainwave: is your ultimate companion for project management and data interaction. Chat with PDFs and websites, craft insightful notes, and effortlessly summarize documents—all in one place! Upgrade your productivity and streamline your workflow with Brainwave today. 🚀💡
""")

# Function to load the Lottie file
def load_lottiefile(filepath: str):
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)

# Load the Lottie file
lottie_coding = load_lottiefile("images/hello.json")

# with st.sidebar:
#     st_lottie(lottie_coding, speed=1, loop=True, quality="high", height=300, width=300)

st_lottie(lottie_coding, speed=1, loop=True, quality="high", height=400, width=400)