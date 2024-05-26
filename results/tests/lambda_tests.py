import json
import unittest

from core.db import UsernameMockDB
from index import handler
from tests.test_utils import create_event_context_from_body

assertions = unittest.TestCase()

string_schedule1 = "01000000100100001010001000000000000000000000000000000000011010001101001010000111000000000000000000"
string_schedule2 = "01000000111100011100001010000001000000000000100000010000010100011010001100000000100000000000000000"

KNOWN_GAPS = set(
    [
        (0, 0),
        (0, 2),
        (0, 4),
        (1, 0),
        (2, 0),
        (3, 0),
        (3, 2),
        (3, 4),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 4),
        (5, 0),
        (5, 1),
        (5, 2),
        (5, 4),
        (6, 0),
        (6, 1),
        (6, 4),
        (7, 0),
        (7, 1),
        (7, 4),
        (8, 0),
        (10, 4),
        (11, 4),
        (12, 0),
        (12, 1),
        (12, 2),
        (12, 4),
        (13, 0),
        (13, 1),
        (13, 2),
        (13, 4),
    ]
)


def get_success_response_body(options):
    raw_request_body = {
        "usernames": ["pepito", "juanito"],
        **options,
    }
    UsernameMockDB.data = {
        "pepito": string_schedule1,
        "juanito": string_schedule2,
    }

    raw_request_json = json.dumps(raw_request_body)
    body, context = create_event_context_from_body(raw_request_json)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 201)
    assertions.assertEqual(response["headers"]["Content-Type"], "application/json")

    return json.loads(response["body"])


def test_sucessful_lambda_execution():

    raw_request_body = {
        "usernames": ["pepito", "juanito"],
    }
    UsernameMockDB.data = {
        "pepito": string_schedule1,
        "juanito": string_schedule2,
    }

    raw_request_json = json.dumps(raw_request_body)
    body, context = create_event_context_from_body(raw_request_json)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 201)

    content_type = response["headers"]["Content-Type"]
    assertions.assertEqual(content_type, "application/json")

    response_body = json.loads(response["body"])
    assertions.assertEqual(response_body["count"], len(KNOWN_GAPS))
    assertions.assertSetEqual(
        set((d["hour_index"], d["day_index"]) for d in response_body["gaps"]),
        KNOWN_GAPS,
    )


def test_sucessful_lambda_execution_when_applying_limit():

    response_body = get_success_response_body({"limit": 5})

    gaps = response_body["gaps"]
    found_gaps_indices = set(map(lambda e: (e["hour_index"], e["day_index"]), gaps))

    assertions.assertEqual(len(found_gaps_indices), 5)


def test_sucessful_lambda_execution_when_applying_day_filter():

    response_body = get_success_response_body({"days_to_filter": [0, 1]})

    gaps = response_body["gaps"]
    found_gaps_indices = set(map(lambda e: (e["hour_index"], e["day_index"]), gaps))
    for gap_index_tuple in found_gaps_indices:
        assertions.assertTrue(gap_index_tuple[1] not in [0, 1])


def test_sucessful_lambda_execution_when_sd_is_set():

    response_body = get_success_response_body({"compute_sd": True})

    gaps = response_body["gaps"]

    assertions.assertTrue("sd" in gaps[0])


def test_sucessful_lambda_execution_when_no_classes_day_is_true():

    response_body = get_success_response_body(
        {
            "no_classes_day": True,
        }
    )

    gaps = response_body["gaps"]

    found_gaps_indices = map(lambda e: e["day_index"], gaps)
    gaps_on_thursday = any(map(lambda e: e == 3, found_gaps_indices))
    assertions.assertTrue(gaps_on_thursday)


def test_sucessful_lambda_execution_when_no_classes_day_is_false():

    response_body = get_success_response_body(
        {
            "no_classes_day": False,
        }
    )

    gaps = response_body["gaps"]

    found_gaps_indices = map(lambda e: e["day_index"], gaps)
    gaps_on_thursday = any(map(lambda e: e == 3, found_gaps_indices))
    assertions.assertFalse(gaps_on_thursday)


def test_sucessful_lambda_execution_when_weekend_is_false():

    response_body = get_success_response_body(
        {
            "ignore_weekend": False,
            "no_classes_day": True,
        }
    )

    gaps = response_body["gaps"]
    found_gaps_indices = map(lambda e: e["day_index"], gaps)
    gaps_on_weekend = any(map(lambda e: e == 5 or e == 6, found_gaps_indices))
    assertions.assertTrue(gaps_on_weekend)


def test_bad_response_when_body_is_not_provided():
    response = handler({}, {})

    assertions.assertEqual(response["statusCode"], 400)


def test_bad_response_when_data_is_not_valid():

    raw_request_body = {"usernames": []}
    raw_request_json = json.dumps(raw_request_body)
    body, context = create_event_context_from_body(raw_request_json)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 400)
