import json
from typing import Any, Dict


class BasicResponse:
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
