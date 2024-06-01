import unittest

from pydantic import ValidationError

from core.entities import AnalyzeMeetingInput
from core.validations import get_body_response_from_pydantic_val_error

assertions = unittest.TestCase()


def test_successful_parsing_when_valid_data():
    data = {"usernames": ["pepito", "juan"]}

    parsed_data = AnalyzeMeetingInput.model_validate(data)
    assertions.assertSetEqual(set(parsed_data.usernames), {"pepito", "juan"})
    assertions.assertEqual(parsed_data.username_to_filter, None)


def test_successful_parsing_when_valid_data_and_username_to_filter():
    data = {"usernames": ["pepito", "juan", "perez"], "username_to_filter": "pepito"}

    parsed_data = AnalyzeMeetingInput.model_validate(data)
    assertions.assertSetEqual(set(parsed_data.usernames), {"pepito", "juan", "perez"})
    assertions.assertEqual(parsed_data.username_to_filter, "pepito")


def test_raise_error_when_usernames_is_less_than_2():
    data = {"usernames": ["pepito"]}
    with assertions.assertRaises(ValidationError) as context:
        AnalyzeMeetingInput.model_validate(data)

    error = context.exception.errors()[0]
    msg_error = get_body_response_from_pydantic_val_error(context.exception)
    assertions.assertEqual(error["loc"][0], "usernames")
    assertions.assertEqual(
        msg_error["usernames"][0], "Al menos debes proporcionar dos usuarios"
    )


def test_raise_error_when_usernames_is_more_than_150():
    data = {"usernames": ["pepito"] * 151}
    with assertions.assertRaises(ValidationError) as context:
        AnalyzeMeetingInput.model_validate(data)

    error = context.exception.errors()[0]
    msg_error = get_body_response_from_pydantic_val_error(context.exception)
    assertions.assertEqual(error["loc"][0], "usernames")
    assertions.assertEqual(
        msg_error["usernames"][0], "No puedes proporcionar más de 150 usuarios"
    )


def test_raise_error_when_username_is_invalid():
    data = {"usernames": ["asdasd", "pe#pito"]}
    with assertions.assertRaises(ValidationError) as context:
        AnalyzeMeetingInput.model_validate(data)

    error = context.exception.errors()[0]
    msg_error = get_body_response_from_pydantic_val_error(context.exception)
    assertions.assertEqual(error["loc"][0], "usernames")
    assertions.assertEqual(
        msg_error["usernames"][0], "El usuario pe#pito solo puede contener letras"
    )
