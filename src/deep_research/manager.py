from src.deep_research.web_research_designer.types import (
    ClarifyingQA,
)
from src.deep_research.web_research_designer.designer import research_designer_agent
from openai.types.responses import ResponseTextDeltaEvent
from src.deep_research.web_research_executor.executor import web_search
from src.deep_research.report_writer.report_writer import WriterAgent
from src.deep_research.report_writer.types import ResearcherReport
from agents import Agent, Runner
from typing import List
from collections.abc import AsyncGenerator

INSTRUCTIONS = """
    You are the Manager agent. Your role is to coordinate the research workflow from start to finish.

    Workflow:
    1. You will receive a topic, a set of follow-up questions, and the user's answers to those questions.
    2. First, call the `designer` to generate a set of focused web search queries based on the topic and clarifying Q&A.
    3. Next, use the `web_search` tool to execute those queries and gather relevant information from the internet.
    4. Finally, pass the collected research results into the `report_writer` tool to produce a structured report

    Your responsibility is to manage the flow of information between tools and ensure the output is coherent, accurate, and ready for use by the researcher.
    """


class DeepResearchManager:
    def __init__(self):
        self._agent = self._create_agent()

    def _create_agent(self) -> Agent:
        report_writer = WriterAgent().agent.as_tool(
            tool_name="report_writer",
            tool_description="Generates a structured ~500-word Markdown research report answering a query using provided background information. Returns a separate summary, three follow-up questions, and the full report with clear flow and professional quality.",
        )
        return Agent(
            instructions=INSTRUCTIONS,
            name="Manager",
            model="gpt-4o-mini",
            output_type=ResearcherReport,
            tools=[research_designer_agent, web_search, report_writer],
        )

    async def stream(
        self, topic: str, clarifying_qas: List[ClarifyingQA]
    ) -> AsyncGenerator[str, None]:
        qa_text = "\n".join([f"Q: {q.question}\nA: {q.answer}" for q in clarifying_qas])
        input_str = f"""
        Topic: {topic}

        Clarifying Questions and Answers:
        {qa_text}
        """

        if self.agent:
            result = Runner.run_streamed(self.agent, input=input_str)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(
                    event.data, ResponseTextDeltaEvent
                ):
                    yield event.data.delta

    @property
    def agent(self) -> Agent:
        return self._agent
