import pytest
from unittest.mock import AsyncMock
from src.refiner.runner import RefiningAgentRunner
from src.refiner.types import RefiningResponse, RefiningQuestion
from agents import Agent, Runner
from typing import List

# Example questions
qs = [
    RefiningQuestion(question="Q1?", reason="R1"),
    RefiningQuestion(question="Q2?", reason="R2"),
    RefiningQuestion(question="Q3?", reason="R3"),
]


# Minimal test agent
class MyAgent(Agent):
    name = "test-agent"


# Minimal result class to mimic runner's output
class FakeResult:
    def __init__(self, questions: List[RefiningQuestion]):
        self.final_output = RefiningResponse(questions=questions)


@pytest.mark.asyncio
async def test_refining_runner():
    agent = MyAgent("")

    # Create a Runner instance
    runner_instance = Runner()

    # Patch only the 'run' method to return our fake result
    runner_instance.run = AsyncMock(return_value=FakeResult(qs))

    # Inject our agent and patched runner
    refining_runner = RefiningAgentRunner(agent=agent, runner=runner_instance)

    overeat, questions = await refining_runner.run("test input")

    assert questions is not None

    assert overeat is False
    assert questions is not None
    assert len(qs) == 3
    for i, q in enumerate(questions.questions):
        assert qs[i].model_dump()["question"] == q.model_dump()["question"]
        assert qs[i].model_dump()["reason"] == q.model_dump()["reason"]
