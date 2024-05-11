# # libraries for chat with csv
# import streamlit as st
# from langchain_openai.chat_models import ChatOpenAI
# from langchain_experimental.agents.agent_toolkits import create_csv_agent
# from streamlit_chat import message
# import os
# import streamlit as st
# import pandas as pd


# # libraries for chat with pdf
# import streamlit as st

# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import google.generativeai as genai
# from langchain.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv

# load_dotenv()
# os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# def get_pdf_text(pdf_docs):
#     text=""
#     for pdf in pdf_docs:
#         pdf_reader= PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text+= page.extract_text()
#     return  text

# def get_text_chunks(text):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
#     chunks = text_splitter.split_text(text)
#     return chunks


# def get_vector_store(text_chunks):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
#     vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
#     vector_store.save_local("faiss_index")


# def get_conversational_chain():

#     prompt_template = """
#     Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
#     provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
#     Context:\n {context}?\n
#     Question: \n{question}\n

#     Answer:
#     """

#     model = ChatGoogleGenerativeAI(model="gemini-pro",
#                              temperature=0.3)

#     prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
#     chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

#     return chain



# def user_input(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
#     new_db = FAISS.load_local("faiss_index", embeddings)
#     docs = new_db.similarity_search(user_question)

#     chain = get_conversational_chain()
#     response = chain(
#         {"input_documents":docs, "question": user_question}
#         , return_only_outputs=True)

#     # print(response)
#     # st.write("Reply: ", response["output_text"])
#     return response["output_text"]

# api= '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'
# llm = ChatOpenAI(api_key=api,model='gpt-3.5-turbo')

# def main():

    
#     st.title("🤖💬Chat with Your data")

#     t1,t2= st.tabs(['Chat With PDF data','Chat with CSV data'])


#     with t1:

#         pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
#         # if st.button("Submit & Process"):
#         if st.checkbox('Submit & Process 🔄 '):
#             # with st.spinner("Processing..."):
#             raw_text = get_pdf_text(pdf_docs)
#             text_chunks = get_text_chunks(raw_text)
#             get_vector_store(text_chunks)
#                 # st.success("Successfuly saved word embedding in VectorDB")

#             # user_question = st.text_input("Ask a Question from the PDF Files")

#             # if user_question:
#             #     user_input(user_question)



#             if 'responses' not in st.session_state:
#                 st.session_state['responses'] = ["Ask Queries to your dataset"]

#             if 'requests' not in st.session_state:
#                 st.session_state['requests'] = []

#             response_container = st.container()
#             # container for text box
#             textcontainer = st.container()

#             with textcontainer:
#                 query = st.chat_input("Query: ", key="input")
#                 if query:
#                     with st.spinner("typing..."):

#                         # ans = agent_executor.invoke(query)
#                         response = user_input(query)

#                     st.session_state.requests.append(query)
#                     st.session_state.responses.append(response)
                
#             with response_container:
#                 if st.session_state['responses']:
#                     # Display chat history
#                     for i in range(len(st.session_state['responses'])):
#                         message(st.session_state['responses'][i], key=str(i))
#                         if i < len(st.session_state['requests']):
#                             message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')




#     with t2:

#         csv_file = st.file_uploader("Upload a CSV file", type="csv")
#         if csv_file is not None:

#             agent_executor = create_csv_agent(
#                 llm,
#                 csv_file,
#                 agent_type="openai-tools",
#                 verbose=True
#             )



#         if st.checkbox('Submit & Process 🔄'):

#             # if csv_file is not None:
#             #     df = pd.read_csv(csv_file)
#             #     st.write(df)

#             if 'responses' not in st.session_state:
#                 st.session_state['responses'] = ["Ask Queries to your dataset"]

#             if 'requests' not in st.session_state:
#                 st.session_state['requests'] = []

#             response_container = st.container()
#             # container for text box
#             textcontainer = st.container()

#             with textcontainer:
#                 query = st.chat_input("Query: ", key="input")
#                 if query:
#                     with st.spinner("typing..."):

#                         ans = agent_executor.invoke(query)
#                         response = ans["output"]

#                     st.session_state.requests.append(query)
#                     st.session_state.responses.append(response)
                
#             with response_container:
#                 if st.session_state['responses']:
#                     # Display chat history
#                     for i in range(len(st.session_state['responses'])):
#                         message(st.session_state['responses'][i], key=str(i))
#                         if i < len(st.session_state['requests']):
#                             message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')


# if __name__ == "__main__":
#     main()





from langchain_community.chat_models import ChatOpenAI
import streamlit as st
import openai
from streamlit_chat import message
from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

import os
import tempfile
from langchain_community.document_loaders import WebBaseLoader

os.environ["GOOGLE_API_KEY"] = "AIzaSyDswh7HV9jrP19D5sGJjNwmGQQotuH7Fcs"
llm = ChatGoogleGenerativeAI(model="gemini-pro")


# llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")

st.title("🤖💬Chat with data")

# File uploader widget
file = st.file_uploader("Upload PDF File", type=["pdf"])
submit = st.checkbox('Submit and chat')

if submit:
   
    # with st.spinner("Creating Vector database..."):
    # st.write('Creating Vector database...')
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(file.read())
    file_path = temp_file.name
    temp_file.close()
    
    loader = PyPDFLoader(file_path)
    data = loader.load_and_split()  
    # loader = WebBaseLoader(url)
    # data = loader.load()
    # Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 150
    )
    splits = text_splitter.split_documents(data)

    # word embedding and storing it in Chroma databases
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    persist_directory = 'docs/chroma/'
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )


    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []


    # Build prompt
    from langchain.prompts import PromptTemplate
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. 
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

    # Run chain
    from langchain.chains import RetrievalQA

    # container for chat history
    response_container = st.container()
    # container for text box
    textcontainer = st.container()


    with textcontainer:
        query = st.chat_input("Query: ", key="input")
        if query:
            with st.spinner("typing..."):

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
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

        
        





