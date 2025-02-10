# Medical-Chatbot-

# End-to-End Medical Chatbot Using Generative AI

## Overview
This project is an end-to-end **Medical Chatbot** that utilizes **Generative AI** for answering medical queries. The chatbot integrates **Flask**, **LangChain**, **Pinecone**, and **OpenAI** (Groq API) to provide intelligent, context-aware responses.

## Tech Stack
- **Flask**: Used for building the backend API and serving the chatbot.
- **LangChain**: Implements Retrieval-Augmented Generation (RAG) to enhance chatbot responses.
- **Pinecone**: Vector database for storing and retrieving embeddings efficiently.
- **OpenAI (Groq API)**: Provides the large language model for generating responses.

## Features
- **End-to-end pipeline**: Handles user queries from input processing to response generation.
- **Retrieval-Augmented Generation (RAG)**: Enhances accuracy by retrieving relevant context before generating responses.
- **Pinecone Integration**: Enables fast and scalable vector search.
- **Flask API**: Serves as the backend for interaction.

## Installation
```bash
# Clone the repository
git clone https://github.com/your-username/medical-chatbot.git
cd medical-chatbot

# Create a virtual environment
python -m venv medibot-env
source medibot-env/bin/activate  # On Windows use 'medibot-env\Scripts\activate'

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables
Create a `.env` file and add the following:
```
PINECONE_API_KEY=your_pinecone_api_key
OPENAI_API_KEY=your_openai_api_key  # Or Groq API Key
```

## Run the Application
```bash
flask run
```
The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints
- `POST /chat` - Accepts user input and returns a generated medical response.

## Usage Example
```python
import requests

url = "http://127.0.0.1:5000/chat"
data = {"query": "What is Acromegaly and Gigantism?"}
response = requests.post(url, json=data)
print(response.json())
```

## Deployment
The chatbot can be deployed on platforms like **AWS, Google Cloud, or Azure** using Flask and a suitable web server (e.g., Gunicorn).

## License
This project is licensed under the MIT License.

