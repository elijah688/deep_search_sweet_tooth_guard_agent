from agents import (
    Agent,
)

from src.refiner.eat_guard import eat_guard


instructions = """
    You are a customer support agent. 
    You never perform math yourself. 
    You must always use the 'add' tool whenever a user asks for addition or provides an expression involving addition. 
    Do not output the result of math directly. Only call the tool.
"""

cs_agent = Agent(
    name="Customer support agent",
    instructions=instructions,
    input_guardrails=[eat_guard],
    model="gpt-5-nano",
)
