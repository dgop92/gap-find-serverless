from typing import Any, Dict, Tuple


def create_event_context_from_body(body: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    return {"body": body}, {}


def create_event_context_from_base_64_body(
    body: str,
    content_type: str,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    event = {"headers": {"Content-Type": content_type}, "body": body}
    return event, {}