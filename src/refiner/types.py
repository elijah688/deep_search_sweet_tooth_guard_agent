
from pydantic import BaseModel, Field
from typing import List
class RefiningQuestion(BaseModel):
    """
    Represents a single Refining question the agent asks.

    Attributes:
        reason (str): The rationale for asking this question.
        question (str): The actual question to pose to the user.
    """

    reason: str = Field(..., description="Rationale for why this question is needed")
    question: str = Field(..., description="The Refining question to ask the user")


class RefiningResponse(BaseModel):
    """
    Represents the full response from the Refining agent.

    Attributes:
        questions (List[RefiningQuestion]): Exactly 3 Refining questions.
    """

    questions: List[RefiningQuestion] = Field(
        ...,
        min_items=3,
        max_items=3,
        description="List of exactly 3 Refining questions",
    )

