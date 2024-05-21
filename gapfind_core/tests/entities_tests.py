import json
import unittest

from pydantic import ValidationError

from core.entities import ManualRegisterInput
from core.responses import get_body_response_from_pydantic_val_error


class ManualRegisterInputTests(unittest.TestCase):
    def test_successful_parsing_when_valid_data(self):
        json_data = """
        {
            "username": "pepito",
            "list_of_indices": [[0, 0], [1, 1], [2, 2]]
        }
        """
        parsed_data = ManualRegisterInput.model_validate_json(json_data)
        self.assertEqual(parsed_data.username, "pepito")
        expected_list_of_indices = [(0, 0), (1, 1), (2, 2)]
        self.assertSetEqual(
            set(parsed_data.list_of_indices), set(expected_list_of_indices)
        )

    def test_raise_error_when_day_index_is_invalid(self):
        json_data = """
        {
            "username": "pepito",
            "list_of_indices": [[0, 7]]
        }
        """
        with self.assertRaises(ValidationError) as context:
            ManualRegisterInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "list_of_indices")

    def test_raise_error_when_hour_index_is_invalid(self):
        json_data = """
        {
            "username": "pepito",
            "list_of_indices": [[14, 0]]
        }
        """
        with self.assertRaises(ValidationError) as context:
            ManualRegisterInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "list_of_indices")

    def test_raise_error_when_list_of_indices_is_empty(self):
        json_data = """
        {
            "username": "pepito",
            "list_of_indices": []
        }
        """
        with self.assertRaises(ValidationError) as context:
            ManualRegisterInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "list_of_indices")

        msg_error = get_body_response_from_pydantic_val_error(context.exception)
        self.assertEqual(
            msg_error, {"non_field_errors": "El horario no puede estar vacío"}
        )

    def test_raise_error_when_list_of_indices_is_too_long(self):
        data = {"username": "pepito", "list_of_indices": [[0, 0]] * 99}
        json_data = json.dumps(data)
        with self.assertRaises(ValidationError) as context:
            ManualRegisterInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "list_of_indices")

        msg_error = get_body_response_from_pydantic_val_error(context.exception)
        self.assertEqual(
            msg_error,
            {
                "non_field_errors": "Es imposible tener más de 98 horas de clases a la semana"
            },
        )

    def test_raise_error_when_username_is_empty(self):
        json_data = """
        {
            "username": "",
            "list_of_indices": [[0, 0]]
        }
        """
        with self.assertRaises(ValidationError) as context:
            ManualRegisterInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "username")

        msg_error = get_body_response_from_pydantic_val_error(context.exception)
        self.assertEqual(
            msg_error, {"username": "El nombre de usuario no puede estar vacío"}
        )

    def test_raise_error_when_username_is_too_long(self):
        data = {"username": "a" * 31, "list_of_indices": [[0, 0]]}
        json_data = json.dumps(data)
        with self.assertRaises(ValidationError) as context:
            ManualRegisterInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "username")

        msg_error = get_body_response_from_pydantic_val_error(context.exception)
        self.assertEqual(
            msg_error,
            {"username": "El nombre de usuario no puede tener más de 30 caracteres"},
        )
