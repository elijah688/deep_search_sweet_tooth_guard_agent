from typing import Protocol, Any


class IAgent(Protocol):
    """Any class that can be used as an Agent."""

    name: str


class IRunner(Protocol):
    """Any runner that knows how to run an agent with input and return a RefiningResponse."""

    @staticmethod
    async def run(agent: IAgent, input: str) -> Any: ...
