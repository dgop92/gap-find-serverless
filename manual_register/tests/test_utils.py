from typing import Any, Dict, Tuple


def create_event_context_from_body(body: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    return {"body": body}, {}
