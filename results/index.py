import pydantic

from core.entities import GapItem, ResultsInput
from core.responses import get_body_response_from_pydantic_val_error
from core.utils import BasicResponse


def handler(event, context):

    print("Hello world")
    print(event)

    raw_body = event.get("body", None)

    if raw_body is None:
        return BasicResponse(status=400, body={"msg": "missing body"}).to_dict()

    try:
        data = ResultsInput.model_validate_json(raw_body)
        print(data)
        response_data = {
            "count": 1,
            "gaps": [
                GapItem(
                    day="Lunes",
                    hour="6:30 AM",
                    avg=1.0,
                    sd=0.1,
                    day_index=0,
                    hour_index=0,
                ).model_dump()
            ],
        }
        return BasicResponse(status=201, body=response_data).to_dict()
    except pydantic.ValidationError as e:
        error_body = get_body_response_from_pydantic_val_error(e)
        return BasicResponse(status=400, body=error_body).to_dict()
    except:
        return BasicResponse(
            status=500, body={"msg": "internal server error"}
        ).to_dict()
