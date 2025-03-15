from langgraph.constants import END


def route_designation(state):
    if state["service_intention"] == "just_chat":
        return "just_chat"
    elif state["service_intention"] == "company_information":
        return "company_information"
    elif state["service_intention"] == "company_service":
        return "company_service"
    else:
        return END
