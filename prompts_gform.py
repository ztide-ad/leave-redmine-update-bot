from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
# from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.embeddings import OllamaEmbeddings

from examples_gform import examples
from typing import List
import json

class FormResponse(BaseModel):
    days: str = Field(description="Number of days will be on leave 1 to 5")
    reason: str = Field(description="A short description of the leave")
    type: str = Field(description="Type of leave (Casual Leave, Medical Leave)")

json_output_parser = JsonOutputParser(pydantic_object=FormResponse)

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}\nJSON:"),
    ("ai", "{json}"),
])

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

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    input_variables=["input"],
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in interpreting natural language descriptions and converting them into structured form responses for issue tracking. Return only the JSON object without any wrapper or additional text."),
    few_shot_prompt,
    # MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}\n{format_instructions}"),
])
