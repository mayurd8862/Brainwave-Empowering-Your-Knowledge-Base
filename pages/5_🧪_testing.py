import streamlit as st
import asyncio
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
import os
import tempfile

GOOGLE_API_KEY = st.secrets.GOOGLE_API_KEY
llm = None

# Ensure there is a running event loop
def get_or_create_event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

loop = get_or_create_event_loop()

async def initialize_llm():
    global llm
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# Initialize the LLM asynchronously
loop.run_until_complete(initialize_llm())

headers = {
    'GOOGLE_API_KEY': st.secrets["GOOGLE_API_KEY"]
}

map_prompt = """
Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:
"""
map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
combine_prompt = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in bullet points which covers the key points of the text.
Also add emojis wherever needed.
`{text}`
BULLET POINT SUMMARY:
"""
combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

def summarize_pdfs_from_folder(pdf_files):
    summaries = []
    for pdf_file in pdf_files:
        # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #     temp_path = temp_file.name
        #     temp_file.write(pdf_file.read())
        
        loader = PyPDFLoader(pdf_files)
        docs = loader.load_and_split()
        
        summary_chain = load_summarize_chain(llm=llm,
                                             chain_type='map_reduce',
                                             map_prompt=map_prompt_template,
                                             combine_prompt=combine_prompt_template,
                                             verbose=True)

        summary = summary_chain.run(docs)
        summaries.append(summary)
        os.remove(temp_path)
    
    return summaries

# Streamlit App
st.title("🚀Document Summarizer")
pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if pdf_files:
    if st.button("Generate Summary"):
        summaries = summarize_pdfs_from_folder(pdf_files)
        for i, summary in enumerate(summaries, 1):
            st.write(f"Summary for PDF {i}:")
            st.write(summary)
