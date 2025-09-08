# agent_factory.py
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from src.refiner.types import RefiningResponse
from src.refiner.eat_guard import eat_guard

INSTRUCTIONS = (
    "You are a Refining agent. "
    "When a user submits a query, do not answer it directly. "
    "Always respond with exactly 3 Refining questions—no more, no less. "
    "Questions must be short, precise, and probing. "
    "Each question must include a 'reason' explaining why it is needed. "
    "The output must strictly follow this Pydantic structure:\n"
    "RefiningResponse(questions=[RefiningQuestion(reason='...', question='...'), ...])"
)


def spawn_refining_agent() -> Agent:
    return Agent(
        instructions=INSTRUCTIONS,
        name="gpt-5-nano Refining Agent",
        model=OpenAIChatCompletionsModel(
            openai_client=AsyncOpenAI(),
            model="gpt-5-nano",
        ),
        input_guardrails=[eat_guard],
        output_type=RefiningResponse,
    )
