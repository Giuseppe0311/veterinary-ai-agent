from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, RemoveMessage
from prompts.system_prompt import SYSTEM_PROMPT
from config.llm_models import llm_openai


def handle_whatsapp_message(state):
    system_message = SystemMessage(content=SYSTEM_PROMPT)
    messages_history = state["messages"]
    if len(messages_history) >= 10:
        last_human_message = messages_history[-1]
        summary_prompt = "Resume la conversación anterior de forma concisa, manteniendo detalles importantes."
        summary_input = [system_message] + messages_history[:-1]
        summary = llm_openai.invoke(summary_input + [HumanMessage(content=summary_prompt)])
        delete_messages = [RemoveMessage(id=m.id) for m in messages_history]
        summary_message = AIMessage(content=f"Resumen de la conversación previa: {summary.content}")
        message_updates = delete_messages + [summary_message, last_human_message]
    else:
        message_updates = [system_message] + messages_history
    return {"messages": message_updates}
