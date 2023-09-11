import openai
import streamlit as st
import vectorSearch
from datetime import date

st.title("Nottingham GPT")

st.balloons()

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        welcome_message = "Hi! Welcome to UNNC🥰"
        st.markdown(welcome_message)
        st.st.session_state.messages.append({"role":"assistant", "content": welcome_message})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # 多轮对话语义补全





        # 获取参考文本
        reference = vectorSearch.getReference(prompt)
        print(reference)

        today =  date.today()   

        system_prompt = f"今天是{today}。你是宁波诺丁汉大学的热心的AI助手，你知道一切关于宁波诺丁汉大学的信息。\n以下是用于回答此问题的参考内容:\n{reference}\n\n根据以上信息,请简要回答用户接下来的问题。确保回答有意义且符合道德规范。" 
        system_msg = {"role": "system", "content": system_prompt}
        messages.insert(0, system_msg)

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
