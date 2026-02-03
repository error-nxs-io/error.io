import json
from dataclasses import dataclass
from typing import Any, Dict, Optional
import urllib.request


@dataclass
class APIResponse:
    intent: str
    parameters: Dict[str, Any]
    reply: str


class APIClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    def interpret(self, text: str, context: Dict[str, Any]) -> Optional[APIResponse]:
        if not self._base_url:
            return None
        payload = json.dumps({"text": text, "context": context}).encode("utf-8")
        request = urllib.request.Request(
            f"{self._base_url}/interpret",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception:
            return None
        return APIResponse(
            intent=data.get("intent", "unknown"),
            parameters=data.get("parameters", {}),
            reply=data.get("reply", ""),
        )
