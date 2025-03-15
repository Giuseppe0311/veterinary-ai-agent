import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

def load_and_process_documents(file_paths):
    documents = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe.")
        loader = TextLoader(file_path)
        documents.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    return docs

def get_faiss_index(docs, embeddings, index_dir):
    if os.path.exists(index_dir):
        print("Cargando índice FAISS existente...")
        return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    print("Creando nuevo índice FAISS...")
    library = FAISS.from_documents(docs, embeddings)
    library.save_local(index_dir)
    return library