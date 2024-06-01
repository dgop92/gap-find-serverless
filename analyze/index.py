from core.entities import AnalyzeMeetingResult
from core.factory import core_factory
from core.responses import BadRequestResponseException, GenericJSONResponse
from core.validations import validate_body

core_components = core_factory()


def handler(event, context):

    content_type = event["headers"]["Content-Type"]
    raw_body = event.get("body", None)

    val_result = validate_body(raw_body, content_type)

    if isinstance(val_result, GenericJSONResponse):
        return val_result.to_dict()

    try:
        results = [
            AnalyzeMeetingResult(
                day_index=0, hour_index=0, number_of_students=0, availability=0.0
            )
        ]
        response_data = [result.model_dump() for result in results]
        return GenericJSONResponse(
            201,
            body={"total_students": len(response_data), "results": response_data},
        ).to_dict()
    except BadRequestResponseException as e:
        return e.bad_request_response.to_dict()
    except Exception as e:
        return GenericJSONResponse(
            500, body={"msg": f"un error ocurrió: {str(e)}"}
        ).to_dict()
