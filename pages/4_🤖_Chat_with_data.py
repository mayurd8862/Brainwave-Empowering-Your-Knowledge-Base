import streamlit as st
from streamlit_chat import message
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import tempfile
import os
import uuid

st.title("🤖💬 Chat with Data")

tab1, tab2 = st.tabs(["Chat with PDF", "Chat with Website"])

groq_api_key = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

def init_session_state(key_prefix):
    if f'{key_prefix}_responses' not in st.session_state:
        st.session_state[f'{key_prefix}_responses'] = ["How can I assist you?"]
    if f'{key_prefix}_requests' not in st.session_state:
        st.session_state[f'{key_prefix}_requests'] = []

def load_and_process_data(loader):
    data = loader.load_and_split() if isinstance(loader, PyPDFLoader) else loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150
    )
    splits = text_splitter.split_documents(data)

    # Word embedding and storing it in FAISS vector store
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(splits, embedding)

    return vectordb

def chat_interface(vectordb, input_key, key_prefix):
    init_session_state(key_prefix)

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
        query = st.chat_input("Query:", key=input_key)
        if query:
            with st.spinner("Typing..."):
                qa_chain = RetrievalQA.from_chain_type(llm,
                                                       retriever=vectordb.as_retriever(),
                                                       return_source_documents=True,
                                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

                result = qa_chain({"query": query})
                response = result["result"]

            st.session_state[f'{key_prefix}_requests'].append(query)
            st.session_state[f'{key_prefix}_responses'].append(response)

    with response_container:
        if st.session_state[f'{key_prefix}_responses']:
            for i in range(len(st.session_state[f'{key_prefix}_responses'])):
                unique_key = str(uuid.uuid4())
                message(st.session_state[f'{key_prefix}_responses'][i], key=f'response_{key_prefix}_{unique_key}')
                if i < len(st.session_state[f'{key_prefix}_requests']):
                    message(st.session_state[f'{key_prefix}_requests'][i], is_user=True, key=f'request_{key_prefix}_{unique_key}_user')

with tab1:
    file = st.file_uploader("Upload PDF File", type=["pdf"])
    submit_pdf = st.checkbox('Submit and chat (PDF)')

    if submit_pdf and file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                file_path = temp_file.name

            loader = PyPDFLoader(file_path)
            vectordb = load_and_process_data(loader)
            chat_interface(vectordb, "input_pdf", "pdf")

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Clean up the temporary file
            if os.path.exists(file_path):
                os.remove(file_path)
    elif submit_pdf:
        st.warning("Please upload a PDF file.")

with tab2:
    url = st.text_input("Enter website URL:")
    submit_url = st.checkbox('Submit and chat (URL)')

    if submit_url and url:
        try:
            loader = WebBaseLoader(url)
            vectordb = load_and_process_data(loader)
            chat_interface(vectordb, "input_url", "url")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif submit_url:
        st.warning("Please enter a website URL.")
