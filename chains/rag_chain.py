from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(faiss_index):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    prompt_template = ChatPromptTemplate.from_template(
        "Based on the following information, answer the question: {question}\n\nInformation: {context}"
    )
    retriever = faiss_index.as_retriever(search_kwargs={"k": 2})
    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template
            | llm
    )
    return rag_chain
