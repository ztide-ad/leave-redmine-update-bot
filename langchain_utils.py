import os
import re
import json
import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
from prompts_redmine import final_prompt, json_output_parser

from langchain_groq import ChatGroq
# from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import LLMChain

load_dotenv()

# LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Groq Inference Engine
groq_api_key=os.environ['GROQ_API_KEY']

REDMINE_URL = "http://localhost:80"
REDMINE_API_KEY = "1061e0df14b13cd320c769a78f6c30c9b53ad370"

def extract_issue_id(user_input):
    match = re.search(r'issue (?:ID|id) (\d+)', user_input)
    return match.group(1) if match else None

def invoke_chain(user_input):
    issue_id = extract_issue_id(user_input)
    if not issue_id:
        return "Error: Issue ID not found in the input."

    

    llm=ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")
    chain = LLMChain(llm=llm, prompt=final_prompt, output_parser=json_output_parser)

    response = chain.run(
        input=user_input,
        # chat_history=messages,
        format_instructions=json_output_parser.get_format_instructions()
    )

    if isinstance(response, dict):
        json_data = response
    else:
        return f"Error: Invalid JSON response from LLM. Details: {str(json.JSONDecodeError)}"

    if 'issue' not in json_data:
        json_data = {'issue': json_data}
    json_data["issue"]["id"] = int(issue_id)

    # Remove any None or empty string values
    json_data["issue"] = {k: v for k, v in json_data["issue"].items() if v not in (None, "")}

    json_data_str = json.dumps(json_data, indent=2)

    headers = {"Content-Type": "application/json", "X-Redmine-API-Key": REDMINE_API_KEY}
    url = f"{REDMINE_URL}/issues/{issue_id}.json"

    try:
        api_response = requests.put(url, headers=headers, data=json_data_str)
        api_response.raise_for_status() 
        
        if api_response.status_code == 204:
            return "Success: Issue updated successfully."
        else:
            return "Success: Issue updated successfully."
    except RequestException as e:
        return f"Error: Failed to update issue. Details: {str(e)}"

# def create_history(messages):
#     history = ChatMessageHistory()
#     for message in messages:
#         if message["role"] == "user":
#             history.add_user_message(message["content"])
#         else:
#     return history

