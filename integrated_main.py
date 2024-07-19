import streamlit as st
from integrated_utils import determine_task, process_redmine, process_form

st.title("Integrated LLM App")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your command:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("Processing..."):
        task = determine_task(prompt)
        if task == "redmine":
            response = process_redmine(prompt)
        elif task == "form":
            response = process_form(prompt)
        else:
            response = "Error: Could not determine the task."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
