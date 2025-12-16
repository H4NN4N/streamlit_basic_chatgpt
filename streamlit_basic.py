import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="한나의 챗봇", page_icon="💬")
st.markdown(
    """
    <style>
    /* 전체 채팅 영역 */
    .stChatMessage {
        margin-bottom: 0.75rem;
    }

    /* assistant 말풍선 */
    .stChatMessage[data-testid="assistant"] {
        background-color: #f1f3f6;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        max-width: 80%;
    }

    /* user 말풍선 */
    .stChatMessage[data-testid="user"] {
        background-color: #dcf8c6;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-left: auto;
        max-width: 80%;
    }

    /* 텍스트 공통 */
    .stChatMessage p {
        margin: 0;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    .stApp {
        background-color: #ddf6b6;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# (0) 사이드바에서 api_key 입력하는 부분
with st.sidebar:
    openai_api_key = os.getenv('OPENAI_API_KEY')
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


st.title("💬 한나의 챗봇 ")

st.markdown(
    """
    <div style="
        padding: 1rem;
        border-radius: 10px;
        background-color: #f7eddd;
        margin-bottom: 1rem;
    ">
        🤖 <strong>한나의 챗봇</strong><br>
        궁금한 것을 자유롭게 질문해 주세요.
    </div>
    """,
    unsafe_allow_html=True
)



# (1) st.session_state에 "messages"가 없으면 초기값을 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "어떻게 도와드릴까요?"}]

# (2) 대화 기록을 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# (3) 사용자 입력을 받아 대화 기록에 추가하고 AI 응답을 생성
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt}) 
    st.chat_message("user").write(prompt) 
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages) 
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg}) 
    st.chat_message("assistant").write(msg)
