import json
import unittest

from index import handler
from tests.test_utils import create_event_context_from_body

assertions = unittest.TestCase()


def test_sucessful_lambda_execution():

    expected_ss = "01000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    list_of_indicies = [
        (0, 1),
    ]
    raw_request_body = {"username": "pepito", "list_of_indices": list_of_indicies}
    raw_request_json = json.dumps(raw_request_body)
    body, context = create_event_context_from_body(raw_request_json)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 201)

    content_type = response["headers"]["Content-Type"]
    assertions.assertEqual(content_type, "application/json")

    response_body = json.loads(response["body"])
    assertions.assertEqual(response_body["username"], "pepito")
    assertions.assertEqual(response_body["schedule"], expected_ss)


def test_bad_response_when_body_is_not_provided():
    response = handler({}, {})

    assertions.assertEqual(response["statusCode"], 400)


def test_bad_response_when_data_is_not_valid():

    raw_request_body = {"username": "pep#ito", "list_of_indices": [[0, 1]]}
    raw_request_json = json.dumps(raw_request_body)
    body, context = create_event_context_from_body(raw_request_json)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 400)

    response_body = json.loads(response["body"])
    assertions.assertIn("username", response_body)
