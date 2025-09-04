# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.prompts.chat import (
#     ChatPromptTemplate,
#     HumanMessagePromptTemplate,
#     SystemMessagePromptTemplate,
# )
# from langchain_openai import ChatOpenAI
# from langchain_community.llms import VLLMOpenAI
# import asyncio

# from transformers import AutoTokenizer

# inference_server_url = "http://129.254.177.83:8000/v1/"

# llm_core = ChatOpenAI(
#     model="meta-llama/Llama-3.1-70B-Instruct",
#     openai_api_key="EMPTY",
#     #max_tokens=16000,
#     openai_api_base=inference_server_url,
#     temperature=0,
#     model_kwargs={"top_p": 1}
# )

# tokenizer = AutoTokenizer.from_pretrained("gpt2")

# def text_generate_llama3(text):
#     if len(tokenizer.tokenize(text)) >= 12500:
#         return "ERROR:OOL" # out of length (token limit overflow)
#     else:
#         messages = [
#             SystemMessage(
#                 content="You are a coding assistent."
#             ),
#             HumanMessage(
#                 content=text
#             ),
#         ]
#         response = llm_core.invoke(messages).content
#         return response
    
# def llm(text):
#     return text_generate_llama3(text)


import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#llm_core = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
llm_core = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def llm(prompt) -> str:
    return llm_core.invoke(prompt).content
