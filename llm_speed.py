from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import time
import streamlit as st

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
        return result
    return wrapper

# def time_per_100_token(content,exc_time):
#     num_tokens = llm1.get_num_tokens(content)
#     st.write(f"📜Our prompt has {num_tokens} tokens")
#     st.write(f"⏱️Execution Time: {measure_time} sec")
#     st.write(f"✅Execution time for 100 tokens is {(exc_time/num_tokens)*100}")


groq_api_key= st.secrets.GROQ_API_KEY
llm1=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")

# GOOGLE_API_KEY = st.secrets.GOOGLE_API_KEY
# llm2 = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY)

# chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
# chat = ChatGroq(temperature=0, groq_api_key="YOUR_API_KEY", model_name="mixtral-8x7b-32768")

@measure_time
def ans(query,llm):

    system = "You are a helpful assistant."
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | llm

    return chain.invoke({"text": query}).content

content =  ans("what is generative AI",llm1)
num_tokens = llm1.get_num_tokens(content)

print(f"content : {content}\n tokens: {num_tokens}")










# import streamlit as st
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# import os
# import google.generativeai as genai
# import time

# st.title("🚀Groq speed test with other LLM models")

# # Decorator for calculating execution time
# def exec_time(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         execution_time = end_time - start_time
#         st.write(result)
#         return result, execution_time
#     return wrapper


# # For Groq
# system = "You are a helpful assistant."
# human = "{text}"
# chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
# prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
# @exec_time
# def get_groq_response(inpt):
#     otpt = prompt | chat
#     return otpt.invoke({"text": inpt}).content


# # for Gemini pro
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# gemini_llm = genai.GenerativeModel("gemini-pro")
# @exec_time
# def get_gemini_response(inpt):
#     response = gemini_llm.generate_content(inpt)
#     return response.text


# # for GPT-3.5 
# from langchain_openai import OpenAI
# llm = OpenAI()
# @exec_time
# def get_openai_gpt_response(inpt):
#     result = llm.invoke(inpt)
#     return result


# def time_per_100_token(content,exc_time):
#     num_tokens = llm.get_num_tokens(content)
#     st.write(f"📜Our prompt has {num_tokens} tokens")
#     st.write(f"⏱️Execution Time: {execution_time} sec")
#     st.write(f"✅Execution time for 100 tokens is {(exc_time/num_tokens)*100}")


# input = st.text_input("Input: ",key="input")
# submit = st.button("Submit and ask question")

# if submit:
#     st.header("1. Groq's Responce")
#     output_content, execution_time = get_groq_response(input)
#     time_per_100_token(output_content, execution_time)
#     st.write("---")

#     st.header("2. OpenAI's GPT-3.5 Responce ")
#     output_content, execution_time = get_openai_gpt_response(input)
#     time_per_100_token(output_content, execution_time)
#     st.write("---")

#     st.header("3. Google's Gemini pro Responce")
#     output_content, execution_time = get_gemini_response(input)
#     time_per_100_token(output_content, execution_time)
#     st.write("---")



