import unittest

from pydantic import ValidationError

from core.entities import ResultsInput


class ResultsInputInputTests(unittest.TestCase):
    def test_successful_parsing_when_valid_data(self):
        json_data = """
        {
            "usernames": ["pepito", "juan"]
        }
        """
        parsed_data = ResultsInput.model_validate_json(json_data)
        self.assertSetEqual(set(parsed_data.usernames), {"pepito", "juan"})
        self.assertEqual(parsed_data.compute_sd, False)
        self.assertEqual(parsed_data.no_classes_day, False)
        self.assertEqual(parsed_data.ignore_weekend, True)
        self.assertIsNone(parsed_data.limit)
        self.assertIsNone(parsed_data.days_to_filter)

    def test_successful_parsing_when_limit_is_provided(self):
        json_data = """
        {
            "usernames": ["pepito", "juan"],
            "limit": 10
        }
        """
        parsed_data = ResultsInput.model_validate_json(json_data)
        self.assertEqual(parsed_data.limit, 10)

    def test_successful_parsing_when_days_to_filter_is_provided(self):
        json_data = """
        {
            "usernames": ["pepito", "juan"],
            "days_to_filter": [0, 1, 2]
        }
        """
        parsed_data = ResultsInput.model_validate_json(json_data)
        days_to_filter = parsed_data.days_to_filter or []
        self.assertSetEqual(set(days_to_filter), {0, 1, 2})

    def test_raise_error_when_usernames_is_less_than_2(self):
        json_data = """
        {
            "usernames": ["pepito"]
        } 
        """
        with self.assertRaises(ValidationError) as context:
            ResultsInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        print(error)
        self.assertEqual(error["loc"][0], "usernames")

    def test_raise_error_when_limit_is_less_than_2(self):
        json_data = """
        {
            "usernames": ["pepito", "juan"],
            "limit": 1
        }
        """
        with self.assertRaises(ValidationError) as context:
            ResultsInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "limit")

    def test_raise_error_when_days_to_filter_is_empty(self):
        json_data = """
        {
            "usernames": ["pepito", "juan"],
            "days_to_filter": []
        }
        """
        with self.assertRaises(ValidationError) as context:
            ResultsInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "days_to_filter")

    def test_raise_error_when_days_to_filter_has_invalid_values(self):
        json_data = """
        {
            "usernames": ["pepito", "juan"],
            "days_to_filter": [0, 1, 2, 7]
        }
        """
        with self.assertRaises(ValidationError) as context:
            ResultsInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "days_to_filter")

    def test_raise_error_when_days_to_filter_is_greater_than_7(self):
        json_data = """
        {
            "usernames": ["pepito", "juan"],
            "days_to_filter": [0, 1, 2, 3, 4, 5, 6, 7]
        }
        """
        with self.assertRaises(ValidationError) as context:
            ResultsInput.model_validate_json(json_data)

        error = context.exception.errors()[0]
        self.assertEqual(error["loc"][0], "days_to_filter")
