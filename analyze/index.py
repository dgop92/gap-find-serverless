from core.factory import core_factory
from core.meeting_analysis import get_meeting_analysis
from core.responses import BadRequestResponseException, GenericJSONResponse
from core.validations import validate_body

core_components = core_factory()


def handler(event, context):

    content_type = event["headers"]["content-type"]
    raw_body = event.get("body", None)

    val_result = validate_body(raw_body, content_type)

    if isinstance(val_result, GenericJSONResponse):
        return val_result.to_dict()

    try:
        total_students, results = get_meeting_analysis(
            val_result, core_components.repository
        )
        response_data = [result.model_dump() for result in results]
        return GenericJSONResponse(
            200,
            body={"total_students": total_students, "results": response_data},
        ).to_dict()
    except BadRequestResponseException as e:
        return e.bad_request_response.to_dict()
    except Exception as e:
        return GenericJSONResponse(
            500, body={"msg": f"un error ocurrió: {str(e)}"}
        ).to_dict()
