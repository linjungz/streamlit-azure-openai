import streamlit as st
import random
import time
from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)


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

        response = client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_API_DEPLOYMENT"),
            messages=messages,
            temperature=0,
            max_tokens=2000,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None,
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += (chunk.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})


