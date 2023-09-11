import openai
import streamlit as st
import vectorSearch
from datetime import date

bg_css = """  
<style>
.stApp {
  background-image: url('https://images.unsplash.com/photo-1630438325568-69fc918b27cc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3131&q=80');
  background-size: cover;
  background-attachment: fixed;
}
</style>
"""

st.markdown(bg_css, unsafe_allow_html=True)

st.title("Nottingham GPT")

st.balloons()

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Welcome to Nottingham🥰"}]

if prompt := st.chat_input("what's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
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
