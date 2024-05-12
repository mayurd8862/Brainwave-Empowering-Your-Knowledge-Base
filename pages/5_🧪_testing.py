from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain.chains.summarize import load_summarize_chain
# import os
# import tempfile

# Securely provide your Google API key (not shown here)
# llm = ChatGoogleGenerativeAI(model="gemini-pro")
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
# print(llm("who is the prime minister of india"))

messages = [
    ("system", "You are a helpful assistant that translates English to French."),
    ("human", "Translate this sentence from English to French. I love programming."),
]
llm.invoke(messages)