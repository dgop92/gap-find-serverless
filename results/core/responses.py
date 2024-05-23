from pydantic import ValidationError


def get_body_response_from_pydantic_val_error(val_error: ValidationError):
    # For this endpoint, client does not read error messages
    return {"non_field_errors": f"error desconocido: {str(val_error)}"}
