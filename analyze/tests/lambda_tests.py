import unittest

from core.db import UsernameMockDB
from index import handler
from tests.test_utils import create_event_context_from_base_64_body, get_random_schedule

assertions = unittest.TestCase()

CONTENT_TYPE = "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"


def test_successful_response_when_data_is_valid():

    UsernameMockDB.data = {
        "dpucas": get_random_schedule(),
        "kaloes": get_random_schedule(),
    }

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InVzZXJuYW1lc19maWxlIjsgZmlsZW5hbWU9InVzZXJuYW1lc19maWxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpkcHVjYXMNCmthbG9lcw0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXLS0NCg=="
    body, context = create_event_context_from_base_64_body(base64_body, CONTENT_TYPE)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 200)


def test_bad_response_when_data_is_invalid():

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InVzZXJuYW1lc19maWxlIjsgZmlsZW5hbWU9InVzZXJuYW1lc19maWxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQoNCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeTdNQTRZV3hrVHJadTBnVy0tDQo="
    body, context = create_event_context_from_base_64_body(base64_body, CONTENT_TYPE)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 400)


def test_bad_response_when_not_enough_usernames():

    UsernameMockDB.data = {
        "dpucas": get_random_schedule(),
    }

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImV4dHJhX3VzZXJuYW1lcyINCg0KcGVwaXRvLGp1YW4NCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeTdNQTRZV3hrVHJadTBnVw0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJ1c2VybmFtZXNfZmlsZSI7IGZpbGVuYW1lPSJib3hwbG90LnBuZyINCkNvbnRlbnQtVHlwZTogaW1hZ2UvcG5nDQoNCmRwdWNhcw0Ka2Fsb2VzDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnk3TUE0WVd4a1RyWnUwZ1ctLQ0K"
    body, context = create_event_context_from_base_64_body(base64_body, CONTENT_TYPE)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 400)


def test_bad_response_when_username_to_filter_does_not_exist():

    UsernameMockDB.data = {
        "dpucas": get_random_schedule(),
    }

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImV4dHJhX3VzZXJuYW1lcyINCg0KcGVwaXRvLGp1YW4NCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeTdNQTRZV3hrVHJadTBnVw0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJ1c2VybmFtZV90b19maWx0ZXIiDQoNCnBlcGl0bw0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXLS0="
    body, context = create_event_context_from_base_64_body(base64_body, CONTENT_TYPE)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 400)
