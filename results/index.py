from core.factory import core_factory
from core.gaps import get_gaps
from core.responses import BadRequestResponseException, GenericJSONResponse
from core.validations import validate_body

core_components = core_factory()


def handler(event, context):

    raw_body = event.get("body", None)

    val_result = validate_body(raw_body)

    if isinstance(val_result, GenericJSONResponse):
        return val_result.to_dict()

    try:
        gaps = get_gaps(val_result, core_components.repository)
        response_data = {"count": len(gaps), "gaps": [gap.model_dump() for gap in gaps]}
        return GenericJSONResponse(201, body=response_data).to_dict()
    except BadRequestResponseException as e:
        return e.bad_request_response.to_dict()
    except Exception as e:
        return GenericJSONResponse(
            500, body={"msg": f"un error ocurrió: {str(e)}"}
        ).to_dict()
