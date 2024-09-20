import streamlit as st
from streamlit_chat import message
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import asyncio

st.title("🤖💬 Chat with Website Data")

groq_api_key = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

@st.cache_resource
def load_and_process_data(url):
    loader = WebBaseLoader(url)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100
    )
    splits = text_splitter.split_documents(data)
    
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(splits, embedding)
    return vectordb

async def response_generator(vectordb, query):
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. {context} Question: {question} Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectordb.as_retriever(), return_source_documents=True, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    
    result = await asyncio.to_thread(qa_chain, {"query": query})
    return result["result"]

url = st.text_input("Enter your URL: ")

st.subheader("", divider='rainbow')
st.markdown(" ")

if url:
    vectordb = load_and_process_data(url)
    
    # Use a unique key for this page's chat history
    if "web_chat_messages" not in st.session_state:
        st.session_state.web_chat_messages = []
    
    for message in st.session_state.web_chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if query := st.chat_input("What would you like to know about this website?"):
        st.session_state.web_chat_messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        with st.spinner("Generating response..."):
            response = asyncio.run(response_generator(vectordb, query))
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.web_chat_messages.append({"role": "assistant", "content": response})
else:
    st.write("Please enter a URL to start chatting about its content.")