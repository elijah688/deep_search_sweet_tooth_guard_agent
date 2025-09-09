from agents import Agent

INSTRUCTIONS = """
   You are an expert researcher tasked with writing a detailed, high-quality research report.
   You will receive a query and background information prepared by junior that helps answer the query. 
   Your task is to produce a report of approximately 500 words and no more than 5 pages, in **Markdown format**, that answers the research question


    Instructions:
    1. Carefully analyze the input and plan the structure of your report **before writing**.
    2. Suggest a clear flow: introduction, main sections, conclusions, and any relevant sub-sections.
    3. Make the report coherent, logical, and comprehensive, as if for a professional audience.
    4. Return the report entirely in **Markdown**, suitable for immediate reading or publishing.
    5. Ensure the report is about **500 words** (~5 pages if formatted).
"""


class WriterAgent:
    def __init__(self, model: str = "gpt-5-nano"):
        self.model = model
        self._agent = self._create_agent()

    def _create_agent(self) -> Agent:
        return Agent(
            instructions=INSTRUCTIONS,
            name="Writer Agent",
            model=self.model,
        )

    @property
    def agent(self) -> Agent:
        return self._agent