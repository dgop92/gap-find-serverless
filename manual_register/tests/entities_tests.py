import json
import unittest

from pydantic import ValidationError

from core.entities import ManualRegisterInput
from core.validations import get_body_response_from_pydantic_val_error

assertions = unittest.TestCase()


def test_successful_parsing_when_valid_data():
    json_data = """
    {
        "username": "pepito",
        "list_of_indices": [[0, 0], [1, 1], [2, 2]]
    }
    """
    parsed_data = ManualRegisterInput.model_validate_json(json_data)
    assertions.assertEqual(parsed_data.username, "pepito")
    expected_list_of_indices = [(0, 0), (1, 1), (2, 2)]
    assertions.assertSetEqual(
        set(parsed_data.list_of_indices), set(expected_list_of_indices)
    )


def test_raise_error_when_day_index_is_invalid():
    json_data = """
    {
        "username": "pepito",
        "list_of_indices": [[0, 7]]
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ManualRegisterInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "list_of_indices")


def test_raise_error_when_hour_index_is_invalid():
    json_data = """
    {
        "username": "pepito",
        "list_of_indices": [[14, 0]]
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ManualRegisterInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "list_of_indices")


def test_raise_error_when_list_of_indices_is_empty():
    json_data = """
    {
        "username": "pepito",
        "list_of_indices": []
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ManualRegisterInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "list_of_indices")

    msg_error = get_body_response_from_pydantic_val_error(context.exception)
    assertions.assertEqual(
        msg_error, {"list_of_indices": ["El horario no puede estar vacío"]}
    )


def test_raise_error_when_list_of_indices_is_too_long():
    data = {"username": "pepito", "list_of_indices": [[0, 0]] * 99}
    json_data = json.dumps(data)
    with assertions.assertRaises(ValidationError) as context:
        ManualRegisterInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "list_of_indices")

    msg_error = get_body_response_from_pydantic_val_error(context.exception)
    assertions.assertEqual(
        msg_error,
        {
            "list_of_indices": [
                "Es imposible tener más de 98 horas de clases a la semana"
            ]
        },
    )


def test_raise_error_when_username_is_empty():
    json_data = """
    {
        "username": "",
        "list_of_indices": [[0, 0]]
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ManualRegisterInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "username")

    msg_error = get_body_response_from_pydantic_val_error(context.exception)
    assertions.assertEqual(
        msg_error, {"username": ["El nombre de usuario no puede estar vacío"]}
    )


def test_raise_error_when_username_is_too_long():
    data = {"username": "a" * 31, "list_of_indices": [[0, 0]]}
    json_data = json.dumps(data)
    with assertions.assertRaises(ValidationError) as context:
        ManualRegisterInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "username")

    msg_error = get_body_response_from_pydantic_val_error(context.exception)
    assertions.assertEqual(
        msg_error,
        {"username": ["El nombre de usuario no puede tener más de 30 caracteres"]},
    )


def test_raise_error_when_username_is_invalid():
    json_data = """
    {
        "username": "pepi#cito",
        "list_of_indices": [[0, 0]]
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ManualRegisterInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "username")

    msg_error = get_body_response_from_pydantic_val_error(context.exception)
    assertions.assertEqual(
        msg_error, {"username": ["El nombre de usuario solo puede contener letras"]}
    )
