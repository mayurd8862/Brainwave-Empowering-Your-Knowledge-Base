# import streamlit as st
# import asyncio
# from langchain_community.document_loaders import PyPDFLoader
# from PyPDF2 import PdfReader
# from langchain.prompts import PromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.summarize import load_summarize_chain
# import os
# import tempfile

# GOOGLE_API_KEY = st.secrets.GOOGLE_API_KEY
# llm = None

# # Ensure there is a running event loop
# def get_or_create_event_loop():
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#     return loop

# loop = get_or_create_event_loop()

# async def initialize_llm():
#     global llm
#     llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# # Initialize the LLM asynchronously
# loop.run_until_complete(initialize_llm())

# headers = {
#     'GOOGLE_API_KEY': st.secrets["GOOGLE_API_KEY"]
# }

# map_prompt = """
# Write a concise summary of the following:
# "{text}"
# CONCISE SUMMARY:
# """
# map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
# combine_prompt = """
# Write a concise summary of the following text delimited by triple backquotes.
# Return your response in bullet points which covers the key points of the text.
# Also add emojis wherever needed.
# `{text}`
# BULLET POINT SUMMARY:
# """
# combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

# def summarize_pdfs_from_folder(pdf_files):
#     summaries = []
#     for pdf_file in pdf_files:
#         # if pdf_file is not None:
#         with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#             tmp_file.write(pdf_file.read())
#             pdf_path = tmp_file.name
#             loader = PyPDFLoader(pdf_path)
#             docs = loader.load_and_split()
#         # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         #     temp_path = temp_file.name
#         #     temp_file.write(pdf_file.read())
        
#         # loader = PyPDFLoader(pdf_files)
#         # docs = loader.load_and_split()
        
#         summary_chain = load_summarize_chain(llm=llm,
#                                              chain_type='map_reduce',
#                                              map_prompt=map_prompt_template,
#                                              combine_prompt=combine_prompt_template,
#                                              verbose=True)

#         summary = summary_chain.run(docs)
#         summaries.append(summary)
#         os.remove(pdf_path)
    
#     return summaries

# # Streamlit App
# st.title("🚀Document Summarizer")
# pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

# if pdf_files:
#     if st.button("Generate Summary"):
#         summaries = summarize_pdfs_from_folder(pdf_files)
#         for i, summary in enumerate(summaries, 1):
#             st.write(f"Summary for PDF {i}:")
#             st.write(summary)








import streamlit as st
from streamlit_chat import message
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import tempfile
import os

st.title("🤖💬 Chat with Data")

tab1, tab2 = st.tabs(["Chat with PDF", "Chat with Website"])

with tab1:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

    # File uploader widget
    file = st.file_uploader("Upload PDF File", type=["pdf"])
    submit = st.checkbox('Submit and chat')

    if submit and file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                file_path = temp_file.name

            loader = PyPDFLoader(file_path)
            data = loader.load_and_split()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=150
            )
            splits = text_splitter.split_documents(data)

            # Word embedding and storing it in FAISS vector store
            embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            vectordb = FAISS.from_documents(splits, embedding)

            if 'responses' not in st.session_state:
                st.session_state['responses'] = ["How can I assist you?"]
            if 'requests' not in st.session_state:
                st.session_state['requests'] = []

            template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. 
            {context}
            Question: {question}
            Helpful Answer:"""
            QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

            # Container for chat history
            response_container = st.container()
            # Container for text box
            textcontainer = st.container()

            with textcontainer:
                query = st.chat_input("Query: ", key="input")
                if query:
                    with st.spinner("Typing..."):
                        qa_chain = RetrievalQA.from_chain_type(llm,
                                                               retriever=vectordb.as_retriever(),
                                                               return_source_documents=True,
                                                               chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

                        result = qa_chain({"query": query})
                        response = result["result"]

                    st.session_state.requests.append(query)
                    st.session_state.responses.append(response)

            with response_container:
                if st.session_state['responses']:
                    for i in range(len(st.session_state['responses'])):
                        message(st.session_state['responses'][i], key=str(i))
                        if i < len(st.session_state['requests']):
                            message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Clean up the temporary file
            if os.path.exists(file_path):
                os.remove(file_path)
    elif submit:
        st.warning("Please upload a PDF file.")
