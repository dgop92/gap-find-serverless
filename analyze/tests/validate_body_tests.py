import json
import unittest

from core.entities import AnalyzeMeetingInput
from core.responses import GenericJSONResponse
from core.validations import validate_body
from tests.base64_body_utils import INVALID_IMG_BODY64

assertions = unittest.TestCase()

CONTENT_TYPE = "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"


def test_bad_response_when_usernames_is_less_than_2_using_only_usernames_file():

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InVzZXJuYW1lc19maWxlIjsgZmlsZW5hbWU9InVzZXJuYW1lc19maWxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQoNCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeTdNQTRZV3hrVHJadTBnVy0tDQo="
    val_result = validate_body(base64_body, CONTENT_TYPE)

    if isinstance(val_result, GenericJSONResponse):
        assertions.assertEqual(val_result.status, 400)
        assertions.assertEqual(
            val_result.body["usernames"][0], "Al menos debes proporcionar dos usuarios"
        )
    else:
        assertions.fail("Expected GenericJSONResponse")


def test_bad_response_when_usernames_file_is_not_text():

    base64_body = INVALID_IMG_BODY64
    val_result = validate_body(base64_body, CONTENT_TYPE)

    if isinstance(val_result, GenericJSONResponse):
        assertions.assertEqual(val_result.status, 400)
        assertions.assertTrue("msg" in val_result.body)
    else:
        assertions.fail("Expected GenericJSONResponse")


def test_sucess_response_when_usernames_file_is_valid():

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InVzZXJuYW1lc19maWxlIjsgZmlsZW5hbWU9InVzZXJuYW1lc19maWxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpkcHVjYXMNCmthbG9lcw0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXLS0NCg=="
    val_result = validate_body(base64_body, CONTENT_TYPE)

    if isinstance(val_result, AnalyzeMeetingInput):
        assertions.assertEqual(set(val_result.usernames), set(["dpucas", "kaloes"]))
        assertions.assertEqual(val_result.username_to_filter, None)
    else:
        assertions.fail("Expected AnalyzeMeetingInput")


def test_bad_response_when_usernames_is_less_than_2_using_only_extra_usernames():

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImV4dHJhX3VzZXJuYW1lcyINCg0KcGVwaXRvDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnk3TUE0WVd4a1RyWnUwZ1ctLQ=="
    val_result = validate_body(base64_body, CONTENT_TYPE)

    if isinstance(val_result, GenericJSONResponse):
        assertions.assertEqual(val_result.status, 400)
        assertions.assertEqual(
            val_result.body["usernames"][0], "Al menos debes proporcionar dos usuarios"
        )
    else:
        assertions.fail("Expected GenericJSONResponse")


def test_sucess_response_when_extra_usernames_is_valid():

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImV4dHJhX3VzZXJuYW1lcyINCg0KcGVwaXRvLGp1YW4NCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeTdNQTRZV3hrVHJadTBnVy0t"
    val_result = validate_body(base64_body, CONTENT_TYPE)

    if isinstance(val_result, AnalyzeMeetingInput):
        assertions.assertEqual(set(val_result.usernames), set(["pepito", "juan"]))
        assertions.assertEqual(val_result.username_to_filter, None)
    else:
        assertions.fail("Expected AnalyzeMeetingInput")


def test_sucess_response_when_extra_usernames_and_usernames_file_are_valid():

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImV4dHJhX3VzZXJuYW1lcyINCg0KcGVwaXRvLGp1YW4NCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeTdNQTRZV3hrVHJadTBnVw0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJ1c2VybmFtZXNfZmlsZSI7IGZpbGVuYW1lPSJib3hwbG90LnBuZyINCkNvbnRlbnQtVHlwZTogaW1hZ2UvcG5nDQoNCmRwdWNhcw0Ka2Fsb2VzDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnk3TUE0WVd4a1RyWnUwZ1ctLQ0K"
    val_result = validate_body(base64_body, CONTENT_TYPE)

    if isinstance(val_result, AnalyzeMeetingInput):
        assertions.assertEqual(
            set(val_result.usernames), set(["pepito", "juan", "dpucas", "kaloes"])
        )
        assertions.assertEqual(val_result.username_to_filter, None)
    else:
        assertions.fail("Expected AnalyzeMeetingInput")


def test_sucess_response_when_extra_username_to_filter_is_valid():

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImV4dHJhX3VzZXJuYW1lcyINCg0KcGVwaXRvLGp1YW4NCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeTdNQTRZV3hrVHJadTBnVw0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJ1c2VybmFtZV90b19maWx0ZXIiDQoNCnBlcGl0bw0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXLS0="
    val_result = validate_body(base64_body, CONTENT_TYPE)

    if isinstance(val_result, AnalyzeMeetingInput):
        assertions.assertEqual(val_result.username_to_filter, "pepito")
    else:
        assertions.fail("Expected AnalyzeMeetingInput")
