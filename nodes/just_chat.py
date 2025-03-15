# nodes/just_chat.py
from langchain_core.messages import AIMessage, RemoveMessage
from config.llm_models import llm_openai
from utils.text_refinator_util import clean_text
from functions.handle_whatsapp_message import handle_whatsapp_message
from tools.just_call_tools import JUST_CALL_TOOLS


def just_chat_node(state):
    state.update(handle_whatsapp_message(state))
    valid_message = [m for m in state["messages"] if not isinstance(m, RemoveMessage)]
    llm_with_tools = llm_openai.bind_tools(JUST_CALL_TOOLS)
    response = llm_with_tools.invoke(valid_message)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            tool = next((t for t in JUST_CALL_TOOLS if t.name == tool_name), None)
            if tool:
                tool_result = tool.func(**tool_args)
                clean_response = clean_text(tool_result)
                state["messages"].append(AIMessage(content=clean_response))
            else:
                state["messages"].append(AIMessage(content="Error: herramienta no encontrada."))
    else:
        clean_response = clean_text(response.content)
        state["messages"].append(AIMessage(content=clean_response))

    return state
