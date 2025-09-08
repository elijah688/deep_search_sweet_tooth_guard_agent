from src.refiner.eat_guard import eat_guard

from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI


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


refining_agent = Agent(
    instructions=(
        "You are a Refining agent. "
        "When a user submits a query, do not answer it directly. "
        "Always respond with exactly 3 Refining questions—no more, no less. "
        "Questions must be short, precise, and probing. "
        "Each question must include a 'reason' explaining why it is needed. "
        "The output must strictly follow this Pydantic structure:\n"
        "RefiningResponse(questions=[RefiningQuestion(reason='...', question='...'), ...])"
    ),
    name="gpt-5-nano Refining Agent",
    model=OpenAIChatCompletionsModel(
        openai_client=AsyncOpenAI(),
        model="gpt-5-nano",
    ),
    input_guardrails=[eat_guard],
    output_type=RefiningResponse,
)
