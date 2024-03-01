import streamlit as st
      

# st.title("Testing Purpose")





from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from streamlit_chat import message
import os
import streamlit as st

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


api= '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'
llm = ChatOpenAI(api_key=api,model='gpt-3.5-turbo')

def main():

    st.header("Ask your CSV 📈")

    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:

        agent_executor = create_csv_agent(
            llm,
            csv_file,
            agent_type="openai-tools",
            verbose=True
        )

    t1,t2,t3 = st.tabs(['Chat With PDF data','Chat with CSV data'])

    with t1:
        st.write("Tab 1 code ")

    with t2:
        st.write("Tab 2 code ")


    if st.checkbox('Submit & Process'):
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

