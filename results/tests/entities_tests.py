import unittest

from pydantic import ValidationError

from core.entities import ResultsInput

assertions = unittest.TestCase()


def test_successful_parsing_when_valid_data():
    json_data = """
    {
        "usernames": ["pepito", "juan"]
    }
    """
    parsed_data = ResultsInput.model_validate_json(json_data)
    assertions.assertSetEqual(set(parsed_data.usernames), {"pepito", "juan"})
    assertions.assertEqual(parsed_data.compute_sd, False)
    assertions.assertEqual(parsed_data.no_classes_day, False)
    assertions.assertEqual(parsed_data.ignore_weekend, True)
    assertions.assertIsNone(parsed_data.limit)
    assertions.assertIsNone(parsed_data.days_to_filter)


def test_successful_parsing_when_limit_is_provided():
    json_data = """
    {
        "usernames": ["pepito", "juan"],
        "limit": 10
    }
    """
    parsed_data = ResultsInput.model_validate_json(json_data)
    assertions.assertEqual(parsed_data.limit, 10)


def test_successful_parsing_when_days_to_filter_is_provided():
    json_data = """
    {
        "usernames": ["pepito", "juan"],
        "days_to_filter": [0, 1, 2]
    }
    """
    parsed_data = ResultsInput.model_validate_json(json_data)
    days_to_filter = parsed_data.days_to_filter or []
    assertions.assertSetEqual(set(days_to_filter), {0, 1, 2})


def test_raise_error_when_usernames_is_less_than_2():
    json_data = """
    {
        "usernames": ["pepito"]
    } 
    """
    with assertions.assertRaises(ValidationError) as context:
        ResultsInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    print(error)
    assertions.assertEqual(error["loc"][0], "usernames")


def test_raise_error_when_limit_is_less_than_2():
    json_data = """
    {
        "usernames": ["pepito", "juan"],
        "limit": 1
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ResultsInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "limit")


def test_raise_error_when_days_to_filter_is_empty():
    json_data = """
    {
        "usernames": ["pepito", "juan"],
        "days_to_filter": []
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ResultsInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "days_to_filter")


def test_raise_error_when_days_to_filter_has_invalid_values():
    json_data = """
    {
        "usernames": ["pepito", "juan"],
        "days_to_filter": [0, 1, 2, 7]
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ResultsInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "days_to_filter")


def test_raise_error_when_days_to_filter_is_greater_than_7():
    json_data = """
    {
        "usernames": ["pepito", "juan"],
        "days_to_filter": [0, 1, 2, 3, 4, 5, 6, 7]
    }
    """
    with assertions.assertRaises(ValidationError) as context:
        ResultsInput.model_validate_json(json_data)

    error = context.exception.errors()[0]
    assertions.assertEqual(error["loc"][0], "days_to_filter")
