from pydantic import ValidationError


def get_body_response_from_pydantic_val_error(val_error: ValidationError):
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

        return {"username": msg}

    return {"non_field_errors": "error desconocido"}
