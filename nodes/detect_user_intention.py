from langchain_core.messages import SystemMessage, HumanMessage
from config.llm_models import llm_openai
from models.schemas import UserIntention
from prompts.intention_prompt import INTENTION_PROMPT

router_intention_llm = llm_openai.with_structured_output(UserIntention)


def detect_user_intention_node(state):
    last_human_message = state["messages"][-1]
    # Obtener la preferencia actual del estado, por defecto "audio" si no existe
    current_preferred_response = state.get("preferred_response", "audio")

    # Formatear el prompt con la preferencia actual
    formatted_prompt = INTENTION_PROMPT.format(current_preferred_response=current_preferred_response)

    # Invocar al LLM con el prompt actualizado
    user_intention = router_intention_llm.invoke(
        [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content=last_human_message.content)
        ]
    )

    print("-----USER INTENTION-----")
    print(user_intention.intention)
    print("-----PREFERRED RESPONSE-----")
    print(user_intention.preferred_response)

    return {
        "service_intention": user_intention.intention,
        "preferred_response": user_intention.preferred_response
    }
