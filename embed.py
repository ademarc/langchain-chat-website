from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config import setup_logging, get_openai_key
import os
import pickle
import faiss
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

# Set up logging
logger = setup_logging()

# Set up open ai api key
OPENAI_API_KEY = get_openai_key()

llm = ChatOpenAI(temperature=0)

def embed_docs(documents):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    VectorStore = save_index(docs, embeddings)
    return VectorStore

def save_index(docs, embeddings):
    vectorStore_openAI = FAISS.from_documents(docs, embeddings)
    with open("faiss_store_openai.pkl", "wb") as f:
        pickle.dump(vectorStore_openAI, f)

    with open("faiss_store_openai.pkl", "rb") as f:
        VectorStore = pickle.load(f)
    return VectorStore
