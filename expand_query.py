import getpass
import os
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI  # Use your preferred LLM
from langchain_openai import ChatOpenAI
import warnings
#Turn off warnings
warnings.filterwarnings("ignore")
if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


model = ChatOpenAI(model="gpt-4o-mini")

def generate_prompts(user_questions):
    system_message = "You are an expert in all matters software and you are a senior in your team.\
        You receive questions from your team members and your job is to think about different ways of formulating question\
        Put every question in a new line. Do not start the question with non needed text like: Here is what I gathered.\
        Just provide the new question.\
        Do not add any information that is not related to the question, just output the question."
    system_message_prompt =  SystemMessagePromptTemplate.from_template(system_message)
    human_question = "{question}"
    query = f'{user_questions}'
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_question)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = chat_prompt | model
    response = chain.invoke({"question":query})
    queries = response.content.split('\n')
    return queries

def generate_answers(user_question, documents):
   system_message = """
    You are an expert in all matters software and you will help me find answers to my questions based on the documents I will be sending you.
    You should only output factual results.
    If you do not know or if you are unsure, you should say so and you should not make up answers.
    I also do not want you to produce summerised answered and I want you to reference parts of the documents in your response.
    And I want you to speak as if you are the owner of the document.
    """
   human_message = """
    Here is my question: {query}
    Below are the documents you need to use:
    {documents}
    """
   system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
   human_message_prompt = HumanMessagePromptTemplate.from_template(human_message)

   chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
   chain = chat_prompt | model
   response = chain.invoke(
      {
         "query": " ".join(user_question),
        "documents": "".join(documents)
      }
    )
   return response