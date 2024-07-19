from typing import Optional
from examples_redmine import examples

import json
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.embeddings import OllamaEmbeddings
import streamlit as st

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.prompts import MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nJSON:"),
        ("ai", "{json}"),
    ]
)

@st.cache_resource
def get_example_selector():
    flattened_examples = []
    for example in examples:
        flattened_example = {
            "input": example["input"],
            "json": json.dumps(example["json"])
        }
        flattened_examples.append(flattened_example)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        flattened_examples,
        OllamaEmbeddings(model='llama3'),
        Chroma,
        k=2,
        input_keys=["input"],
    )
    return example_selector

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=get_example_selector(),
    input_variables=["input"],
)

class Issue(BaseModel):
    priority_id: Optional[int] = Field(None, description="Priority ID of the issue. 1 for low, 2 for normal, 3 for high, 4 for immediate, 5 for urgent")
    subject: Optional[str] = Field(None, description="Subject of the issue")
    description: Optional[str] = Field(None, description="Description of the issue")
    status_id: Optional[int] = Field(None, description="Status ID of the issue. 1 for new, 2 for in progress, 3 for in UAT, 5 for closed, 9 for ready for tech, 3 for In UAT, 5	for Closed, 6 for Abandoned, 7 for Reopened, 8 for Brainstorming")
    assigned_to_id: Optional[int] = Field(None, description="ID of the user assigned to the issue")
    due_date: Optional[str] = Field(None, description="Due date of the issue in YYYY-MM-DD format")
    done_ratio: Optional[int] = Field(None, description="Percentage of completion for the issue")
    estimated_hours: Optional[float] = Field(None, description="Estimated hours for the issue")


class IssueUpdate(BaseModel):
    issue: Issue = Field(description="Issue details to be updated")

json_output_parser = JsonOutputParser(pydantic_object=IssueUpdate)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert in generating JSON structures from natural language commands. Only include the fields that the user has input no need to include all the fields leave them as null. Return only the JSON object without any wrapper or additional text."),
        few_shot_prompt,
        # MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}\n{format_instructions}"),
    ]
)

