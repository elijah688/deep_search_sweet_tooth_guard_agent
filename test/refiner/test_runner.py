import pytest
from src.refiner.runner import RefiningAgentRunner
from src.refiner.types import RefiningResponse, RefiningQuestion


class FakeAgent:
    name = "fake-agent"


class FakeRunner:
    @staticmethod
    async def run(agent, input):
        class Result:
            final_output = RefiningResponse(
                questions=[
                    RefiningQuestion(question="Q1?", reason="R1"),
                    RefiningQuestion(question="Q2?", reason="R2"),
                    RefiningQuestion(question="Q3?", reason="R3"),
                ]
            )
        return Result()


@pytest.mark.asyncio
async def test_refining_runner():
    runner = RefiningAgentRunner(agent=FakeAgent(), runner=FakeRunner)

    overeat, questions = await runner.run("test input")

    assert overeat is False
    assert questions is not None
    assert len(questions) == 3
    for q in questions:
        assert "question" in q
        assert "reason" in q
