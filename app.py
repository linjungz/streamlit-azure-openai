import streamlit as st
import random
import time
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_API_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

system_prompt = {"role":"system","content":"You are an AI assistant that helps people find information."}

st.title('GPT Bot Demo')

#init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is up"):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        history_to_keep = 10
        message_history = [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
        messages = [system_prompt] + message_history[-history_to_keep:]
        print(messages)

        message_placeholder = st.empty()
        full_response = ""

        for response in openai.ChatCompletion.create(
            engine=os.environ.get("AZURE_OPENAI_API_DEPLOYMENT"),
            messages=messages,
            temperature=0,
            max_tokens=2000,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None,
            stream=True
        ):
            if response.choices and 'delta' in response.choices[0] and 'content' in response.choices[0].delta:
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")


        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})


