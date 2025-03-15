from langchain_core.messages import RemoveMessage, AIMessage, SystemMessage, HumanMessage

from functions.handle_whatsapp_message import handle_whatsapp_message

from functions.rag_implementation import rag_implementation
from utils.text_refinator_util import clean_text
from prompts.rag_prompt_refination import RAG_PROMPT_REFINED
from config.llm_models import llm_openai


def get_company_information_node(state):
    print("-----COMPANY INFORMATION-----")
    state.update(handle_whatsapp_message(state))
    valid_message = [m for m in state["messages"] if not isinstance(m, RemoveMessage)]
    print("-----VALID MESSAGE-----")
    print(valid_message)
    refined_message = llm_openai.invoke([SystemMessage(content=RAG_PROMPT_REFINED)] + valid_message)
    print("-----REFINED MESSAGE-----")
    print(refined_message.content)
    rag_chain = rag_implementation(refined_message.content)
    print(rag_chain)
    print("-----COMPANY INFORMATION-----")
    text_cleaned = clean_text(rag_chain.content)
    state["messages"].append(AIMessage(content=text_cleaned))
    return state
