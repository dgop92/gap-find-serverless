import json
import unittest

from index import handler
from tests.test_utils import create_event_context_from_body

assertions = unittest.TestCase()


def test_sucessful_lambda_execution():

    raw_request_body = {
        "usernames": ["pepito", "juanito"],
    }
    raw_request_json = json.dumps(raw_request_body)
    body, context = create_event_context_from_body(raw_request_json)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 201)


def test_bad_response_when_body_is_not_provided():
    response = handler({}, {})

    assertions.assertEqual(response["statusCode"], 400)


def test_bad_response_when_data_is_not_valid():

    raw_request_body = {"usernames": []}
    raw_request_json = json.dumps(raw_request_body)
    body, context = create_event_context_from_body(raw_request_json)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 400)
