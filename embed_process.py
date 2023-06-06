from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from config import get_openai_key, setup_logging
import os

# Set up environment variables
OPENAI_API_KEY = get_openai_key()

# Set up logging
logger = setup_logging()

def embed_index(docs, embed_fn, index_store):
    try:
        faiss_db = FAISS.from_documents(docs, embed_fn)
        if os.path.exists(index_store):
            local_db = FAISS.load_local(index_store,embed_fn)
            local_db.merge_from(faiss_db)
            logger.info("Merge completed")
            local_db.save_local(index_store)
            logger.info("Updated index saved")
        else:
            faiss_db.save_local(folder_path=index_store)
            logger.info("New store created...")

    except Exception as e:
        logger.error(f"Failed to create or update index. Error: {str(e)}")

def embed_docs(documents):
    try:
        text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        # select which embeddings we want to use
        embeddings = OpenAIEmbeddings()
        # create the vectorestore to use as the index
        index_store = 'data/indexes/global_index'
        embed_index(docs, embeddings, index_store)
        logger.info(f"Successfully processed documents.")
    except Exception as e:
        logger.error(f"Failed to process documents. Error: {str(e)}")
