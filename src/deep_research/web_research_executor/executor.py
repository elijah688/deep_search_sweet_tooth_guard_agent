from src.deep_research.web_research_designer.types import DesignerResponse
from agents import Agent, Runner, WebSearchTool
import asyncio
from agents import function_tool
from typing import List


INSTRUCTIONS = """You are a web search agent. Always use the provided WebSearchTool to execute searches.
After retrieving results, summarize the essence of the results
- no more than 2-3 paragraphs
- use at most 300 characters.
- ignore any fluff.
- do not worry about grammar or punctuation.
"""


@function_tool
async def web_search(designer_input: DesignerResponse) -> list[str]:
    agent = Agent(
        instructions=INSTRUCTIONS,
        name="WebSearchResponse Agent",
        tools=[WebSearchTool(search_context_size="low")],
        model="gpt-5-nano",
    )
    """
    Executes web searches in parallel for all questions provided in the DesignerResponse.

    Args:
        designer_input (DesignerResponse): A structured response containing the set of web search questions.

    Returns:
        list[str]: A list of final outputs from each completed search, preserving only successful results.
    """
    res: List[str] = []
    tasks = [Runner.run(agent, input=i.question) for i in designer_input.items]
    for i, c in enumerate(asyncio.as_completed(tasks)):
        print(f"Search {i} complete....")
        res.append((await c).final_output)
    return res
