import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from pathlib import Path
from PIL import Image
import io

from utils.bedrock import BedrockAgent, AgentType
from utils.rag import KnowledgeBase
from utils.query import build_query


DOCS_BASE_PATH = Path("./docs/")
knowledge_base = KnowledgeBase(
    collection_name="rag_store",
)


def upload_pdf(file: UploadedFile) -> None:
    file_path = DOCS_BASE_PATH / file.name
    with file_path.open("wb") as f:
        f.write(file.getbuffer())


def read_image_bytes(uploaded_image: UploadedFile) -> bytes:
    image = Image.open(uploaded_image)
    img_bytes_arr = io.BytesIO()
    image.save(img_bytes_arr, format="PNG")
    return img_bytes_arr.getvalue()


if __name__ == "__main__":
    with st.sidebar:
        st.title(" Chat Configuration")
        st.header("Enable VQA")
        uploaded_image = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=False,
        )
        st.header("Enrich Knowledge Base by Adding Documents to Vector Store")
        is_rag = st.checkbox("Enable RAG")
        if is_rag:
            uploaded_file = st.file_uploader(
                "Upload a PDF file",
                type=["pdf"],
                accept_multiple_files=False,
            )
            if uploaded_file:
                upload_pdf(uploaded_file)
                knowledge_base.update(DOCS_BASE_PATH / uploaded_file.name)
        st.header("Clear Chat History")
        if st.button("Clear Chat"):
            st.session_state.messages = []


    st.title("Chat with Bedrock")
    question = st.chat_input(placeholder="Type a message...")

    agent_type = AgentType.QA

    if is_rag and question:
        agent_type = AgentType.RAG
        context = knowledge_base.retrieve(question)
        query = build_query(agent_type, question, context)

    if uploaded_image and question:
        agent_type = AgentType.IMAGE
        image_bytes = read_image_bytes(uploaded_image)
    
    query = build_query(agent_type, question)
    
    agent = BedrockAgent(agent_type=agent_type)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["text"])

    if question:
        st.session_state.messages.append({"role": "User", "text": question})
        with st.chat_message("User"):
            st.write(question)
        if agent_type == AgentType.IMAGE:
            response = agent.answer(query, image=image_bytes)
        else:
            response = agent.answer(query)
        st.session_state.messages.append({"role": "Assistant", "text": response})
        with st.chat_message("Assistant"):
            st.write(response)
