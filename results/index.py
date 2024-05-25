from core.entities import GapItem
from core.factory import core_factory
from core.responses import GenericJSONResponse
from core.validations import validate_body

core_components = core_factory()


def handler(event, context):

    raw_body = event.get("body", None)

    val_result = validate_body(raw_body)

    if isinstance(val_result, GenericJSONResponse):
        return val_result.to_dict()

    try:
        print(val_result)
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
        return GenericJSONResponse(201, body=response_data).to_dict()
    except Exception as e:
        return GenericJSONResponse(
            500, body={"msg": f"un error ocurrió: {str(e)}"}
        ).to_dict()
