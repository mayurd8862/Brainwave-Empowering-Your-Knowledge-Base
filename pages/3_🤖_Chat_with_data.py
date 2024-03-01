# libraries for chat with csv
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from streamlit_chat import message
import os
import streamlit as st
import pandas as pd


# libraries for chat with pdf
import streamlit as st

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    # print(response)
    # st.write("Reply: ", response["output_text"])
    return response["output_text"]

api= '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'
llm = ChatOpenAI(api_key=api,model='gpt-3.5-turbo')

def main():

    
    st.title("🤖💬Chat with Your data")

    t1,t2= st.tabs(['Chat With PDF data','Chat with CSV data'])


    with t1:

        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        # if st.button("Submit & Process"):
        if st.checkbox('Submit & Process 🔄 '):
            # with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_docs)
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks)
                # st.success("Successfuly saved word embedding in VectorDB")

            # user_question = st.text_input("Ask a Question from the PDF Files")

            # if user_question:
            #     user_input(user_question)



            if 'responses' not in st.session_state:
                st.session_state['responses'] = ["Ask Queries to your dataset"]

            if 'requests' not in st.session_state:
                st.session_state['requests'] = []

            response_container = st.container()
            # container for text box
            textcontainer = st.container()

            with textcontainer:
                query = st.chat_input("Query: ", key="input")
                if query:
                    with st.spinner("typing..."):

                        # ans = agent_executor.invoke(query)
                        response = user_input(query)

                    st.session_state.requests.append(query)
                    st.session_state.responses.append(response)
                
            with response_container:
                if st.session_state['responses']:
                    # Display chat history
                    for i in range(len(st.session_state['responses'])):
                        message(st.session_state['responses'][i], key=str(i))
                        if i < len(st.session_state['requests']):
                            message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')




    with t2:

        csv_file = st.file_uploader("Upload a CSV file", type="csv")
        if csv_file is not None:

            agent_executor = create_csv_agent(
                llm,
                csv_file,
                agent_type="openai-tools",
                verbose=True
            )



        if st.checkbox('Submit & Process 🔄'):

            # if csv_file is not None:
            #     df = pd.read_csv(csv_file)
            #     st.write(df)

            if 'responses' not in st.session_state:
                st.session_state['responses'] = ["Ask Queries to your dataset"]

            if 'requests' not in st.session_state:
                st.session_state['requests'] = []

            response_container = st.container()
            # container for text box
            textcontainer = st.container()

            with textcontainer:
                query = st.chat_input("Query: ", key="input")
                if query:
                    with st.spinner("typing..."):

                        ans = agent_executor.invoke(query)
                        response = ans["output"]

                    st.session_state.requests.append(query)
                    st.session_state.responses.append(response)
                
            with response_container:
                if st.session_state['responses']:
                    # Display chat history
                    for i in range(len(st.session_state['responses'])):
                        message(st.session_state['responses'][i], key=str(i))
                        if i < len(st.session_state['requests']):
                            message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')


if __name__ == "__main__":
    main()









