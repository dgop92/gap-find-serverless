import base64
import re
from typing import Any, Dict, List

from pydantic import ValidationError
from requests_toolbelt.multipart import decoder

from core.entities import AnalyzeMeetingInput
from core.responses import BadRequestResponse, GenericJSONResponse


def get_body_response_from_pydantic_val_error(val_error: ValidationError):
    try:
        error = val_error.errors()[0]
        field_name = error["loc"][0]

        if field_name == "usernames":
            msg = "error desconocido"

            if error["type"] == "string_too_short":
                msg = "El nombre de usuario no puede estar vacío"

            if error["type"] == "string_too_long":
                msg = "El nombre de usuario no puede tener más de 30 caracteres"

            if error["type"] == "string_pattern_mismatch":
                msg = f"El usuario {error['input']} solo puede contener letras"

            if error["type"] == "too_short":
                msg = "Al menos debes proporcionar dos usuarios"

            if error["type"] == "too_long":
                msg = "No puedes proporcionar más de 150 usuarios"

            return {"usernames": [msg]}

        if field_name == "username_to_filter":
            if error["type"] == "string_too_short":
                msg = "El nombre de usuario no puede estar vacío"

            if error["type"] == "string_too_long":
                msg = "El nombre de usuario no puede tener más de 30 caracteres"

            if error["type"] == "string_pattern_mismatch":
                msg = f"El usuario {error['input']} solo puede contener letras"

        return {"non_field_errors": ["error desconocido"]}
    except:
        return {"non_field_errors": [f"error desconocido: {str(val_error)}"]}


def parse_usernames_file(body: bytes) -> List[str]:
    # get size of the file
    size = len(body)

    # if size is greater than 10KB
    if size > 10240:
        raise ValueError("file size is greater than 10KB")
    try:
        # decode the file as string
        file_content = body.decode("utf-8")
        lines = file_content.splitlines()
        # clean lines
        lines = [line.strip() for line in lines]
        # delete empty lines and duplicates
        lines_without_of_spaces = [line for line in lines if line]
        usernames = set(lines_without_of_spaces)
        return list(usernames)
    except UnicodeDecodeError:
        raise ValueError("invalid file encoding for usernames file")


def parse_username_to_filter(body: bytes) -> str:
    try:
        username = body.decode("utf-8")
        return username
    except UnicodeDecodeError:
        raise ValueError("invalid encoding for username to filter field")


def parse_extra_usernames(body: bytes) -> List[str]:
    try:
        usernames_as_str = body.decode("utf-8")
        usernames = usernames_as_str.split(",")
        # clean usernames
        usernames = [username for username in usernames if username != ""]
        return usernames
    except UnicodeDecodeError:
        raise ValueError("invalid encoding for username to filter field")


def parse_base_on_field_name(body: bytes, field_name: str) -> Any:
    if field_name == "usernames_file":
        return parse_usernames_file(body)
    elif field_name == "username_to_filter":
        return parse_username_to_filter(body)
    elif field_name == "extra_usernames":
        return parse_extra_usernames(body)

    return None


def parse_base64_multi_part_body(
    body: str,
    content_type: str,
) -> Dict[str, Any]:

    final_data = {}

    parsed_body = base64.b64decode(body)
    multipart_data = decoder.MultipartDecoder(parsed_body, content_type)
    for part in multipart_data.parts:
        content_disposition = part.headers[b"Content-Disposition"].decode("utf-8")  # type: ignore
        match = re.search(r'name="(\w+)"', content_disposition)
        if match:
            name = match.group(1)
            content = part.content
            # if field is already known, ignore it
            if name in final_data:
                continue

            d = parse_base_on_field_name(content, name)

            # if field is not known, ignore it
            if d is None:
                continue

            final_data[name] = d
        else:
            raise ValueError("invalid content disposition, missing name")

    # merge usernames and extra_usernames
    final_usernames = []

    if "usernames_file" in final_data:
        final_usernames.extend(final_data["usernames_file"])
        del final_data["usernames_file"]

    if "extra_usernames" in final_data:
        final_usernames.extend(final_data["extra_usernames"])
        del final_data["extra_usernames"]

    final_data["usernames"] = final_usernames

    return final_data


def validate_body(
    raw_body: Any | None, content_type: str
) -> GenericJSONResponse | AnalyzeMeetingInput:

    if raw_body is None:
        return BadRequestResponse(body={"msg": "missing body"})

    if not isinstance(raw_body, str):
        return BadRequestResponse(body={"msg": "body must be a string"})

    try:
        raw_data = parse_base64_multi_part_body(raw_body, content_type)
        data = AnalyzeMeetingInput.model_validate(raw_data)
        return data
    except ValidationError as e:
        error_body = get_body_response_from_pydantic_val_error(e)
        return BadRequestResponse(body=error_body)
    except ValueError as e:
        return BadRequestResponse(body={"msg": str(e)})
    except Exception as e:
        return GenericJSONResponse(
            status=500, body={"msg": f"internal server error: {str(e)}"}
        )
