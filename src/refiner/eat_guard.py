from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)


class OverEatingOutput(BaseModel):
    is_trying_to_get_fat: bool
    reasoning: str


instructions = """
    You are a classifier. 
    Your task is to detect if the user is describing behavior that promotes overeating, excessive calorie consumption, or junk food indulgence. 
    Flag anything that suggests sugar, sweets, pastries, cakes, candy, chocolate, fast food, fried food, carbs, or binge eating. 
    If there is any hint of this, immediately return: 'possible attempt to over eat'. 
    Otherwise, return: 'not related'. 
    Do not explain, justify, or qualify. Only classify.
"""


@input_guardrail
async def eat_guard(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        Agent(
            name="Guardrail check",
            instructions=instructions,
            output_type=OverEatingOutput,
            model="gpt-5-nano",
        ),
        input,
        context=ctx.context,
    )

    output_info: OverEatingOutput = result.final_output
    return GuardrailFunctionOutput(
        output_info,
        tripwire_triggered=output_info.is_trying_to_get_fat,
    )
