from langchain_core.messages import RemoveMessage, SystemMessage, AIMessage

from functions.handle_whatsapp_message import handle_whatsapp_message
from config.llm_models import llm_openai
from prompts.company_service_atention import COMPANY_SERVICE_PROMPT
from utils.text_refinator_util import clean_text
def company_service_node(state):
    state.update(handle_whatsapp_message(state))
    valid_message = [m for m in state["messages"] if not isinstance(m, RemoveMessage)]
    response = llm_openai.invoke([SystemMessage(content=COMPANY_SERVICE_PROMPT)] + valid_message)
    text_cleaned= clean_text(response.content)
    state["messages"].append(AIMessage(content=text_cleaned))
    return state