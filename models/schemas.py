from typing import Literal

from pydantic import BaseModel, Field


class UserIntention(BaseModel):
    intention: Literal["just_chat", "company_service", "company_information"] = Field(
        description=
        """
        The user intention for the conversation
        """
    )
    preferred_response: Literal["audio", "text"] = Field(
        description="The preferred response type for the conversation"
    )
