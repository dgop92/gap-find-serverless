from typing import List, Tuple

from pydantic import AfterValidator, BaseModel, Field
from typing_extensions import Annotated


def validate_hour_day_tuple(dayhour_tuple: Tuple[int, int]) -> Tuple[int, int]:
    hour_index, day_index = dayhour_tuple
    assert 0 <= hour_index <= 13, "La hora debe estar entre 0 y 13"
    assert 0 <= day_index <= 6, "El día debe estar entre 0 y 6"

    return dayhour_tuple


HourDayTuple = Annotated[Tuple[int, int], AfterValidator(validate_hour_day_tuple)]


class ManualRegisterInput(BaseModel):
    username: str = Field(..., min_length=1, max_length=30, pattern=r"^[a-zA-Z]*$")
    list_of_indices: List[HourDayTuple] = Field(..., min_length=1, max_length=98)
