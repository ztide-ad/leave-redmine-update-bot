
# Integrated NL2JSON LLM App

This application is a Natural Language to JSON (NL2JSON) chatbot designed to facilitate interaction with Redmine issue tracking and Google Forms through natural language commands. Using the LangChain framework and the power of LLMs particularly llama3, the chatbot converts user commands into structured JSON data that can be directly used to update Redmine issues or submit Google forms.


## Pre requisite

To run the LLM locally i have used ollama, so download that by first going to Ollama and download for respective OS

https://ollama.com/download

then open bash and download the model required. For this project I have used llama3 8B so will continue with that

```bash
 ollama run llama3 
```


## Installation

Install the dependencies by installing the libraries in  requirements.txt

```python
  pip install -r requirements.txt
```

## Set Up

#### 1. API Keys

Create a `.env` file and store the api keys for LangChain and LangSmith

```bash
LANGCHAIN_API_KEY = ""
LANGCHAIN_PROJECT = "Project_name" 
```
Also can include OpenAI API key, HuggingFaceHub API key

#### 2. Redmine Configuration

In the `langchain_utils.py` file set the redmine url and admin api key accordingly

```python
REDMINE_URL = ""
REDMINE_API_KEY = ""
```

#### 3. Activating Stuff

After entering the API Keys and URLs activate the API in the `gform_api.py`

```python
python gform_api.py
```

and then activate streamlit which will act as the UI for the user and the LLM to interact

```python
streamlit run integrated_main.py
```

## Documentation

### Main

#### 1. Semantic Search 

In the `examples_integrated.py` all the examples, for semantically searching and differentiating the task is present

#### 2. KeyWord Search

Is commented out but might prove useful later on if are dealing with huge  huge user inputs maybe.

In the `examples_integrated.py` all the keywords, for searching and differentiating the task is present

### Google Form

#### 1. Configuration

First create a Google Sheet and then go to Tools tab and click on create a new form. 

There create the form and then get the prefilled link.

In the url change `viewform` to `formResponse&submit=Submit`  and get the entry points of the respective the questions.

And then paste all of this in `gform_api.py` file 

e.g.

```python
form_structure = {
    "formId_url": "https://docs.google.com/forms/d/e/1FAIpQLSepBTbfwHsFCHOa4-p7wsbwC5WOTJaRBp32joacBIFwyPlCxw/formResponse",
    "form_data": {
        "entry.737578346": "days",
        "entry.726687366": "reason",
        "entry.89965788": "type"
    }
}
```
#### 2. Prompts

In the `promts_gform.py` can set up the description of each question for better LLM response.

In the `examples_gform.py` all the examples, engineering the Google Form Filler is present 

### Redmine

#### 1. Prompts

In the `promts_redmine.py` can set up the description of each question for better LLM response.

In the `examples_redmine.py` all the examples, engineering the Redmine Issue Changer is present 
