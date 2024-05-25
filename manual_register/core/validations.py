from typing import Any

from pydantic import ValidationError

from core.entities import ManualRegisterInput
from core.responses import BadRequestResponse, GenericJSONResponse


def get_body_response_from_pydantic_val_error(val_error: ValidationError):
    try:
        error = val_error.errors()[0]
        field_name = error["loc"][0]

        if field_name == "list_of_indices":
            msg = "error desconocido"
            if error["type"] == "too_short":
                msg = "El horario no puede estar vacío"

            if error["type"] == "too_long":
                msg = "Es imposible tener más de 98 horas de clases a la semana"

            return {"non_field_errors": msg}

        if field_name == "username":
            msg = "error desconocido"
            if error["type"] == "string_too_short":
                msg = "El nombre de usuario no puede estar vacío"

            if error["type"] == "string_too_long":
                msg = "El nombre de usuario no puede tener más de 30 caracteres"

            if error["type"] == "string_pattern_mismatch":
                msg = "El nombre de usuario solo puede contener letras"

            return {"username": msg}

        return {"non_field_errors": "error desconocido"}
    except:
        return {"non_field_errors": f"error desconocido: {str(val_error)}"}


def validate_body(raw_body: Any | None) -> GenericJSONResponse | ManualRegisterInput:

    if raw_body is None:
        return BadRequestResponse(body={"msg": "missing body"})

    if not isinstance(raw_body, str):
        return BadRequestResponse(body={"msg": "body must be a string"})

    try:
        data = ManualRegisterInput.model_validate_json(raw_body)
        return data
    except ValidationError as e:
        error_body = get_body_response_from_pydantic_val_error(e)
        return BadRequestResponse(body=error_body)
    except Exception as e:
        return GenericJSONResponse(
            status=500, body={"msg": f"internal server error: {str(e)}"}
        )
