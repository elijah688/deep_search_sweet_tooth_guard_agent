import pytest
from src.refiner.runner import RefiningAgentRunner
from src.refiner.types import RefiningResponse, RefiningQuestion


class FakeAgent:
    name = "fake-agent"


qs = [
    RefiningQuestion(question="Q1?", reason="R1"),
    RefiningQuestion(question="Q2?", reason="R2"),
    RefiningQuestion(question="Q3?", reason="R3"),
]


class FakeRunner:
    @staticmethod
    async def run(agent, input):
        class Result:
            final_output = RefiningResponse(questions=qs)

        return Result()


@pytest.mark.asyncio
async def test_refining_runner():
    runner = RefiningAgentRunner(agent=FakeAgent(), runner=FakeRunner)

    overeat, questions = await runner.run("test input")

    assert overeat is False
    assert questions is not None
    assert len(questions) == 3
    for i, q in enumerate(questions):
        assert qs[i].model_dump()["question"] == q.model_dump()["question"]
        assert qs[i].model_dump()["reason"] == q.model_dump()["reason"]
