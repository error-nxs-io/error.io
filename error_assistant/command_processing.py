from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from .api_client import APIClient, APIResponse


@dataclass
class Command:
    intent: str
    parameters: Dict[str, Any]
    response: str


class CommandProcessor:
    def __init__(self, api_client: APIClient) -> None:
        self._api_client = api_client

    def interpret(self, text: str, context: Dict[str, Any]) -> Command:
        api_result = self._api_client.interpret(text, context)
        if api_result:
            return Command(
                intent=api_result.intent,
                parameters=api_result.parameters,
                response=api_result.reply,
            )
        intent, params = self._fallback_intent(text)
        return Command(intent=intent, parameters=params, response="")

    def _fallback_intent(self, text: str) -> Tuple[str, Dict[str, Any]]:
        normalized = text.lower()
        if normalized.startswith("open "):
            return "open_app", {"name": text[5:].strip()}
        if normalized.startswith("close "):
            return "close_app", {"name": text[6:].strip()}
        if normalized.startswith("browse "):
            return "browse", {"url": text[7:].strip()}
        if normalized.startswith("create file "):
            return "create_file", {"path": text[12:].strip()}
        if normalized.startswith("delete file "):
            return "delete_file", {"path": text[12:].strip()}
        if normalized.startswith("move file "):
            return "move_file", self._parse_two_paths(text[10:])
        if normalized.startswith("copy file "):
            return "copy_file", self._parse_two_paths(text[10:])
        if normalized.startswith("search files "):
            return "search_files", {"query": text[13:].strip()}
        if normalized.startswith("shutdown"):
            return "shutdown", {}
        if normalized.startswith("restart"):
            return "restart", {}
        if normalized.startswith("lock"):
            return "lock", {}
        return "unknown", {"text": text}

    def _parse_two_paths(self, remainder: str) -> Dict[str, Any]:
        if " to " in remainder:
            source, destination = remainder.split(" to ", 1)
            return {"source": source.strip(), "destination": destination.strip()}
        return {"source": remainder.strip(), "destination": ""}
