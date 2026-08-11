from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st 

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

st.title("QnA Bot.")
st.markdown("This is the first project in the GenAI Course.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for messages in st.session_state.messages:
    role = messages['role']
    content = messages['content']
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask your question")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({'role': 'user', 'content': query})

    response = llm.invoke(query)
    st.chat_message("ai").markdown(response.text)
    st.session_state.messages.append({'role': 'ai', 'content': response.text})