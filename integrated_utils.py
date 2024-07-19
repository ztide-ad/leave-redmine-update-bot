import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from langchain_utils import invoke_chain

from form_utils import invoke_input, submit_form
from examples_integrated import redmine_examples, form_examples, redmine_keywords, form_keywords

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similarity_score(input_text, example_texts):
    input_embedding = embedding_model.encode([input_text])[0]
    example_embeddings = embedding_model.encode(example_texts)
    
    similarity_scores = cosine_similarity([input_embedding], example_embeddings)
    
    return np.max(similarity_scores)

def determine_task(user_input):
    # Keyword matching
    # if any(keyword in user_input.lower() for keyword in redmine_keywords):
    #     return "redmine"
    # elif any(keyword in user_input.lower() for keyword in form_keywords):
    #     return "form"
    
    # Semantic similarity
    redmine_similarity = get_similarity_score(user_input, redmine_examples)
    form_similarity = get_similarity_score(user_input, form_examples)
    
    return "redmine" if redmine_similarity > form_similarity else "form"

def process_redmine(user_input):
    return invoke_chain(user_input)

def process_form(user_input):
    form_data = invoke_input(user_input)
    return submit_form(form_data)

