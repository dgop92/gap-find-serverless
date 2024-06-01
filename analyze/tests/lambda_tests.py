import json
import unittest

from index import handler
from tests.test_utils import create_event_context_from_base_64_body

assertions = unittest.TestCase()

CONTENT_TYPE = "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"


def test_bad_response_when_data_is_invalid():

    base64_body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5N01BNFlXeGtUclp1MGdXDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InVzZXJuYW1lc19maWxlIjsgZmlsZW5hbWU9InVzZXJuYW1lc19maWxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQoNCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeTdNQTRZV3hrVHJadTBnVy0tDQo="
    body, context = create_event_context_from_base_64_body(base64_body, CONTENT_TYPE)

    response = handler(body, context)

    assertions.assertEqual(response["statusCode"], 400)
