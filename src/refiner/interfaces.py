from typing import Protocol, TypeVar, Optional
from agents import  RunHooks, RunConfig, Session, TResponseInputItem, RunResult
from src.refiner.types import RefiningResponse

class IAgent(Protocol):
    """Any class that can be used as an Agent."""

    name: str


class IRunnerResult(Protocol):
    """The result object returned from IRunner.run"""

    final_output: RefiningResponse

TA = TypeVar("TA")

class IRunner(Protocol[TA]):
    """Protocol representing any Runner compatible class."""

    @classmethod
    async def run(
        cls,
        starting_agent: IAgent,
        input: str | list[TResponseInputItem],
        *,
        context: Optional[TA] = None,
        max_turns: int = ...,
        hooks: Optional[RunHooks[TA]] = None,
        run_config: Optional[RunConfig] = None,
        previous_response_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        session: Optional[Session] = None,
    ) -> RunResult: ...