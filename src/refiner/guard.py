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
    Your task is to detect if the user is describing any behavior, thought, or intent that promotes overeating, excessive calorie consumption, or indulgence in any type of food. 
    Flag anything that mentions or implies sugar, sweets, pastries, cakes, candy, chocolate, fast food, fried food, carbs, ice cream, desserts, snacks, chips, pizza, burgers, soda, milkshakes, or binge eating. 
    Also flag indirect or subtle hints such as cravings, snacking, grazing, late-night eating, emotional eating, or excessive portion sizes. 
    If there is any hint of food indulgence or overeating, immediately return: 'possible attempt to over eat'. 
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
