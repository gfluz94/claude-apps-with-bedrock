import streamlit as st

from utils.bedrock import BedrockAgent, AgentType
from utils.query import build_query


if __name__ == "__main__":
    with st.sidebar:
        st.title(" Chat Configuration")
        st.header("Clear Chat History")
        if st.button("Clear Chat"):
            st.session_state.messages = []


    st.title("Chat with Bedrock")
    question = st.chat_input(placeholder="Type a message...")

    agent_type = AgentType.QA
    query = build_query(agent_type, question)
    
    agent = BedrockAgent(agent_type=AgentType.QA)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["text"])

    if question:
        st.session_state.messages.append({"role": "User", "text": question})
        with st.chat_message("User"):
            st.write(question)
        response = agent.answer(query)
        st.session_state.messages.append({"role": "Assistant", "text": response})
        with st.chat_message("Assistant"):
            st.write(response)
