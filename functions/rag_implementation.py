from langchain_openai import OpenAIEmbeddings
from chains.rag_chain import create_rag_chain
from utils.document_processing import load_and_process_documents, get_faiss_index

file_paths = ["./docs/company_atention.txt", "./docs/company_story.txt"]
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


def rag_implementation(quest):
    docs = load_and_process_documents(file_paths)
    print("---DOCS---")
    print(docs)
    faiss_index = get_faiss_index(docs, embeddings, "faiss_index")
    rag_chain = create_rag_chain(faiss_index)
    response = rag_chain.invoke(quest)
    return response
