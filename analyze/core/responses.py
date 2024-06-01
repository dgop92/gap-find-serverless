import json
from typing import Any, Dict


class GenericJSONResponse:
    def __init__(self, status: int, body: Dict[str, Any]):
        self.status = status
        self.body = body

    def to_dict(self):
        return {
            "statusCode": self.status,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(self.body, ensure_ascii=False),
        }


class BadRequestResponse(GenericJSONResponse):
    def __init__(self, body: Dict[str, Any]):
        super().__init__(status=400, body=body)


class BadRequestResponseException(Exception):

    def __init__(self, bad_request_response: BadRequestResponse, *args: object) -> None:
        self.bad_request_response = bad_request_response
        super().__init__(*args)
