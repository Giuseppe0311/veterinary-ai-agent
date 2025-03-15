from typing import TypedDict, Literal, Annotated, Any, Union
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from nodes.detect_user_intention import detect_user_intention_node
from nodes.just_chat import just_chat_node
from nodes.company_information import get_company_information_node
from nodes.company_service import company_service_node
from functions.route_designation import route_designation


class State(TypedDict):
    messages: Annotated[list, add_messages]
    service_intention: Literal["just_chat", "appointment", "information"]
    preferred_response: Literal["audio", "text"]


def build_graph():
    graph = StateGraph(State)

    graph.add_node("detect_user_intention", detect_user_intention_node)
    graph.add_node("just_chat_node", just_chat_node)
    graph.add_node("company_information_node", get_company_information_node)
    graph.add_node("company_service_node", company_service_node)

    graph.add_edge(START, "detect_user_intention")
    graph.add_conditional_edges("detect_user_intention", route_designation, {
        "just_chat": "just_chat_node",
        "company_information": "company_information_node",
        "company_service": "company_service_node"
    })
    graph.add_edge("just_chat_node", END)
    graph.add_edge("company_information_node", END)
    graph.add_edge("company_service_node", END)

    memory = MemorySaver()
    return graph.compile(memory)


graph_compiled = build_graph()
