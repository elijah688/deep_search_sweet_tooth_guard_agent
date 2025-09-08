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
    Your task is to detect if the user is describing behavior that promotes overeating, excessive calorie consumption, or junk food indulgence. 
    Flag anything that suggests sugar, sweets, pastries, cakes, candy, chocolate, fast food, fried food, carbs, or binge eating. 
    If there is any hint of this, immediately return: 'possible attempt to get fat'. 
    Otherwise, return: 'not related'. 
    Do not explain, justify, or qualify. Only classify.
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

    print(output_info)
    return GuardrailFunctionOutput(
        output_info,
        tripwire_triggered=output_info.is_trying_to_get_fat,
    )
