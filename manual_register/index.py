import pydantic

from core.db import UsernameRedisDB
from core.entities import ManualRegisterInput
from core.responses import get_body_response_from_pydantic_val_error
from core.utils import BasicResponse


def handler(event, context):

    from core.config import APP_CONFIG

    redis_db = UsernameRedisDB(APP_CONFIG.redis_url)

    raw_body = event.get("body", None)

    if raw_body is None:
        return BasicResponse(status=400, body={"msg": "missing body"}).to_dict()

    try:
        data = ManualRegisterInput.model_validate_json(raw_body)
        print(data)
        response_data = {
            "username": "pepito",
            "schedule": "10001111",
        }
        redis_db.save_user(
            username=response_data["username"], schedule=response_data["schedule"]
        )
        return BasicResponse(status=201, body=response_data).to_dict()
    except pydantic.ValidationError as e:
        error_body = get_body_response_from_pydantic_val_error(e)
        return BasicResponse(status=400, body=error_body).to_dict()
    except:
        return BasicResponse(
            status=500, body={"msg": "internal server error"}
        ).to_dict()
