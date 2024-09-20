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
import asyncio

st.title("🤖💬 Chat with Data")

groq_api_key = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

@st.cache_resource
def load_and_process_data(files):
    all_splits = []
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.read())
            file_path = temp_file.name
        
        loader = PyPDFLoader(file_path)
        data = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100
        )
        splits = text_splitter.split_documents(data)
        all_splits.extend(splits)
    
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(all_splits, embedding)
    return vectordb

async def response_generator(vectordb, query):
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. {context} Question: {question} Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectordb.as_retriever(), return_source_documents=True, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    
    result = await asyncio.to_thread(qa_chain, {"query": query})
    return result["result"]

files = st.file_uploader("Upload PDF File(s)", type=["pdf"], accept_multiple_files=True)
submit_pdf = st.checkbox('Submit and chat (PDF)')

st.subheader("", divider='rainbow')
st.markdown(" ")

if files and submit_pdf:
    vectordb = load_and_process_data(files)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if query := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        with st.spinner("Generating response..."):
            response = asyncio.run(response_generator(vectordb, query))
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})