from typing import Optional, Tuple
from agents import Runner, InputGuardrailTripwireTriggered, Agent
from src.refiner.types import RefiningResponse


class RefiningAgentRunner:
    def __init__(self, agent: Optional[Agent] = None, runner: Runner = Runner()):
        self.agent = agent
        self.runner = runner

    async def run(self, user_input: str) -> Tuple[bool, Optional[RefiningResponse]]:
        trying_to_over_eat = False
        questions_list: Optional[RefiningResponse] = None

        try:
            if self.agent:
                questions_list = (
                    await self.runner.run(self.agent, input=user_input)
                ).final_output
        except InputGuardrailTripwireTriggered:
            trying_to_over_eat = True

        return trying_to_over_eat, questions_list
