#if we want to add something in the book we can 
from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain_community.embeddings import HuggingFaceEmbeddings  # Updated import
import pinecone
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Ensure that PINECONE_API_KEY is set in your environment
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in the environment.")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment="us-east-1")

# Define the function to load PDF using PyPDFLoader
def load_pdf_file(data):
    loader = PyPDFLoader(data)  # Use PyPDFLoader directly for a single file
    documents = loader.load()  # Load the PDF as documents
    return documents

# Load the PDF file
extracted_data = load_pdf_file(data='C:/Users/ANURITI/Downloads/Medical_book.pdf')

# Split the extracted data into chunks (assuming text_split is implemented in your helper)
text_chunks = text_split(extracted_data)

# Download Hugging Face embeddings (make sure the model path is correct)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create the Pinecone index if it doesn't exist already
index_name = "medicalbot"

# Check if the index already exists
if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        name=index_name,
        dimension=384,  # Ensure that the dimension matches the embeddings
        metric="cosine",
    )

# Connect to the Pinecone index
index = pinecone.Index(index_name)

# Prepare the data to be upserted into Pinecone
upsert_data = [
    (str(i), embedding.embed(text_chunk), {}) for i, text_chunk in enumerate(text_chunks)
]

# Upsert data into Pinecone index
index.upsert(vectors=upsert_data)

print("Data successfully upserted into Pinecone.")
