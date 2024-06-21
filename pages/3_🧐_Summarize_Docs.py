import streamlit as st
import asyncio
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
import os
import tempfile
GOOGLE_API_KEY = st.secrets.GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY)

headers ={
    'GOOGLE_API_KEY' : st.secrets["GOOGLE_API_KEY"]
}


try:
    asyncio.get_running_loop()
except RuntimeError:
    # Create a new event loop if there isn't one
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


# from langchain_groq import ChatGroq
# groq_api_key= st.secrets.GROQ_API_KEY
# llm=ChatGroq(groq_api_key=groq_api_key,
#             model_name="Llama3-8b-8192")


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
    # summaries = []
    for pdf_file in pdf_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(pdf_file.read())
        
        loader = PyPDFLoader(temp_path)
        docs = loader.load_and_split()
        # chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary_chain = load_summarize_chain(llm=llm,
                                        chain_type='map_reduce',
                                        map_prompt=map_prompt_template,
                                        combine_prompt=combine_prompt_template,
                                        verbose=True)  # Optional for debugging

        summary = summary_chain.run(docs)
        os.remove(temp_path)
    
    return summary


# Streamlit App
st.title("🚀Document Summarizer")
pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if pdf_files:

    if st.button("Generate Summary"):
        summary = summarize_pdfs_from_folder(pdf_files)
        st.write(f"Summary for PDF:")
        st.write(summary)
