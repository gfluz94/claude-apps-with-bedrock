# Building LLM Solutions with AWS Bedrock

## Overview
This repository explores the capabilities of **Claude 3.5** via **AWS Bedrock** within a **Streamlit** application. 

The project aims to experiment with:
- **Raw conversational AI**
- **Tool usage** (function calling, APIs, etc.)
- **Retrieval-Augmented Generation (RAG)**
- **Multimodal AI** (Visual Question Answering - VQA)

## Features
- **Conversational Chatbot**: A basic chat interface to interact with Claude 3.5.
- **Tool Usage**: Implementing function calling for AI-assisted automation.
- **RAG Integration**: Enhancing responses using external knowledge sources.
- **Multimodal Capabilities**: Using VQA to process and analyze images.

## Setup & Installation
### Prerequisites
- Python 3.9+
- AWS credentials with access to **Bedrock**
- A Streamlit-compatible environment

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/gfluz94/claude-apps-with-bedrock.git
   cd claude-apps-with-bedrock
   ```

2. Create a virtual environment:
    ```sh
    python3.11 -m venv ~/.llm
    source ~/.llm/bin/activate
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Usage
1. Configure AWS credentials:
    ```sh
    export AWS_ACCESS_KEY_ID=your-access-key
    export AWS_SECRET_ACCESS_KEY=your-secret-key
    export AWS_REGION=your-region
   ```

2. Run the streamlit application:
    ```sh
    streamlit run app.py
   ```

3. Access the application in your browser at http://localhost:8501.

____

🚀 Happy Experimenting with Claude 3.5 on AWS Bedrock!
