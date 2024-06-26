from typing import Any

from pydantic import ValidationError

from core.entities import ResultsInput
from core.responses import BadRequestResponse, GenericJSONResponse


def get_body_response_from_pydantic_val_error(val_error: ValidationError):
    try:
        error = val_error.errors()[0]
        field_name = error["loc"][0]

        if field_name == "usernames":
            msg = "error desconocido"

            if error["type"] == "string_pattern_mismatch":
                msg = f"El usuario {error['input']} solo puede contener letras"

            return {"usernames": [msg]}

        return {"non_field_errors": ["error desconocido"]}
    except:
        return {"non_field_errors": [f"error desconocido: {str(val_error)}"]}


def validate_body(raw_body: Any | None) -> GenericJSONResponse | ResultsInput:

    if raw_body is None:
        return BadRequestResponse(body={"msg": "missing body"})

    if not isinstance(raw_body, str):
        return BadRequestResponse(body={"msg": "body must be a string"})

    try:
        data = ResultsInput.model_validate_json(raw_body)
        return data
    except ValidationError as e:
        error_body = get_body_response_from_pydantic_val_error(e)
        return BadRequestResponse(body=error_body)
    except Exception as e:
        return GenericJSONResponse(
            status=500, body={"msg": f"internal server error: {str(e)}"}
        )
