from core.factory import core_factory
from core.responses import GenericJSONResponse
from core.schedule_logic import find_ss_from_class_hours
from core.validations import validate_body

core_components = core_factory()


def handler(event, context):
    raw_body = event.get("body", None)

    val_result = validate_body(raw_body)

    if isinstance(val_result, GenericJSONResponse):
        return val_result.to_dict()

    schedule = find_ss_from_class_hours(val_result.list_of_indices)
    username = val_result.username

    try:
        repository = core_components.repository
        repository.save_user(username, schedule)
        return GenericJSONResponse(
            201, body={"username": username, "schedule": schedule}
        ).to_dict()
    except Exception as e:
        return GenericJSONResponse(
            500, body={"msg": f"un error ocurrió: {str(e)}"}
        ).to_dict()
