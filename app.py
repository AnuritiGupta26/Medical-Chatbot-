from flask import Flask, render_template, request, jsonify
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing in environment variables.")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in environment variables.")

# Load Hugging Face embeddings
embeddings = download_hugging_face_embeddings()

# Define Pinecone index name
index_name = "medicalbot"

# Load Pinecone vector store
docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)

# Define retriever
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize ChatGroq
llm = ChatGroq(api_key=GROQ_API_KEY, temperature=0.4, max_tokens=500)

# Define system prompt
system_prompt = "You are a medical assistant. Answer user queries based on relevant documents."

# Create a ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("assistant", "{context}")
])

# Create question-answer chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Create RAG chain
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    print("User Input:", msg)

    # Retrieve context from Pinecone
    retrieved_docs = retriever.invoke(msg)

    # Invoke RAG chain
    response = rag_chain.invoke({
        "input": msg,
        "context": retrieved_docs
    })

    print("Response:", response["answer"])

    # Ensure JSON response is correctly formatted
    return jsonify(answer=response["answer"])


@app.route('/home')
def home():
    return "Hello, Render!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Get PORT from Render, default to 8080
    app.run(host="0.0.0.0", port=port, debug=True)