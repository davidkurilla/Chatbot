# Imports
import os
from groq import Groq
import streamlit as st

# Get API Key
API_KEY = os.environ["api_key"]

# Configure client
client = Groq(
  api_key = API_KEY,
)

# Define chat function
def prompt_groq(prompt):
  
  try:
  
    chat_completion = client.chat.completions.create(
      messages = [
        {
          "role": "user",
          "content": prompt,
        }
      ],
      model = "llama3-8b-8192",
    )
  
    return chat_completion.choices[0].message.content

  except Exception as e:
    print(e)
    return "SYSTEM ERROR - Could not get response from Groq"

# Setup UI for Streamlit
st.title("Pieces Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me a question?"):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = prompt_groq(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
