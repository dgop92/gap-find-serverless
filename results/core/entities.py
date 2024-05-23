from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class ResultsInput(BaseModel):
    usernames: List[Annotated[str, Field(min_length=1, max_length=30)]] = Field(
        ..., min_length=2, max_length=98
    )

    compute_sd: bool = False
    no_classes_day: bool = False
    ignore_weekend: bool = True

    limit: int | None = Field(None, ge=2)
    days_to_filter: List[Annotated[int, Field(ge=0, le=6)]] | None = Field(
        None, min_length=1, max_length=7
    )


class GapItem(BaseModel):
    day: str
    hour: str
    avg: float
    sd: float | None
    day_index: int
    hour_index: int
