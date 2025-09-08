from typing import Optional, List, Tuple
from agents import Runner, InputGuardrailTripwireTriggered
from src.refiner.types import RefiningResponse
from src.refiner.interfaces import IAgent, IRunner


class RefiningAgentRunner:
    def __init__(self, agent: Optional[IAgent] = None, runner: type[IRunner] = Runner):
        self.agent = agent
        self.runner = runner

    async def run(self, user_input: str) -> Tuple[bool, Optional[List[dict]]]:
        trying_to_over_eat = False
        questions_list: Optional[List[dict]] = None

        try:
            if self.agent:
                res: RefiningResponse = (
                    await self.runner.run(self.agent, input=user_input)
                ).final_output
                questions_list = [x.model_dump() for x in res.questions]
        except InputGuardrailTripwireTriggered:
            trying_to_over_eat = True

        return trying_to_over_eat, questions_list
