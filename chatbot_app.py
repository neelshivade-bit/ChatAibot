import os
import streamlit as st
from openai import OpenAI

# Load API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Chatbot", page_icon="💬")
st.title("💬 Streamlit Chatbot using OpenAI API")
st.write("Ask me anything!")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ Error: {e}"

            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
