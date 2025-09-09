from typing import List
from pydantic import BaseModel, Field, field_validator

SEARCH_TERM_SIZE = 3


class ClarifyingQA(BaseModel):
    """
    Represents a single clarifying question and its corresponding answer.
    """

    question: str = Field(
        ..., description="The clarifying question text provided to the user."
    )
    answer: str = Field(
        ..., description="The user's answer to the clarifying question."
    )


class WebSearchItem(BaseModel):
    """
    Represents a single web search question along with the research designer's reasoning for why it was generated.
    """

    question: str = Field(
        ..., description="The web search question to be used in the web search"
    )
    reason: str = Field(
        ...,
        description="Justification or rationale explaining why this question is important to the reasearch.",
    )


class DesignerResponse(BaseModel):
    """
    Represents the response containing exactly `SEARCH_TERM_SIZE` web search questions.
    """

    items: List[WebSearchItem] = Field(
        ...,
        min_length=SEARCH_TERM_SIZE,
        max_length=SEARCH_TERM_SIZE,
        description=f"A list of {SEARCH_TERM_SIZE} web search questions, each with its justification.",
    )

    @field_validator("items")
    @classmethod
    def must_have_exactly_10(cls, v: List[WebSearchItem]):
        """
        Validates that the list of web search items contains exactly `SEARCH_TERM_SIZE` entries.

        Args:
            v (List[WebSearchItem]): The list of web search items.

        Returns:
            List[WebSearchItem]: The validated list if correct length.

        Raises:
            ValueError: If the list does not contain exactly `SEARCH_TERM_SIZE` items.
        """
        if len(v) != SEARCH_TERM_SIZE:
            raise ValueError(f"Must contain exactly {SEARCH_TERM_SIZE} items")
        return v
