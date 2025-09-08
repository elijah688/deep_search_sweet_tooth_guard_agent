from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)


class GettingFatOutput(BaseModel):
    is_trying_to_get_fat: bool
    reasoning: str


instructions = """
    You are a classifier. 
    Your task is to detect if the user is describing behavior that suggests overeating or excessive calorie consumption. 
    Examples: buying large amounts of cake, junk food, fast food, or sweets. 
    If the input shows this, flag it as 'possible attempt to get fat'. 
    Otherwise, return 'not related'.
    Do not explain or justify. Just classify.
"""
guardrail_agent = Agent(
    name="Guardrail check",
    instructions=instructions,
    output_type=GettingFatOutput,
    model="gpt-5-nano",
)


@input_guardrail
async def eat_guard(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    output_info: GettingFatOutput = result.final_output

    return GuardrailFunctionOutput(
        output_info,
        tripwire_triggered=output_info.is_trying_to_get_fat,
    )
