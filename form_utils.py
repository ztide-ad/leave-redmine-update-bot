from langchain_groq import ChatGroq

import requests
import os
from prompts_gform import final_prompt, json_output_parser
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:5000"

# LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

groq_api_key=os.environ['GROQ_API_KEY']

def invoke_input(user_input):
    llm=ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")
    chain = final_prompt | llm | json_output_parser
    response = chain.invoke({
        "input": user_input,
        # "chat_history": chat_history,
        "format_instructions": json_output_parser.get_format_instructions()
    })
    return response

def submit_form(form_data):
    try:
        response = requests.post(f"{API_URL}/submit", json=form_data)
        if response.status_code == 200:
            return f"Form submitted successfully."
        else:
            return f"Error submitting form. Status code: {response.status_code}, message: {response.json().get('message')}"
    except Exception as e:
        return f"Error submitting form: {str(e)}"
