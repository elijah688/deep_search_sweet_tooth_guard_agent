from pydantic import BaseModel, Field, field_validator
from typing import List


class ResearcherReport(BaseModel):
    summary: str = Field(..., description="A concise summary of the input information")
    markdown_formatted: str = Field(
        ..., description="Input content reformatted in Markdown style"
    )
    follow_up_questions: List[str] = Field(
        ..., description="List of follow-up questions for further research"
    )

    @field_validator("follow_up_questions")
    @classmethod
    def max_three_questions(cls, v: List[str]):
        if len(v) > 3:
            raise ValueError(
                f"follow_up_questions can have at most 3 items, got {len(v)}"
            )
        return v
