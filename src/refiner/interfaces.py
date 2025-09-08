from typing import Protocol
from src.refiner.types import RefiningResponse


class IAgent(Protocol):
    """Any class that can be used as an Agent."""

    name: str


class IRunnerResult(Protocol):
    """The result object returned from IRunner.run"""

    final_output: RefiningResponse


class IRunner(Protocol):
    """Any runner that can run an agent with input and return a result with .final_output"""

    @staticmethod
    async def run(agent: IAgent, input: str) -> IRunnerResult: ...
