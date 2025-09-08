from typing import List
from src.deep_research.web_research_designer.types import (
    ClarifyingQA,
    DesignerResponse,
    SEARCH_TERM_SIZE,
)
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from openai import AsyncOpenAI


def __generate_instructions(topic: str, clarifying_qas: List[ClarifyingQA]) -> str:
    qa_pairs = "\n".join([f"Q: {qa.question} A: {qa.answer}" for qa in clarifying_qas])
    instructions = (
        f"You are a web search question generator agent.\n"
        f"Topic: {topic}\n"
        f"Use the following clarifying Q&A to guide your question generation:\n"
        f"{qa_pairs}\n"
        f"Generate exactly {SEARCH_TERM_SIZE} relevant web search questions."
    )
    return instructions


@function_tool
async def research_designer_agent(
    topic: str, clarifying_qas: List[ClarifyingQA]
) -> DesignerResponse:
    """Generates web search questions for a topic
    using clarifying Q&A pairs.
    Produces focused, research-ready questions to
    support structured and efficient web research workflows.
    """

    agent: Agent = Agent(
        instructions=__generate_instructions(
            topic=topic, clarifying_qas=clarifying_qas
        ),
        name="Research Designer Agent",
        model=OpenAIChatCompletionsModel(
            openai_client=AsyncOpenAI(),
            model="gpt-5-nano",
        ),
        output_type=DesignerResponse,
    )

    res = await Runner.run(
        agent,
        input=topic,
    )

    return res.final_output
