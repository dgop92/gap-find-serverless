from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class AnalyzeMeetingInput(BaseModel):
    usernames: List[
        Annotated[str, Field(min_length=1, max_length=30, pattern=r"^[a-zA-Z]*$")]
    ] = Field(..., min_length=2, max_length=150)
    username_to_filter: str | None = Field(None, min_length=1, max_length=150)


class AnalyzeMeetingResult(BaseModel):
    day_index: int
    hour_index: int
    number_of_students: int
    availability: float
